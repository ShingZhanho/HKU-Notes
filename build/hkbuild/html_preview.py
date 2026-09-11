"""Cached, local pdf2htmlEX conversion. No TeX execution or remote conversion API."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

from .document import digest, inside, write_json

IMAGE = 'pdf2htmlex/pdf2htmlex@sha256:89fc3eaf829f4e786b6b07d4821026bd9ddb14614ec6db2959b0f492dbbcc597'
FORMAT = 1
OPTIONS = ['--embed', 'cfijo', '--split-pages', '0', '--process-outline', '0',
           '--correct-text-visibility', '1']


def backend():
    native = os.environ.get('PDF2HTMLEX') or shutil.which('pdf2htmlEX')
    if native:
        native = shutil.which(native) or native
        version = subprocess.run([native, '--version'], capture_output=True, text=True, check=True, timeout=30)
        return [native], hashlib.sha256((version.stdout + version.stderr).encode()).hexdigest()
    if not shutil.which('docker'):
        raise ValueError('HTML previews require pdf2htmlEX or a running Docker-compatible engine; see README.md')
    return None, IMAGE


def convert(pdf, destination, native):
    name = 'hku-preview-' + uuid.uuid4().hex
    args = [*OPTIONS, '--dest-dir', str(destination), str(pdf), 'document.html']
    if native:
        command = native + args
    else:
        command = ['docker', 'run', '--rm', '--name', name, '--platform', 'linux/amd64',
                   '--network', 'none', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                   '--user', f'{os.getuid()}:{os.getgid()}',
                   '--mount', f'type=bind,source={pdf.parent},target=/input,readonly',
                   '--mount', f'type=bind,source={destination},target=/output',
                   '--entrypoint', 'pdf2htmlEX', IMAGE, *OPTIONS,
                   '--dest-dir', '/output', '/input/' + pdf.name, 'document.html']
    try:
        subprocess.run(command, check=True, timeout=600)
    finally:
        if not native:
            # A timed-out/interrupted Docker client can otherwise leave its container running.
            subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=30)


def preview(directory):
    directory = Path(directory).resolve()
    manifest = json.loads((directory / 'manifest.json').read_text())
    output = manifest['outputs'].get('primary')
    if not output or not output['path'].lower().endswith('.pdf'):
        return
    pdf = inside(directory, output['path'])
    if digest(pdf) != output['sha256']:
        raise ValueError(f'Artifact checksum mismatch: {pdf}')
    native, identity = backend()
    key = {'format': FORMAT, 'pdf': output['sha256'], 'converter': identity, 'options': OPTIONS}
    destination = directory / '~preview'
    stamp = directory / 'preview.json'
    if stamp.exists() and destination.is_dir():
        previous = json.loads(stamp.read_text())
        files = {str(p.relative_to(destination)): digest(p) for p in sorted(destination.rglob('*')) if p.is_file()}
        if previous.get('key') == key and files and previous.get('files') == files:
            print(f'Unchanged HTML preview: {manifest["target"]}', flush=True)
            return
    with tempfile.TemporaryDirectory(prefix='html-preview-', dir=directory) as tmp:
        temporary = Path(tmp)
        convert(pdf, temporary, native)
        from bs4 import BeautifulSoup
        html = temporary / 'document.html'
        soup = BeautifulSoup(html.read_text(), 'html.parser')
        if not soup.select('#page-container .pf'):
            raise ValueError(f'pdf2htmlEX produced no pages for {pdf}')
        # Viewer JS assumes a global document and loads pages on demand. The site
        # supplies its own shadow-aware controls and keeps all text rendered.
        for script in soup.find_all('script'):
            script.decompose()
        html.write_text(str(soup), encoding='utf-8')
        files = {str(p.relative_to(temporary)): digest(p) for p in sorted(temporary.rglob('*')) if p.is_file()}
        backup = directory / '~preview.previous'
        if backup.exists():
            shutil.rmtree(backup)
        if destination.exists():
            destination.rename(backup)
        try:
            temporary.rename(destination)
            write_json(stamp, {'key': key, 'files': files})
        except BaseException:
            if destination.exists():
                shutil.rmtree(destination)
            if backup.exists():
                backup.rename(destination)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    print(f'Generated HTML preview: {manifest["target"]}', flush=True)
