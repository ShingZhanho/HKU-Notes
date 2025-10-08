# hash_tex_pkgs.py
#
# This script calculates the hash value of all LaTeX packages used in a target.
# The script traverses the directory tree and look for .tex, .sty, and .cls files.
# It extracts the package names from the \usepackage, \documentclass, and \RequirePackage commands.
# The hash value is guaranteed to be the same for the same set of packages, regardless of the order
# and optional arguments.
# The calculated hash value is printed to the standard output if the script is run directly,
# or returned as a string if the script is imported as a module.
#
# The hash value will be 0 if one of the following conditions is met:
# 1. The target directory does not exist.
# 2. No .tex, .sty, or .cls files are found in the target directory.
# 3. No packages are found in the .tex, .sty, or .cls files.
#
# The hash value is calculated by SHA-256(sorted_pkgs_hash_string).
# The sorted_pkgs_hash_string is a comma-separated string of hash values of the package names.

import hashlib
import os
import re
import sys

def hash_pkgs(target: str, print_pkg_list: bool = False) -> str:
    PATTERN = r'\\(?:usepackage|documentclass|RequirePackage)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}'
    packages = set()

    target_dir = os.path.join("./src", target)
    if not os.path.exists(target_dir):
        return "0"
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(('.tex', '.sty', '.cls')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = re.findall(PATTERN, content)
                    for match in matches:
                        for pkg in match.split(','):
                            packages.add(pkg.strip())

    if not packages:
        return "0"
    
    sorted_pkgs = sorted(packages)
    if print_pkg_list:
        print(sorted_pkgs)
    hashed_pkgs = [hashlib.sha256(pkg.encode('utf-8')).hexdigest() for pkg in sorted_pkgs]
    pkg_list_str = ','.join(hashed_pkgs)
    hash_value = hashlib.sha256(pkg_list_str.encode('utf-8')).hexdigest()
    return hash_value

if __name__ == "__main__":
    print(hash_pkgs(sys.argv[1], True if (sys.argv[2].lower() if len(sys.argv) > 2 else "") == "true" else False))