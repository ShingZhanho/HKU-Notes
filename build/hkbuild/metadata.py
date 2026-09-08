"""Strict, offline metadata loading. Only schema v3 is supported."""
from copy import deepcopy
import json
from pathlib import Path

import jsonschema

REPOSITORY = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY / 'site/docs/statics/schemas/v3.json'
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)


def load(path: Path, profile: str | None = None) -> dict:
    path = Path(path)
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('$schema') not in SCHEMA['properties']['$schema']['enum']:
        raise ValueError(f'{path}: only metadata v3 is supported; migrate v1/v2 metadata')
    errors = sorted(VALIDATOR.iter_errors(data), key=lambda e: str(e.path))
    if errors:
        error = errors[0]
        raise ValueError(f'{path}: {".".join(map(str, error.path))}: {error.message}')
    data = deepcopy(data)
    if profile:
        if profile not in data.get('profiles', {}):
            raise ValueError(f'{path}: unknown profile {profile!r}')
        data['build'].update(data['profiles'][profile])
        try:
            VALIDATOR.validate(data)
        except jsonschema.ValidationError as error:
            raise ValueError(f'{path}: invalid profile {profile!r}: {error.message}') from error
    build = data['build']
    if build['type'] == 'latex':
        build.setdefault('root_file', f'{path.parent.name}.tex')
        build.setdefault('output_file', f'{path.parent.name}.pdf')
        build.setdefault('engine', 'pdflatex')
        build.setdefault('shell_escape', False)
    # Outputs are relative to the document; built-in compilation always produces PDF.
    if build['type'] == 'latex' and not build['output_file'].endswith('.pdf'):
        raise ValueError(f'{path}: a latex output_file must end in .pdf')
    outputs = build.get('outputs', {})
    if 'primary' in outputs:
        raise ValueError(f'{path}: outputs.primary is reserved for output_file')
    filenames = [build['output_file'], *outputs.values()] if 'output_file' in build else []
    if len(set(filenames)) != len(filenames):
        raise ValueError(f'{path}: published output paths must be distinct')
    for filename in filenames:
        if any(char in filename for char in '*?['):
            raise ValueError(f'{path}: output paths cannot contain glob patterns')
        if filename in ('metadata.json', 'Makefile', 'manifest.json', 'preview.json') or filename.startswith(('.build/', '~preview/')):
            raise ValueError(f'{path}: reserved output path {filename}')
    return data


def resolve_alias(document: Path, profile: str | None = None) -> Path:
    seen = []
    document = Path(document).resolve()
    while True:
        if document in seen:
            raise ValueError('Alias cycle: ' + ' -> '.join(p.name for p in [*seen, document]))
        seen.append(document)
        metadata = load(document / 'metadata.json', profile if len(seen) == 1 else None)
        if metadata['build']['type'] != 'alias':
            return document
        document = document.parent / metadata['build']['target']
