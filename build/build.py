#!/usr/bin/env python3
"""CI-neutral command-line entry point."""
import subprocess
import sys
from hkbuild.cli import main

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(f'build: {error}')
