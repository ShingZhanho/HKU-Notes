"""Optional standalone page generation; normally invoked by make site."""
import argparse
from pathlib import Path
from hkbuild.metadata import REPOSITORY
from page_gen_tools import start
from page_gen_tools.paths import SitePaths

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, default=REPOSITORY)
    parser.add_argument('--docs', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('targets', nargs='+')
    args = parser.parse_args()
    start(args.targets, SitePaths(args.repository.resolve(), args.docs.resolve(), args.artifacts.resolve()))
