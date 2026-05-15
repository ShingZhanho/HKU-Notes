# generate_nav.py
# This script generates the navigation list for the Resources section in site/mkdocs.yml.
# It replaces the placeholder comment line "# == RES_LIST_PLACEHOLDER == #" with the
# generated YAML navigation entries.
#
# Usage: python3 ./build/generate_nav.py "<space-separated targets list>"
#
# The nav is generated in this format (under "- Resources:" at 4-space indent):
#
#       - COMP2120:
#           - COMP2120-Notes: downloads/details/COMP2120-Notes.md
#           - COMP2120-Cheatsheet: downloads/details/COMP2120-Cheatsheet.md
#
# Alias targets are included but their link points to the actual (alias_to) target's page.

import sys
from mttools import Reader, Metadata

PLACEHOLDER = "# == RES_LIST_PLACEHOLDER == #"
MKDOCS_FILE = "./site/mkdocs.yml"
FIRST_LEVEL_INDENT = " " * 6   # 6 spaces — course code level (child of "- Resources:")
SECOND_LEVEL_INDENT = " " * 8  # 8 spaces — individual target level


def get_course_code(target: str) -> str:
    """
    Returns the 8-character course code if the target name starts with one
    (e.g. "COMP2120" from "COMP2120-Notes"), otherwise returns "Miscellaneous".
    A valid course code has 4 alpha chars followed by 4 digit chars.
    """
    if len(target) > 8 and target[:4].isalpha() and target[4:8].isdigit():
        return target[:8]
    return "Miscellaneous"


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("Usage: python3 generate_nav.py \"<space-separated targets list>\"")
        sys.exit(1)

    targets_list = [t for t in sys.argv[1].split() if t.strip()]

    # Group targets by course code; alias targets link to the alias_to target's page
    # course_nav maps course_code -> list of (display_name, link_target) tuples
    course_nav: dict[str, list[tuple[str, str]]] = {}

    for target in targets_list:
        metadata: Metadata = Reader(f"./src/{target}/metadata.json", target).parse()
        if metadata.computed.is_alias.get():
            link_target = metadata.static_site.alias_to.get()
            print(f"Alias target: {target} -> {link_target}")
        else:
            link_target = target

        course_code = get_course_code(target)
        if course_code not in course_nav:
            course_nav[course_code] = []
        course_nav[course_code].append((target, link_target))

    # Sort course codes and entries within each course by display name
    course_nav = dict(sorted(course_nav.items()))
    for course_code in course_nav:
        course_nav[course_code].sort(key=lambda x: x[0])

    # Generate the YAML nav lines
    nav_lines = []
    for course_code, entries in course_nav.items():
        nav_lines.append(f"{FIRST_LEVEL_INDENT}- {course_code}:")
        for display_name, link_target in entries:
            nav_lines.append(
                f"{SECOND_LEVEL_INDENT}- {display_name}: downloads/details/{link_target}.md"
            )

    nav_str = "\n".join(nav_lines)

    # Replace the placeholder in mkdocs.yml
    with open(MKDOCS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if PLACEHOLDER not in content:
        print(f"Warning: Placeholder '{PLACEHOLDER}' not found in {MKDOCS_FILE}. Nothing replaced.")
        return

    new_content = content.replace(PLACEHOLDER, nav_str)

    with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    total = sum(len(v) for v in course_nav.values())
    print(f"Generated nav with {len(course_nav)} course(s) and {total} target(s).")


if __name__ == "__main__":
    main()
