import os
import shutil
import random
from mttools import Metadata, Reader
from .utils import write_front_matters, get_last_modified_time_hkt
from .authors_resolver import resolve_authors, get_author_cards, write_authors_section
from .status_badge import get_badge_str
from .pdf_preview import generate_pdf_viewer_html

def gen_details_page(target: str, metadata: Metadata, all_targets: dict[str, dict[str, list[str]]]):
    print(f"Generating details page for target: {target}")

    if metadata.computed.is_alias.get():
        print(f"Skipping alias target: {target}")
        return
    
    # Prepare output file path
    out_file = f"./site/docs/downloads/details/{target}.md"
    f = open(out_file, "w", encoding="utf-8")
    print(f"Writing details page to: {out_file}")

    # Prepare front matter data
    front_matter = {
        "hide": [
            "navigation",
        ],
        "description": metadata.static_site.meta_description.get() or \
            f"Download {target} for free - {metadata.static_site.description.get()}",
        "comments": True,
    }
    write_front_matters(f, front_matter)
    print("Front matter written.")

    # Write target information
    __write_target_info(f, target, metadata)
    print("Target information written.")

    # Write authors section
    resolved_authors = resolve_authors(metadata.authors.get())
    if len(resolved_authors) == 0:
        raise Exception(f"No authors found for target: {target}")
    author_cards = get_author_cards(resolved_authors)
    write_authors_section(f, author_cards)
    print("Authors section written.")

    # Writ buttons
    f.write('\n\n<p></p>\n<div class="author-card-container" markdown="1">\n')
    f.write('<span>Action(s):</span>\n')
    for button in metadata.static_site.buttons.get():
        f.write(__generate_button_md(
            button.is_primary.get(),
            button.text.get(),
            button.href.get(),
            button.icon.get(),
            button.message.get()
        ))
        f.write("\n")
    f.write("\n</div>\n\n")
    print("Buttons written.")

    # Move PDF preview pngs (if any) - MUST be done before generating PDF viewer HTML
    if metadata.output_file.get().endswith(".pdf"):
        os.makedirs(
            f"./site/docs/downloads/details/{target}~preview",
            exist_ok=True
        )
        for file in os.listdir(f"./gh-out/files/{target}/~preview"):
            shutil.copy2(
                f"./gh-out/files/{target}/~preview/{file}",
                f"./site/docs/downloads/details/{target}~preview/{file}"
            ) if file.endswith(".png") else None
        shutil.rmtree(f"./gh-out/files/{target}/~preview")
        print("PDF preview images moved.")

    # Prepare PDF viewer section
    pdf_viewer_html = ""
    if metadata.output_file.get().endswith(".pdf") and metadata.static_site.pdf_viewer.get() != "hidden":
        pdf_viewer_html = generate_pdf_viewer_html(target)

    # Write customised content
    parsed_content = __read_and_process_custom_md(
        f"./src/{target}/{metadata.static_site.custom_md_file.get()}" if metadata.static_site.custom_md_file.get() else "",
        pdf_viewer_html,
        metadata.static_site.pdf_viewer.get()
    )
    f.write(parsed_content)
    print("Custom markdown content written.")

    # Write "See also" section
    __write_see_also_section(f, target, all_targets)
    print("See also section written.")

    f.close()
    print(f"Details page generation for target {target} completed.")

def __write_target_info(file_obj, target: str, metadata: Metadata):
    f = file_obj
    ## Heading
    f.write(f"# {target}\n\n")

    ## Information
    f.write(f"**File description:** {metadata.static_site.description.get()}\n\n")
    f.write(f"**Document status:** {get_badge_str(metadata.static_site.document_status.get(), True)}\n\n")
    f.write(f"**Last modified:** {get_last_modified_time_hkt(target)}\n\n")

def __generate_button_md(primary: bool, text: str, href: str, icon: str | None = None, message: str | None = None) -> str:
    return "".join((
        f"[{text}",
        f" :{icon}:" if icon else "",
        f"]({href}",
        f' "{message}"' if message else "",
        ")",
        "{.md-button ",
        ".md-button--primary" if primary else "",
        "}",
    ))
    
def __read_and_process_custom_md(file_path: str, pdf_viewer_html: str, pdf_viewer_mode: str) -> str:
    if file_path == "" or file_path is None:
        return "".join(["\n\n", pdf_viewer_html, "\n\n"])
    
    lines: list[str] = []
    flag_pdf_tag_found = False
    PDF_TAG = "<!-- % PDF_VIEWER % -->"

    with open(file_path, "r", encoding="utf-8") as f:
        while (line := f.readline()) != "":
            if pdf_viewer_mode != "at_tag":
                lines.append(line)
            else:
                if PDF_TAG in line:
                    lines.append(line.replace(PDF_TAG, pdf_viewer_html))
                    flag_pdf_tag_found = True
                else:
                    lines.append(line)

    if pdf_viewer_mode == "at_tag" and not flag_pdf_tag_found:
        print(f"Did not find PDF viewer tag in the custom markdown file: {file_path}.")
        raise Exception("PDF viewer tag not found.")
    
    if pdf_viewer_mode == "at_head":
        lines = [pdf_viewer_html, "\n\n"] + lines

    if pdf_viewer_mode == "at_footer":
        lines = lines + ["\n\n", pdf_viewer_html]

    return "".join(lines)

def __write_see_also_section(file_obj, target: str, all_targets: dict[str, dict[str, list[str]]]):
    f = file_obj
    f.write("\n\n## See also\n\n")

    see_also_targets = []

    # first select targets with the same course code
    course_code = ""
    if len(target) >= 9 and target[:4].isalpha() and target[4:8].isdigit():
        course_code = target[:8]
        alphabet = course_code[0]
        if alphabet in all_targets and course_code in all_targets[alphabet]:
            see_also_targets = [
                t for t in all_targets[alphabet][course_code]
                if t != target and not Reader(f"./src/{t}/metadata.json", t).parse().computed.is_alias.get()
            ]
    
    # then fill up with other targets if needed
    if len(see_also_targets) < 6:
        additional_targets = []
        selected_set = set(see_also_targets + [target])
        for alpha in all_targets.keys():
            for course in all_targets.get(alpha).keys():
                for t in all_targets.get(alpha).get(course):
                    if t not in selected_set and not Reader(f"./src/{t}/metadata.json", t).parse().computed.is_alias.get():
                        additional_targets.append(t)
        random.shuffle(additional_targets)
        see_also_targets.extend(additional_targets[:6 - len(see_also_targets)])
    
    # truncate to 6 targets
    see_also_targets = see_also_targets[:6]
    
    # write see also cards
    f.write('<div class="grid cards" markdown>\n\n')
    for t in see_also_targets:
        metadata = Reader(f"./src/{t}/metadata.json", t).parse()
        f.write(__generate_see_also_card(t, metadata))
    f.write('</div>\n\n')
    
def __generate_see_also_card(target: str, metadata: Metadata) -> str:
    return "".join((
        f"-   :material-file-document:{{ .lg .middle }} __{target}__\n\n",
        f"    ---\n\n",
        f"    {metadata.static_site.description.get()}\n\n",
        f"    [Check out the document :octicons-arrow-right-24:](./{target}.md)\n\n"
    ))