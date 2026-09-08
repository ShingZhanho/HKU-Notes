import argparse
import json
from pathlib import Path
import shutil
import sys

from . import document
from .configure import MARKER
from .metadata import REPOSITORY, resolve_alias
from .targets import select


def main(argv=None):
    parser = argparse.ArgumentParser(description='Shared document/site build runner')
    parser.add_argument('--config', type=Path)
    parser.add_argument('--force', action='store_true', help='Bypass artifact/step caches and force TeX compilation')
    parser.add_argument('command', choices=['build', 'preview', 'site', 'clean', 'distclean', 'targets', 'validate'])
    parser.add_argument('targets', nargs='*')
    args = parser.parse_args(argv)
    if args.command in ('targets', 'validate'):
        targets = select(REPOSITORY, args.targets or None)
        if args.command == 'targets':
            print(json.dumps(targets))
        else:
            from .metadata import load
            paths = list((REPOSITORY / 'src').rglob('metadata.json'))
            paths = [p for p in paths if '.build' not in p.parts]
            for path in paths:
                load(path)
                resolve_alias(path.parent)
            print(f'Validated {len(paths)} metadata files and {len(targets)} selected targets')
        return
    if not args.config:
        parser.error('--config is required; run configure and make')
    config = json.loads(args.config.read_text())
    repository = Path(config['repository'])
    directory = Path(config['directory'])
    selected = args.targets or config['targets']
    if any(name not in config['targets'] for name in selected):
        parser.error('Target was not configured; rerun configure with the desired selection')
    documents = list(dict.fromkeys(resolve_alias(directory if config['mode'] == 'document' else repository / 'src' / name) for name in selected))
    artifacts = Path(config['artifact_root'])
    if args.command == 'build':
        for path in documents:
            document.build(path, artifacts, config['profile'], config['source_dir'], config['artifact_input'], force=args.force)
    elif args.command == 'preview':
        for path in documents:
            document.preview(artifacts / path.name)
    elif args.command == 'site':
        if config['mode'] != 'repository':
            parser.error('Website assembly requires repository configuration')
        from .website import assemble
        assemble(repository, selected, artifacts, config['site_url'])
    else:
        for path in documents:
            with document.document_lock(path):
                document.clean(path, args.command == 'distclean')
                (artifacts / path.name / 'manifest.json').unlink(missing_ok=True)
        if config['mode'] == 'repository':
            for path in (repository / '.build/site', repository / 'dist/site'):
                if path.exists():
                    shutil.rmtree(path)
        if args.command == 'distclean':
            for path in [*documents, directory]:
                makefile = path / 'Makefile'
                if makefile.exists() and makefile.read_text().startswith(MARKER):
                    makefile.unlink()
                if (path / '.build').exists():
                    shutil.rmtree(path / '.build')
            if config['mode'] == 'repository':
                for path in documents:
                    artifact = artifacts / path.name
                    if artifact.exists():
                        shutil.rmtree(artifact)
