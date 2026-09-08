"""Query normalized v3 metadata: python build/get_metadata.py FILE dotted.key."""
import argparse
import json
from pathlib import Path
from hkbuild.metadata import load

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('key')
    args = parser.parse_args()
    value = load(args.file)
    for part in args.key.split('.'):
        value = value.get(part) if isinstance(value, dict) else None
    print(value if isinstance(value, str) else json.dumps(value))
