from mttools import Reader, Metadata

def gen_catalogue_page(targets: dict[str, dict[str, list[str]]]):
    print("Generating catalogue page...")

    f = open("./site/docs/downloads/index.md", "w", encoding="utf-8")

    # Prepare front matter data
    from .utils import write_front_matters
    front_matter = {
        "hide": [
            "navigation",
        ],
        "description": "Browse and download free HKU notes and materials. \
            Mainly for Computer Science courses but some common core courses are also available!",
        "comments": True,
    }
    write_front_matters(f, front_matter)
    print("Front matter written.")

    f.write("\n# Course Catalogue\n\n")

    # Write catalogue content
    # for each leading alphabet:
    for alphabet in targets.keys():
        if len(targets[alphabet]) == 0:
            continue
        if alphabet == "#" and len(targets[alphabet]["Miscellaneous"]) == 0:
            continue
        print(f"Writing catalogue section for leading alphabet: {alphabet}")

        if alphabet == "#":
            f.write('## \\#\n\n')
        else:
            f.write(f'## {alphabet}\n\n')

        # for each course code under the leading alphabet:
        for course_code in targets[alphabet].keys():
            course_name = __get_course_name(course_code)
            print(f"Writing catalogue subsection for course code: {course_code}")
            # course code and name h3 header
            f.write(f'### {course_code}')
            if course_name:
                f.write(f' - {course_name}')
            f.write('\n\n')

            # table header row
            f.write('| Material Name | Description | Last Modified | Author(s) | Status |\n')
            f.write('| --- | --- | --- | --- | :-: |\n')

            # for each target under the course code:
            for target in targets[alphabet][course_code]:
                metadata: Metadata = Reader(f"./src/{target}/metadata.json", target).parse()
                print(f"Writing catalogue entry for target: {target}")
                flag_is_alias = metadata.computed__is_alias()

                # alias targets:
                if flag_is_alias:
                    # override metadata with the aliased target's metadata
                    metadata = Reader(f'./src/{metadata.static_site__alias_to}/metadata.json', metadata.static_site__alias_to).parse()
                    alias_from = target
                    target = metadata.name

                # Description
                description = (metadata.static_site__description 
                                    if not flag_is_alias else
                              f"_An alias of [{target}](./details/{target}.md)_")
                
                # Last Modified
                from .utils import get_last_modified_time_hkt
                last_modified = get_last_modified_time_hkt(target)

                # Authors
                from .authors_resolver import get_authors_summary, resolve_authors
                authors_string = get_authors_summary(resolve_authors(metadata.authors))

                # Status
                from .status_badge import get_badge_str
                status_badge = get_badge_str(metadata.static_site__document_status, False)

                # write table row
                f.write("".join((
                    "| ",
                    f"[{target if not flag_is_alias else alias_from}](./details/{target}.md)",
                    " | ",
                    description,
                    " | ",
                    last_modified,
                    " | ",
                    authors_string,
                    " | ",
                    status_badge,
                    " |\n",
                )))
            f.write("\n")
        f.write("\n")
    f.close()
    print("Catalogue page generation completed.")

def __get_course_name(course_code: str) -> str:
    """
    Get the course name from the course code.
    """
    if course_code == "Miscellaneous":
        return "Miscellaneous"
    import sqlite3
    conn = sqlite3.connect("./build/course-codes.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT course_name FROM courses WHERE course_code = ?", (course_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        result = row[0]
        # for each word, cap the first letter and lower the rest,
        # except for words that are all uppercase (e.g. "HKU")
        result = ' '.join(word.capitalize() if not word.isupper() else word for word in result.split())
        return result
    return None