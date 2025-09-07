from mttools import *
from get_authors import Authors
import sqlite3
import sys
import re
import shutil
import os


def main():
    targets_list = sys.argv[1].split(" ")
    alpha_groups = dict() # "alphabet" -> {"course_code": ["targets"]}

    for alpha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        alpha_groups[alpha] = dict()

    alpha_groups["#"] = dict() # for miscellaneous targets
    alpha_groups["#"]["Miscellaneous"] = list()

    for target in targets_list:
        # check if target begins with course code (4 alpha + 4 digits) with regex
        match = re.match(r"([a-zA-Z]{4}\d{4})", target)
        if match:
            course_code = match.group(1).upper()
            # add course code to corresponding alpha group, create if not exists
            alpha = course_code[0].upper()
            if course_code not in alpha_groups[alpha]:
                alpha_groups[alpha][course_code] = list()
            alpha_groups[alpha][course_code].append(target)
        else:
            # treat
            alpha_groups["#"]["Miscellaneous"].append(target)
    
    # sort all course codes and all targets
    for alpha in alpha_groups:
        for course_code in alpha_groups[alpha]:
            alpha_groups[alpha][course_code].sort()
        alpha_groups[alpha] = dict(sorted(alpha_groups[alpha].items()))

    # generate details pages
    os.mkdir("./site/docs/downloads/details")
    for target in targets_list:
        metadata_reader = Reader(f"./src/{target}/metadata.json", target)
        metadata = metadata_reader.parse()

        if is_alias_target := metadata.computed__is_alias():
            continue  # no details page for alias targets

        src_checksum = ""
        compiled_at = ""
        with open(f"./gh-out/files/{target}/src-checksum.txt", "r") as f:
            src_checksum = f.read().strip()
        with open(f"./gh-out/files/{target}/compiled-at.txt", "r") as f:
            compiled_at = f.read().strip()
        custom_md_file = metadata.static_site__custom_md_file
        custom_md_content = ""
        if custom_md_file != "":
            with open(f"./src/{target}/{custom_md_file}", "r") as f:
                custom_md_content = f.read()
        output_file = metadata.output_file
        with open(f"./site/docs/downloads/details/{target}.md", "w") as f:
            print(f"Generating details page for {target}")
            ## Front matter in YAML
            f.write(f"---\nhide:\n  - navigation\ndescription: Download {target} for free - {metadata.static_site__description}\ncomments: true\n---\n")

            ## Header
            f.write(f"# {target}\n\n")

            ## Content
            f.write(f"**File description:** {metadata.static_site__description}\n\n")
            f.write(f"**Document status:** {generate_badge(metadata.static_site__document_status, True)}\n\n")
            f.write(f"**Compiled at:** {compiled_at}\n\n")
            
            ## Authors
            f.write("<div class=\"author-card-container\">\n")
            f.write("<span><strong>Author(s):</strong></span>\n")
            authors = metadata.authors
            if len(authors) == 0:
                raise ValueError(f"{target} has no authors specified in metadata.json. The default value is overwritten incorrectly.")
            # check main author number
            main_author_count = len([a for a in authors if a.startswith("!")])
            if main_author_count > 1:
                raise ValueError(f"{target} has more than one main author specified in metadata.json.")
            
            authors_manager = Authors()
            authors = list(set([a if authors_manager.author_exists(a) else "@unknown" for a in authors]))
            if "@unknown" in authors:
                # move "@unknown" to the end
                authors.remove("@unknown")
                authors.append("@unknown")
            unknown_author_count = authors.count("@unknown")
            if main_author_count == 1:
                # move the main author to the front
                main_author = [a for a in authors if a.startswith("!")][0]
                authors.remove(main_author)
                authors.insert(0, main_author)
            authors_names_id = [(authors_manager.get_author_display_name(a), a) for a in authors]  # [(author_display_name, author_id)]
            sorted_authors = []
            if main_author_count == 1:
                sorted_authors.append(authors_names_id[0])
                authors_names_id = authors_names_id[1:]
            if unknown_author_count == 1:
                authors_names_id = authors_names_id[:-1]  # remove the last author, which is "@unknown"
            sorted_authors.extend(sorted(authors_names_id, key=lambda x: x[0]))
            if unknown_author_count == 1:
                sorted_authors.append((authors_manager.get_author_display_name("@unknown"), "@unknown"))

            if main_author_count == 0 and unknown_author_count == 0:
                sorted_authors[0] = (sorted_authors[0][0], f"!{sorted_authors[0][1]}")  # make the first author a main author

            for author in sorted_authors:
                author_display_name, author_id = author
                author_href = authors_manager.get_author_href(author_id)
                author_avatar = authors_manager.get_author_avatar(author_id)

                f.write(f"<a class=\"author-card md-button")
                if author_id.startswith("!"):
                    f.write(" md-button--primary")
                f.write("\" title=\"You will be redirected to the author's defined URL, which may be outside of this website.\"")
                f.write(f" href=\"{author_href}\">\n")
                f.write(f"<img class=\"author-card__avatar\" src=\"{author_avatar}\" alt=\"{author_display_name}'s avatar\" />\n")
                f.write(f"<span class=\"author-card__name\">{author_display_name}</span>\n")
                f.write("</a>\n")
            f.write("</div>\n\n")

            ## Primary button
            if not metadata.static_site__primary_button__disabled:
                f.write(f"[{metadata.static_site__primary_button__text}")
                if metadata.static_site__primary_button__icon is not None and metadata.static_site__primary_button__icon != "":
                    f.write(f" :{metadata.static_site__primary_button__icon}:")
                f.write(f"]({metadata.static_site__primary_button__href})")
                f.write("{.md-button .md-button--primary}\n")

            ## Secondary button
            if not metadata.static_site__secondary_button__disabled:
                f.write(f"[{metadata.static_site__secondary_button__text}")
                if metadata.static_site__secondary_button__icon is not None and metadata.static_site__secondary_button__icon != "":
                    f.write(f" :{metadata.static_site__secondary_button__icon}:")
                f.write(f"]({metadata.static_site__secondary_button__href})")
                f.write("{.md-button}\n")

            f.write(f"\n\n")

            ## PDF preview if file is a PDF
            pdf_viewer_string = None
            if metadata.output_file.endswith(".pdf") and metadata.static_site__pdf_viewer != "hidden":
                pdf_viewer_string = f"\n\n<iframe src=\"https://docs.google.com/gview?url=https://shingzhanho.github.io/HKU-Notes/files/{target}/{output_file}"
                pdf_viewer_string += "&embedded=true\" style=\"width: 100%; height: 600px;\" frameborder=\"0\"></iframe>\n\n"

            ## Write PDF viewer to head
            if pdf_viewer_string is not None and metadata.static_site__pdf_viewer == "at_head":
                f.write(pdf_viewer_string)

            ## Find PDF viewer tag in custom md
            if pdf_viewer_string is not None and metadata.static_site__pdf_viewer == "at_tag":
                tag_occ = custom_md_content.count("<!-- % PDF_VIEWER % -->")

                if tag_occ == 0:
                    raise ValueError(f"{target} has pdf_viewer set to 'at_tag' but no '<!-- % PDF_VIEWER % -->' tag found in the custom markdown.")
                elif tag_occ > 1:
                    raise ValueError(f"{target} has multiple '<!-- % PDF_VIEWER % -->' tags found in the custom markdown.")

                custom_md_content = custom_md_content.replace("<!-- % PDF_VIEWER % -->", pdf_viewer_string)

            ## Custom page content
            f.write(custom_md_content)

            if pdf_viewer_string is not None and metadata.static_site__pdf_viewer == "at_footer":
                f.write(pdf_viewer_string)

    # generate course catalogue page
    with open("./site/docs/downloads/index.md", "w") as f:
        print("Generating course catalogue page")
        f.write("---\nhide:\n  - navigation\n")
        f.write("description: Download free and open source HKU computer science course notes/cheatsheets/materials. ")
        f.write("Discover tips and tricks for your studies at the University of Hong Kong.\n")
        f.write("comments: true")
        f.write("\n---\n")
        f.write(f"# Course Catalogue\n\n")
        f.write("All materials are sorted by course code. Use the navigation panel to jump to the course you want.\n\n")
        for alpha in alpha_groups:
            if len(alpha_groups[alpha]) == 0:
                continue
            if alpha == "#" and len(alpha_groups[alpha]["Miscellaneous"]) == 0:
                continue
            f.write(f"## {alpha}\n\n")
            for course_code in alpha_groups[alpha]:
                course_name = get_course_name(course_code)
                f.write(f"### {course_code}")
                f.write(f" - {course_name}\n\n" if course_name else "\n\n")
                f.write("| Material Name | Description | Compiled At | Author(s) | Status |\n")
                f.write("| --- | --- | --- | --- | :-: |\n")
                for target in alpha_groups[alpha][course_code]:
                    metadata_reader = Reader(f"./src/{target}/metadata.json", target)
                    metadata = metadata_reader.parse()

                    if is_alias_target := metadata.computed__is_alias():
                        metadata_reader = Reader(f"./src/{metadata.static_site__alias_to}/metadata.json", metadata.static_site__alias_to)
                        metadata = metadata_reader.parse()
                        alias_from = target
                        target = metadata.name

                    ## Compiled At 
                    compiled_at = ""
                    with open(f"./gh-out/files/{target}/compiled-at.txt", "r") as f2:
                        compiled_at = f2.read().strip().replace(" UTC+8 (Hong Kong)", "")

                    ## Description
                    description = ""
                    if is_alias_target:
                        description = f"_(An alias of [{target}](./details/{target}.md).)_"
                    else:
                        description = metadata.static_site__description

                    ## Document Status
                    document_status = metadata.static_site__document_status
                    status_badge = generate_badge(document_status, False)

                    ## Author(s)
                    authors = metadata.authors
                    if len(authors) == 0:
                        raise ValueError(f"{target} has no authors specified in metadata.json. The default value is overwritten incorrectly.")
                    # check main author number
                    main_author_count = len([a for a in authors if a.startswith("!")])
                    if main_author_count > 1:
                        raise ValueError(f"{target} has more than one main author specified in metadata.json.")
                    authors_manager = Authors()
                    authors = list(set([a if authors_manager.author_exists(a) else "@unknown" for a in authors]))
                    if "@unknown" in authors:
                        # move "@unknown" to the end
                        authors.remove("@unknown")
                        authors.append("@unknown")
                    unknown_author_count = authors.count("@unknown")
                    if main_author_count == 1:
                        # move the main author to the front
                        main_author = [a for a in authors if a.startswith("!")][0]
                        authors.remove(main_author)
                        authors.insert(0, main_author)
                    authors_names = [authors_manager.get_author_display_name(a) for a in authors]
                    sorted_authors = []
                    if main_author_count == 1:
                        sorted_authors.append(authors_names[0])
                        authors_names = authors_names[1:]
                    if unknown_author_count == 1:
                        authors_names = authors_names[:-1]  # remove the last author, which is "@unknown"
                    sorted_authors.extend(sorted(authors_names))
                    if unknown_author_count == 1:
                        sorted_authors.append(authors_manager.get_author_display_name("@unknown"))

                    if len(sorted_authors) == 1:
                        authors_str = sorted_authors[0]
                    else:
                        authors_str = sorted_authors[0] + " et al."

                    f.write(f"| [{target if not is_alias_target else alias_from}](./details/{target}.md) | {description} | {compiled_at} | {authors_str} | {status_badge} |\n")
                f.write("\n\n")
            f.write("\n\n")

    # copy static files in .COPY directory
    for target in targets_list:
        if os.path.exists(f"./src/{target}/.COPY"):
            print(f"Copying static files for {target}")
            os.makedirs(f"./site/docs/downloads/{target}", exist_ok=True)
            shutil.copytree(f"./src/{target}/.COPY", f"./site/docs/downloads/{target}", dirs_exist_ok=True, copy_function=shutil.copy2, symlinks=False)

def generate_badge(status: str, is_detail_page: bool) -> str:
    """
    Generate a badge for the given status.
    """
    status_icons = {
        "sre": "material-check-circle",
        "wip": "material-sign-caution",
        "lts": "material-archive-clock",
        "abd": "material-pencil-off",
        "obs": "material-clock-alert",
        "fin": "material-calendar-end",
        "unk": "material-help",
    }
    status_icon = status_icons.get(status, "material-alert-octagon")

    status_descs = {
        "sre": "This is a stable release of the document.",
        "wip": "This document is still under editing and is incomplete.",
        "lts": "This is a long-term support document.",
        "abd": "This document is no longer being updated and is incomplete.",
        "obs": "This document is now deprecated.",
        "fin": "This document is at its final state.",
        "unk": "The status of this document is unknown.",
    }
    status_desc = status_descs.get(status, "An error happened during the website generation process.")

    static_hrefs = {
        "sre": "stable-release",
        "wip": "work-in-progress",
        "lts": "long-term-support",
        "abd": "abandoned",
        "obs": "obsolete",
        "fin": "final-state",
        "unk": "unknown-status",
    }
    static_href = static_hrefs.get(status, "error")
    static_href = "../document-status.md#" + static_href if is_detail_page else "document-status.md#" + static_href

    return """<span class=\"status-badge\">
    <span class=\"status-badge__icon\">:{% status-icon %}:</span>
    <span class=\"status-badge__text\">[{% status-name %}]({% status-href %} \"{% status-desc %} Click for more details.\")</span>
    </span>""".replace("{% status-icon %}", status_icon).replace("{% status-name %}", status.upper()).replace("{% status-href %}", static_href).replace("{% status-desc %}", status_desc).replace("\n", "")

def get_course_name(course_code: str) -> str:
    """
    Get the course name from the course code.
    """
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

if __name__ == "__main__":
    main()
