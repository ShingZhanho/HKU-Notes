"""Target selection without CI-specific output or branch assumptions."""
from pathlib import Path
import re
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


def build_tree(lines) -> dict:
    tree = {}
    stack = [(-1, tree)]  # (indent_level, current_dict)
    for line in lines:
        # Skip comments and empty lines
        if line.strip() == "" or line.lstrip().startswith("#"):
            continue
        # Count leading tabs for indentation level
        indent = 0
        while line.startswith('\t' * (indent + 1)):
            indent += 1
        key = line.strip()
        # Remove from stack until we find the correct parent
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent_dict = stack[-1][1]
        # Merge if key exists, else create
        if key not in parent_dict:
            parent_dict[key] = {}
        stack.append((indent, parent_dict[key]))
    # Recursively convert empty dicts to None
    def clean(d):
        for k, v in d.items():
            if v == {}:
                d[k] = None
            else:
                clean(v)
    clean(tree)
    return tree

def flatten_tree(tree) -> list:
    result = []
    def dfs(node, path):
        for key, child in node.items():
            new_path = path + [key]
            if child is None:
                result.append("".join(new_path))
            else:
                dfs(child, new_path)
    dfs(tree, [])
    return result
