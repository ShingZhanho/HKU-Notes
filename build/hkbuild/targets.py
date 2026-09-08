"""Target selection without CI-specific output or branch assumptions."""
from pathlib import Path
import re
from resolve_targets import build_tree, flatten_tree
from .metadata import load, resolve_alias


def select(repository: Path, names: list[str] | None = None) -> list[str]:
    if names is None:
        names = flatten_tree(build_tree((repository / 'build/build-targets.txt').read_text().splitlines()))
    result = []
    for name in names:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name):
            raise ValueError(f'Invalid target name: {name!r}')
        if name in {'all', 'site', 'preview', 'clean', 'distclean', 'help', 'Makefile'}:
            raise ValueError(f'Reserved Make target name: {name}')
        load(repository / 'src' / name / 'metadata.json')
        canonical = resolve_alias(repository / 'src' / name).name
        for item in (canonical, name):
            if item not in result:
                result.append(item)
    if not result:
        raise ValueError('No build targets selected')
    return result
