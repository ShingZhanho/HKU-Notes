from mttools import *
import sys
import re
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
        src_checksum = ""
        compiled_at = ""
        with open(f"./gh-out/files/{target}/src-checksum.txt", "r") as f:
            src_checksum = f.read().strip()
        with open(f"./gh-out/files/{target}/compiled-at.txt", "r") as f:
            compiled_at = f.read().strip()
        metadata_reader = Reader(f"./src/{target}/metadata.json", target)
        metadata = metadata_reader.parse()
        custom_md_file = metadata.static_site__custom_md_file
        custom_md_content = ""
        if custom_md_file != "":
            with open(f"./src/{target}/{custom_md_file}", "r") as f:
                custom_md_content = f.read()
        with open(f"./site/docs/downloads/details/{target}.md", "w") as f:
            print(f"Generating details page for {target}")
            f.write("---\nhide:\n  - navigation\n---\n")
            f.write(f"# {target}\n\n")
            f.write(f"File description: {metadata.static_site__description}\n\n")
            f.write(f"Document status: {generate_badge(metadata.static_site__document_status, True)}\n\n")
            f.write(f"??? \"Digital Digest\"\n\n")
            f.write(f"\tSource file hash: `{src_checksum}`\n\n")
            f.write(f"\tCompiled at: `{compiled_at}`\n")
            f.write(f"[Download :material-download:](https://shingzhanho.github.io/HKU-Notes/files/{target}/{target}.pdf)")
            f.write("{.md-button .md-button--primary}\n")
            f.write(f"[View source :material-github:](https://github.com/ShingZhanho/HKU-Notes/tree/master/src/{target})")
            f.write("{.md-button}\n")
            f.write(f"\n\n")
            f.write(custom_md_content)

    # generate course catalogue page
    with open("./site/docs/downloads/index.md", "w") as f:
        print("Generating course catalogue page")
        f.write("---\nhide:\n  - navigation\n---\n")
        f.write(f"# Course Catalogue\n\n")
        f.write("All materials are sorted by course code. Use the navigation panel to jump to the course you want.\n\n")
        for alpha in alpha_groups:
            if len(alpha_groups[alpha]) == 0:
                continue
            if alpha == "#" and len(alpha_groups[alpha]["Miscellaneous"]) == 0:
                continue
            f.write(f"## {alpha}\n\n")
            for course_code in alpha_groups[alpha]:
                f.write(f"### {course_code}\n\n")
                f.write("| Material Name | Description | Compiled At | Status |\n")
                f.write("| --- | --- | --- | :-: |\n")
                for target in alpha_groups[alpha][course_code]:
                    compiled_at = ""
                    with open(f"./gh-out/files/{target}/compiled-at.txt", "r") as f2:
                        compiled_at = f2.read().strip().replace("UTC+8 (Hong Kong)", "")
                    description = ""
                    metadata_reader = Reader(f"./src/{target}/metadata.json", target)
                    metadata = metadata_reader.parse()
                    description = metadata.static_site__description
                    document_status = metadata.static_site__document_status
                    status_badge = generate_badge(document_status, False)
                    f.write(f"| [{target}](./details/{target}.md) | {description} | {compiled_at} | {status_badge} |\n")
                f.write("\n\n")
            f.write("\n\n")

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
        "unk": "material-help",
    }
    status_icon = status_icons.get(status, "material-alert-octagon")

    status_descs = {
        "sre": "This is a stable release of the document.",
        "wip": "This document is still under editing and is incomplete.",
        "lts": "This is a long-term support document.",
        "abd": "This document is no longer being updated and is incomplete.",
        "obs": "This document is now deprecated.",
        "unk": "The status of this document is unknown.",
    }
    status_desc = status_descs.get(status, "An error happened during the website generation process.")

    static_hrefs = {
        "sre": "stable-release",
        "wip": "work-in-progress",
        "lts": "long-term-support",
        "abd": "abandoned",
        "obs": "obsolete",
        "unk": "unknown-status",
    }
    static_href = static_hrefs.get(status, "error")
    static_href = "../document-status.md#" + static_href if is_detail_page else "document-status.md#" + static_href

    return """<span class=\"status-badge\">
    <span class=\"status-badge__icon\">:{% status-icon %}:</span>
    <span class=\"status-badge__text\">[{% status-name %}]({% status-href %} \"{% status-desc %} Click for more details.\")</span>
    </span>""".replace("{% status-icon %}", status_icon).replace("{% status-name %}", status.upper()).replace("{% status-href %}", static_href).replace("{% status-desc %}", status_desc).replace("\n", "")

if __name__ == "__main__":
    main()
