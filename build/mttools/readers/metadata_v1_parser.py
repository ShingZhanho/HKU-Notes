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

        return self.parsed_obj