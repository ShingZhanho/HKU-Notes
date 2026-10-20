#!/usr/bin/env python3
"""Verify restored document artifacts before provisioning a CI compiler."""
import argparse
import os
from pathlib import Path

from hkbuild.document import check_environment, restore_cached
from hkbuild.fingerprint import fingerprint
from hkbuild.metadata import REPOSITORY, load, resolve_alias


def needs_compilation(document, artifacts, force=False):
    document = resolve_alias(document.resolve())
    spec = load(document / 'metadata.json')['build']
    if spec['type'] == 'page':
        return False, 'page-only target; no compiler needed'
    check_environment(spec)
    if force:
        return True, 'forced build requested'
    if not spec.get('cache', True):
        return True, 'document caching disabled'
    key = fingerprint(document, spec)
    if restore_cached(document, spec, artifacts / document.name, key, None):
        return False, 'sources unchanged; artifacts verified; skipping compiler setup'
    return True, 'changed inputs or missing/invalid artifacts; compiler required'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target')
    args = parser.parse_args()
    document = REPOSITORY / 'src' / args.target
    if document.parent != REPOSITORY / 'src' or not document.is_dir():
        parser.error('Expected a document name directly under src/')
    required, reason = needs_compilation(document, REPOSITORY / 'dist/artifacts',
                                         force=os.environ.get('FORCE_REBUILD') == '1')
    print(f'{args.target}: {reason}')
    if output := os.environ.get('GITHUB_OUTPUT'):
        with Path(output).open('a') as stream:
            stream.write(f'compile={str(required).lower()}\n')
    if summary := os.environ.get('GITHUB_STEP_SUMMARY'):
        with Path(summary).open('a') as stream:
            stream.write(f'- {args.target}: {reason}.\n')


if __name__ == '__main__':
    main()
