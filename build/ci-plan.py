#!/usr/bin/env python3
"""Select CI targets once; compile aliases only through their canonical target."""
import json
import os
from pathlib import Path

from hkbuild.metadata import REPOSITORY, resolve_alias
from hkbuild.targets import select


def plan(branch, repository=REPOSITORY):
    parts = branch.split('/')
    names = [parts[1]] if len(parts) >= 3 and parts[0] == 'targets' else None
    targets = select(repository, names)
    canonical = list(dict.fromkeys(resolve_alias(repository / 'src' / name).name for name in targets))
    return {'targets': targets, 'matrix': {'target': canonical}}


if __name__ == '__main__':
    result = plan(os.environ.get('TARGET_BRANCH', 'master'))
    if output := os.environ.get('GITHUB_OUTPUT'):
        with Path(output).open('a') as stream:
            for name, value in result.items():
                stream.write(f'{name}={json.dumps(value, separators=(",", ":"))}\n')
    else:
        print(json.dumps(result))
