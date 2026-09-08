"""Document execution shared by Make, the CLI, and CI."""
from contextlib import contextmanager
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

from .metadata import load, resolve_alias


def run(argv, cwd=None, capture=False):
    argv = [str(value) for value in argv]
    print('+ ' + ' '.join(argv), flush=True)
    return subprocess.run(argv, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None)


def inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes {root}: {relative}')
    return path


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_changed(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() == destination.resolve():
        return
    if not destination.is_file() or digest(source) != digest(destination):
        shutil.copy2(source, destination)


@contextmanager
def document_lock(document):
    # The supported shells are POSIX (including WSL). OS locks are released on failure.
    import fcntl
    directory = document / '.build'
    directory.mkdir(exist_ok=True)
    with (directory / 'lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def expand(value, document, source):
    for key, replacement in {'python': sys.executable, 'document': document, 'source': source}.items():
        value = value.replace('{' + key + '}', str(replacement))
    return value


def check_environment(spec):
    requested = spec.get('environment', {})
    actual = {'os': platform.system().lower(),
              'architecture': {'amd64': 'x86_64', 'aarch64': 'arm64'}.get(platform.machine().lower(), platform.machine().lower())}
    if actual['os'] == 'linux':
        release = platform.freedesktop_os_release()
        actual.update(distribution=release.get('ID'), version=release.get('VERSION_ID'))
    differences = [f'{key}={value} (current: {actual.get(key, "unknown")})'
                   for key, value in requested.items() if actual.get(key) != value]
    if differences:
        raise ValueError('Required build environment: ' + ', '.join(differences) +
                         '. Use the Ubuntu build container or configure --artifact-dir with an existing artifact.')


def check_tools(document, spec, source_override=None):
    if spec['type'] == 'page':
        return
    check_environment(spec)
    executables = set(spec.get('requires', {}).get('executables', []))
    if spec['type'] == 'latex':
        executables.update(['latexmk', spec.get('engine', 'pdflatex')])
    if spec.get('source') and not source_override:
        executables.add('git')
    for step in [*spec.get('prepare', []), *spec.get('steps', []), *spec.get('finish', [])]:
        if step['type'] == 'latex':
            executables.update(['latexmk', step.get('engine', 'pdflatex')])
        elif step['type'] == 'wordcount':
            executables.add('texcount')
        elif step['type'] == 'shell':
            executables.add(step['interpreter'])
        elif step['argv'][0] != '{python}' and '/' not in step['argv'][0] and '{' not in step['argv'][0]:
            executables.add(step['argv'][0])
    missing = [tool for tool in sorted(executables) if not shutil.which(tool)]
    for package in spec.get('requires', {}).get('python', []):
        try:
            importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            missing.append(f'Python package {package}')
    if missing:
        raise ValueError(f'{document.name}: missing dependencies: {", ".join(missing)}. See README.md for setup.')


def source_root(document, spec, override=None):
    if override:
        source = Path(override).resolve()
        if not source.is_dir():
            raise ValueError(f'Source directory does not exist: {source}')
        return source
    declaration = spec.get('source')
    if not declaration:
        return document
    key = hashlib.sha256(json.dumps(declaration, sort_keys=True).encode()).hexdigest()[:20]
    destination = document / '.build/sources' / key
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
            checkout = Path(temporary) / 'checkout'
            run(['git', 'init', checkout])
            run(['git', 'remote', 'add', 'origin', declaration['url']], checkout)
            run(['git', 'fetch', '--depth=1', 'origin', declaration['revision']], checkout)
            run(['git', 'checkout', '--detach', 'FETCH_HEAD'], checkout)
            checkout.rename(destination)
    # Detect a manually altered cache rather than compiling a different revision.
    revision = run(['git', 'rev-parse', 'HEAD'], destination, capture=True).stdout.strip()
    if revision != declaration['revision']:
        raise ValueError(f'Source cache revision mismatch: {destination}')
    source = inside(destination, declaration.get('subdirectory', '.'))
    if not source.is_dir():
        raise ValueError(f'Missing source subdirectory: {source}')
    return source


def input_files(source, patterns):
    result = []
    for pattern in patterns:
        inside(source, pattern)
        matches = sorted(path for path in source.glob(pattern) if path.is_file())
        if not matches:
            raise ValueError(f'Input pattern has no files: {source / pattern}')
        for path in matches:
            inside(source, str(path.relative_to(source)))
            if path not in result:
                result.append(path)
    return result


def latex(source, relative, spec, state):
    root = inside(source, relative)
    if not root.is_file():
        raise ValueError(f'Missing TeX root: {root}')
    mode = {'pdflatex': '-pdf', 'xelatex': '-xelatex', 'lualatex': '-lualatex'}[spec.get('engine', 'pdflatex')]
    command = ['latexmk', mode, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-synctex=1']
    command.append('-shell-escape' if spec.get('shell_escape', False) else '-no-shell-escape')
    if spec.get('config_file'):
        command.extend(['-r', str(inside(source, spec['config_file']))])
    command.extend(spec.get('args', []))
    command.extend(['-cd', str(root)])
    # Record ownership before execution so clean also works after a failed compile.
    if str(root) not in state['tex_roots']:
        state['tex_roots'].append(str(root))
    run(command, source)
    output = root.with_suffix('.pdf')
    if not output.is_file():
        raise ValueError(f'LaTeX did not produce {output}')
    return output


def execute_step(step, source, document, state, key):
    kind = step['type']
    if kind == 'latex':
        for file in input_files(source, step['inputs']):
            latex(source, str(file.relative_to(source)), step, state)
        return
    files = input_files(source, step.get('inputs', []))
    outputs = [inside(source, path) for path in step.get('outputs', [])]
    if kind == 'wordcount':
        outputs = [inside(source, step['output'])]
    signature = hashlib.sha256(json.dumps({'step': step, 'source': str(source),
        'inputs': [(str(path), digest(path)) for path in files]}, sort_keys=True).encode()).hexdigest()
    previous = state['steps'].get(key)
    current_outputs = {str(path): digest(path) for path in outputs if path.is_file()}
    if files and outputs and previous == {'signature': signature, 'outputs': current_outputs} and len(current_outputs) == len(outputs):
        return
    cwd = inside(source, step.get('cwd', '.'))
    if kind == 'command':
        run([expand(arg, document, source) for arg in step['argv']], cwd)
    elif kind == 'shell':
        run([step['interpreter'], '-c', step['script']], cwd)
    elif kind == 'wordcount':
        total = 0
        for file in files:
            output = run(['texcount', str(file)], source, capture=True).stdout
            match = re.search(r'^Words in text:\s*(\d+)', output, re.MULTILINE)
            if not match:
                raise ValueError(f'texcount returned no text count for {file}')
            total += int(match[1])
        outputs[0].parent.mkdir(parents=True, exist_ok=True)
        text = f'{total}\n'
        if not outputs[0].exists() or outputs[0].read_text() != text:
            outputs[0].write_text(text)
    for output in outputs:
        if not output.is_file():
            raise ValueError(f'Step did not produce {output}')
    state['steps'][key] = {'signature': signature, 'outputs': {str(path): digest(path) for path in outputs}}


def publish(document, spec, artifact_root, profile=None):
    directory = artifact_root / document.name
    directory.mkdir(parents=True, exist_ok=True)
    outputs = {}
    if spec['type'] != 'page':
        outputs = {'primary': spec['output_file'], **spec.get('outputs', {})}
    entries = {}
    for name, relative in outputs.items():
        source = inside(document, relative)
        if not source.is_file():
            raise ValueError(f'{document.name}: expected output is missing: {source}')
        copy_changed(source, inside(directory, relative))
        entries[name] = {'path': relative, 'sha256': digest(source)}
    manifest = {'version': 1, 'target': document.name, 'type': spec['type'], 'profile': profile, 'outputs': entries}
    write_json(directory / 'manifest.json', manifest)
    return directory


def build(document, artifact_root, profile=None, source_override=None, artifact_input=None):
    document = document.resolve()
    canonical = resolve_alias(document)
    if canonical != document:
        return build(canonical, artifact_root, profile, source_override, artifact_input)
    spec = load(document / 'metadata.json', profile)['build']
    with document_lock(document):
        state_path = document / '.build/state.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {'tex_roots': [], 'steps': {}, 'published': []}
        try:
            supplied = Path(artifact_input) / document.name if artifact_input else None
            if supplied and supplied.is_dir() and spec['type'] != 'page':
                for relative in [spec['output_file'], *spec.get('outputs', {}).values()]:
                    source = inside(supplied, relative)
                    if not source.is_file():
                        raise ValueError(f'Supplied artifact is missing: {source}')
                    copy_changed(source, inside(document, relative))
            elif spec['type'] != 'page':
                check_tools(document, spec, source_override)
                source = source_root(document, spec, source_override)
                for phase in ('prepare', 'main', 'finish'):
                    if phase == 'main' and spec['type'] == 'latex':
                        output = latex(source, spec['root_file'], spec, state)
                        copy_changed(output, inside(document, spec['output_file']))
                    else:
                        for index, step in enumerate(spec.get('steps' if phase == 'main' else phase, [])):
                            execute_step(step, source, document, state, f'{phase}:{index}')
            result = publish(document, spec, artifact_root, profile)
            if spec['type'] != 'page':
                state['published'] = sorted(set(state['published'] + [str(inside(document, value)) for value in [spec['output_file'], *spec.get('outputs', {}).values()]]))
            return result
        finally:
            write_json(state_path, state)


def preview(directory):
    manifest = json.loads((directory / 'manifest.json').read_text())
    output = manifest['outputs'].get('primary')
    if not output or not output['path'].endswith('.pdf'):
        return
    pdf = inside(directory, output['path'])
    key = digest(pdf)
    preview_dir = directory / '~preview'
    stamp = directory / 'preview.json'
    if stamp.exists() and preview_dir.exists():
        previous = json.loads(stamp.read_text())
        if previous.get('pdf') == key and previous.get('images') == {p.name: digest(p) for p in sorted(preview_dir.glob('*.png'))}:
            return
    if not shutil.which('pdftoppm'):
        raise ValueError('PDF previews require pdftoppm (Poppler); see README.md')
    with tempfile.TemporaryDirectory(dir=directory) as temporary:
        temporary = Path(temporary)
        run(['pdftoppm', '-png', '-r', '200', '-forcenum', str(pdf), str(temporary / (manifest['target'] + '_preview'))])
        images = {p.name: digest(p) for p in sorted(temporary.glob('*.png'))}
        if not images:
            raise ValueError(f'No preview images generated for {pdf}')
        if preview_dir.exists():
            shutil.rmtree(preview_dir)
        shutil.copytree(temporary, preview_dir)
    write_json(stamp, {'pdf': key, 'images': images})


def clean(document, distclean=False):
    state_path = document / '.build/state.json'
    if not state_path.exists():
        return
    state = json.loads(state_path.read_text())
    for root in state.get('tex_roots', []):
        root = Path(root)
        if root.is_file():
            run(['latexmk', '-C' if distclean else '-c', '-cd', str(root)], root.parent)
    # Only delete outputs that this runner recorded, never glob through source files.
    if distclean:
        for path in state.get('published', []):
            inside(document, str(Path(path).relative_to(document))).unlink(missing_ok=True)
    state['steps'] = {}
    write_json(state_path, state)
