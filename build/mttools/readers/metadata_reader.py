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
        
        # Determine version: first check $schema, then fall back to @metadata_file_version
        version = None
        
        # Try to detect version from $schema field (v2 format)
        schema_match = re.search(r'"\$schema"\s*:\s*"([^"]+)"', metadata_str)
        if schema_match:
            schema_url = schema_match.group(1)
            # Check if it's the v2 schema
            if 'schemas/v2.json' in schema_url:
                version = "2"
        
        # Fall back to @metadata_file_version field (v1 and legacy v2 format)
        if version is None:
            version_match = re.search(r'"@metadata_file_version"\s*:\s*"([^"]+)"', metadata_str)
            if version_match:
                version = version_match.group(1)
        
        # If no version indicator found, raise an error
        if version is None:
            raise ValueError(
                "Metadata file version could not be determined. "
                "Please include either '$schema' field (v2) or '@metadata_file_version' field (v1)."
            )

        # select the appropriate parser based on the version
        if version == "1":
            from .metadata_v1_parser import MetadataV1Parser as Parser
        elif version == "2":
            from .metadata_v2_parser import MetadataV2Parser as Parser
        else:
            raise ValueError(f"Unsupported metadata file version: {version}")
        
        # create the parser object
        parser = Parser(metadata_str, self.build_target)
        # parse the metadata and return the metadata object
        metadata = parser.parse()
        return metadata
        