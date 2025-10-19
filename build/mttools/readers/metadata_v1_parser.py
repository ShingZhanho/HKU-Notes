from .metadata_base_parser import MetadataParserBase
from ..metadata2 import Metadata2

class MetadataV1Parser(MetadataParserBase):
    """
    Parser for version 1 of the metadata file.
    """
    def __init__(self, metadata_file, build_target):
        """
        Initialize the parser with a metadata file.
        """
        super().__init__(metadata_file, build_target)

    def parse(self) -> Metadata2:
        # Top-level keys
        self.parsed_obj.root_file.set_if(
            self.json_obj.get("build", {}).get("root_file"),
            lambda x: x is not None
        )
        self.parsed_obj.output_file.set_if(
            self.json_obj.get("build", {}).get("output_file"),
            lambda x: x is not None
        )

        # "build" sub-keys
        self.parsed_obj.build.requires.set_if(
            self.json_obj.get("build", {}).get("requires"),
            lambda x: x is not None
        )
        self.parsed_obj.build.no_latex.set_if(
            self.json_obj.get("build", {}).get("no_latex"),
            lambda x: x is not None
        )
        self.parsed_obj.build.prebuild_command.set_if(
            self.json_obj.get("build", {}).get("prebuild_command"),
            lambda x: x is not None
        )
        # build_command has a computed default based on root_file
        self.parsed_obj.build.build_command.set_if_else(
            self.json_obj.get("build", {}).get("build_command"),
            lambda x: x is not None,
            f"latexmk -pdf -f -interaction=nonstopmode -cd -outdir=. ./{self.parsed_obj.root_file.get()}"
        )
        self.parsed_obj.build.postbuild_command.set_if(
            self.json_obj.get("build", {}).get("postbuild_command"),
            lambda x: x is not None
        )
        self.parsed_obj.build.miktex_package_file.set_if(
            self.json_obj.get("build", {}).get("miktex_package_file"),
            lambda x: x is not None
        )

        # "static_site" keys
        self.parsed_obj.static_site.description.set_if_else(
            self.json_obj.get("static_site", {}).get("description"),
            lambda x: x is not None,
            "-"
        )
        self.parsed_obj.static_site.meta_description.set_if(
            self.json_obj.get("static_site", {}).get("meta_description"),
            lambda x: x is not None
        )
        self.parsed_obj.static_site.custom_md_file.set_if_else(
            self.json_obj.get("static_site", {}).get("custom_md_file"),
            lambda x: x is not None,
            ""
        )
        self.parsed_obj.static_site.document_status.set_if_else(
            self.json_obj.get("static_site", {}).get("document_status"),
            lambda x: x is not None,
            "unk"
        )
        self.parsed_obj.static_site.alias_to.set_if(
            self.json_obj.get("static_site", {}).get("alias_to"),
            lambda x: x is not None
        )
        self.parsed_obj.static_site.pdf_viewer.set_if(
            self.json_obj.get("static_site", {}).get("pdf_viewer"),
            lambda x: x is not None
        )

        # "static_site" > "primary_button" keys
        self.parsed_obj.static_site.primary_button.disabled.set_if(
            self.json_obj.get("static_site", {}).get("primary_button", {}).get("disabled"),
            lambda x: x is not None
        )
        self.parsed_obj.static_site.primary_button.text.set_if_else(
            self.json_obj.get("static_site", {}).get("primary_button", {}).get("text"),
            lambda x: x is not None,
            "Download"
        )
        self.parsed_obj.static_site.primary_button.icon.set_if_else(
            self.json_obj.get("static_site", {}).get("primary_button", {}).get("icon"),
            lambda x: x is not None,
            "material-download"
        )
        self.parsed_obj.static_site.primary_button.href.set_if_else(
            self.json_obj.get("static_site", {}).get("primary_button", {}).get("href"),
            lambda x: x is not None,
            f"https://hku.jacobshing.com/files/{self.parsed_obj.name.get()}/{self.parsed_obj.output_file.get()}"
        )

        # "static_site" > "secondary_button" keys
        self.parsed_obj.static_site.secondary_button.disabled.set_if(
            self.json_obj.get("static_site", {}).get("secondary_button", {}).get("disabled"),
            lambda x: x is not None
        )
        self.parsed_obj.static_site.secondary_button.text.set_if_else(
            self.json_obj.get("static_site", {}).get("secondary_button", {}).get("text"),
            lambda x: x is not None,
            "View source"
        )
        self.parsed_obj.static_site.secondary_button.icon.set_if_else(
            self.json_obj.get("static_site", {}).get("secondary_button", {}).get("icon"),
            lambda x: x is not None,
            "material-github"
        )
        self.parsed_obj.static_site.secondary_button.href.set_if_else(
            self.json_obj.get("static_site", {}).get("secondary_button", {}).get("href"),
            lambda x: x is not None,
            f"https://github.com/ShingZhanho/HKU-Notes/tree/master/src/{self.parsed_obj.name.get()}"
        )

        # "authors" keys
        self.parsed_obj.authors.set_if_else(
            self.json_obj.get("authors"),
            lambda x: x is not None,
            ["jacob_shing"]
        )

        return self.parsed_obj