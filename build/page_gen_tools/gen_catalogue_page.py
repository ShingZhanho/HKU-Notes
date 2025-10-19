import sqlite3
from mttools import Reader, Metadata
from .utils import write_front_matters, get_last_modified_time_hkt
from .authors_resolver import get_authors_summary, resolve_authors
from .status_badge import get_badge_str

def gen_catalogue_page(targets: dict[str, dict[str, list[str]]]):
    print("Generating catalogue page...")

    f = open("./site/docs/downloads/index.md", "w", encoding="utf-8")

    # Prepare front matter data
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
            if course_name and course_code != "Miscellaneous":
                f.write(f' - {course_name}')
            f.write('\n\n')

            # table header row
            f.write('| Material Name | Description | Last Modified | Author(s) | Status |\n')
            f.write('| --- | --- | --- | --- | :-: |\n')

            # for each target under the course code:
            for target in targets[alphabet][course_code]:
                metadata: Metadata = Reader(f"./src/{target}/metadata.json", target).parse()
                print(f"Writing catalogue entry for target: {target}")
                flag_is_alias = metadata.computed.is_alias.get()

                # alias targets:
                if flag_is_alias:
                    # override metadata with the aliased target's metadata
                    metadata = Reader(f'./src/{metadata.static_site.alias_to.get()}/metadata.json', metadata.static_site.alias_to.get()).parse()
                    alias_from = target
                    target = metadata.name.get()

                # Description
                description = (metadata.static_site.description.get() 
                                    if not flag_is_alias else
                              f"_An alias of [{target}](./details/{target}.md)_")
                
                # Last Modified
                last_modified = get_last_modified_time_hkt(target)

                # Authors
                authors_string = get_authors_summary(resolve_authors(metadata.authors.get()))

                # Status
                status_badge = get_badge_str(metadata.static_site.document_status.get(), False)

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
    conn = sqlite3.connect("./build/course-codes.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT course_name FROM courses WHERE course_code = ?", (course_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        result = row[0]
        # Convert to title case with proper exceptions
        result = __to_title_case(result)
        return result
    return None

def __to_title_case(text: str) -> str:
    """
    Convert text to title case, capitalizing major words while keeping
    minor words (articles, prepositions, conjunctions) lowercase,
    preserving roman numerals and acronyms.
    """
    # Minor words that should be lowercase (unless first or last word)
    minor_words = {
        'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'of', 'on', 
        'or', 'the', 'to', 'via', 'with', 'from', 'into', 'onto', 'than',
        'over', 'upon', 'nor', 'yet', 'so'
    }
    
    # Roman numerals (common ones used in course names)
    roman_numerals = {'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'}
    
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        word_lower = word.lower()
        is_first = i == 0
        is_last = i == len(words) - 1
        
        # Check if it's a roman numeral
        if word_lower in roman_numerals:
            result.append(word.upper())
        # Check if it's an acronym (all uppercase in original, length > 1)
        elif word.isupper() and len(word) > 1:
            result.append(word)
        # Check if it's a contraction (contains apostrophe)
        elif "'" in word:
            # Capitalize first part, keep rest as-is for contractions
            parts = word.split("'")
            result.append(parts[0].capitalize() + "'" + parts[1].lower())
        # Check if it's a minor word (and not first/last)
        elif word_lower in minor_words and not is_first and not is_last:
            result.append(word_lower)
        # Default: capitalize first letter
        else:
            result.append(word.capitalize())
    
    return ' '.join(result)