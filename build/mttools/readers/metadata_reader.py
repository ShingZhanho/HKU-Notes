from ..metadata import Metadata
import re

class Reader:
    """
    Wrapper class for reading metadata files.
    """
    def __init__(self, metadata_file, build_target=None):
        """
        Initialize the reader with a metadata file.
        """
        self.metadata_file = metadata_file
        if build_target is None:
            # if no build target is provided, set name as parent dir of the metadata file
            self.build_target = metadata_file.split('/')[-2]
        else:
            self.build_target = build_target
        
    def parse(self) -> Metadata:
        """
        Parse the metadata file and return a metadata object.
        """
        # Read the metadata file
        with open(self.metadata_file, 'r') as file:
            metadata_str = file.read()
        # use regex to find the metadata file version
        # format: "@metadata_file_version": "<ver>", ...
        # if not found, raise an error
        match = re.search(r'"@metadata_file_version"\s*:\s*"([^"]+)"', metadata_str)
        if not match:
            raise ValueError("Metadata file version not found.")
        version = match.group(1)

        # select the appropriate parser based on the version
        if version == "1":
            from .metadata_v1_parser import MetadataV1Parser as Parser
        else:
            raise ValueError(f"Unsupported metadata file version: {version}")
        
        # create the parser object
        parser = Parser(metadata_str, self.build_target)
        # parse the metadata and return the metadata object
        metadata = parser.parse()
        return metadata
        