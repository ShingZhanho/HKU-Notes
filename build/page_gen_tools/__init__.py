# page_gen_tools module
# This module provides tools for generating pages.
# The functions in here should be used by generate_pages.py only.

import os
import shutil
from .utils import get_targets_dict
from .gen_details_page import gen_details_page
from .gen_catalogue_page import gen_catalogue_page
from mttools import Reader, Metadata2

def start(targets: list[str], out_dir: str | None = None):
    out_dir = out_dir or "./site/docs/downloads"
    print("Page generation started...")
    print(f"Writing output to {out_dir}")

    targets_dict = get_targets_dict(targets)
    print("Parsed targets:", targets_dict)

    # generate details pages
    details_output_dir = os.path.join(out_dir, "details")
    os.makedirs(details_output_dir, exist_ok=True)
    print("Generating details pages...")
    print("Writing outputs to", details_output_dir)

    for target in targets:
        metadata: Metadata2 = Reader(f"./src/{target}/metadata.json", target).parse()
        gen_details_page(target, metadata, targets_dict)

        # post-page-generation file handling
        if os.path.exists(f"./src/{target}/.COPY"):
            print(f"Copying .COPY files for target: {target}")
            os.makedirs(f"./site/docs/downloads/{target}", exist_ok=True)
            shutil.copytree(
                f"./src/{target}/.COPY",
                f"./site/docs/downloads/{target}",
                dirs_exist_ok=True,
                copy_function=shutil.copy2,
                symlinks=False
            )
    print("Details pages generation completed.")

    # generate catalogue page
    print("Generating catalogue page...")

    gen_catalogue_page(targets_dict)

    print("Page generation completed.")