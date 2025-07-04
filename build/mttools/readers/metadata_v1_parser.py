from .metadata_base_parser import MetadataParserBase
from ..metadata import Metadata

class MetadataV1Parser(MetadataParserBase):
    """
    Parser for version 1 of the metadata file.
    """
    def __init__(self, metadata_file, build_target):
        """
        Initialize the parser with a metadata file.
        """
        super().__init__(metadata_file, build_target)

    def parse(self) -> Metadata:
        self.parsed_obj.root_file = self.json_obj.get("build", {}).get("root_file", self.parsed_obj.root_file)
        self.parsed_obj.output_file = self.json_obj.get("build", {}).get("output_file", self.parsed_obj.output_file)

        self.parsed_obj.build__requires = self.json_obj.get("build", {}).get("requires", None)
        self.parsed_obj.build__prebuild_command = self.json_obj.get("build", {}).get("prebuild_command", None)
        self.parsed_obj.build__build_command = self.json_obj.get("build", {}).get("build_command", self.parsed_obj.build__build_command)
        self.parsed_obj.build__postbuild_command = self.json_obj.get("build", {}).get("postbuild_command", None)
        self.parsed_obj.build__miktex_package_file = self.json_obj.get("build", {}).get("miktex_package_file", self.parsed_obj.build__miktex_package_file)

        # "static_site" keys
        self.parsed_obj.static_site__description = self.json_obj.get("static_site", {}).get("description", "-")
        self.parsed_obj.static_site__custom_md_file = self.json_obj.get("static_site", {}).get("custom_md_file", "")
        self.parsed_obj.static_site__document_status = self.json_obj.get("static_site", {}).get("document_status", "unk")
        self.parsed_obj.static_site__alias_to = self.json_obj.get("static_site", {}).get("alias_to", None)

        # "static_site" > "primary_button" keys
        self.parsed_obj.static_site__primary_button__disabled = self.json_obj.get("static_site", {}).get("primary_button", {}).get("disabled", False)
        self.parsed_obj.static_site__primary_button__text = self.json_obj.get("static_site", {}).get("primary_button", {}).get("text", "Download")
        self.parsed_obj.static_site__primary_button__icon = self.json_obj.get("static_site", {}).get("primary_button", {}).get("icon", "material-download")
        self.parsed_obj.static_site__primary_button__href = self.json_obj.get("static_site", {}).get("primary_button", {}).get("href", self.parsed_obj.static_site__primary_button__href)

        # "static_site" > "secondary_button" keys
        self.parsed_obj.static_site__secondary_button__disabled = self.json_obj.get("static_site", {}).get("secondary_button", {}).get("disabled", False)
        self.parsed_obj.static_site__secondary_button__text = self.json_obj.get("static_site", {}).get("secondary_button", {}).get("text", "View source")
        self.parsed_obj.static_site__secondary_button__icon = self.json_obj.get("static_site", {}).get("secondary_button", {}).get("icon", "material-github")
        self.parsed_obj.static_site__secondary_button__href = self.json_obj.get("static_site", {}).get("secondary_button", {}).get("href", self.parsed_obj.static_site__secondary_button__href)

        # "authors" keys
        self.parsed_obj.authors = self.json_obj.get("authors", [])

        return self.parsed_obj