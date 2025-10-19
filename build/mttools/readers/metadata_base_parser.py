import json
from ..metadata import Metadata

class MetadataParserBase:
    """
    Base class for metadata parsers.
    """
    
    def __init__(self, json_str: str, build_target: str):
        """
        Initialise the parser.
        """
        self.json_str = json_str
        self.json_obj = json.loads(json_str)
        self.parsed_obj = Metadata(build_target)

    def parse(self) -> Metadata:
        """
        Parse the JSON string and return a Metadata object.
        """
        pass # implemented in subclasses