import json
from ..metadata2 import Metadata2

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
        self.parsed_obj = Metadata2(build_target)

    def parse(self) -> Metadata2:
        """
        Parse the JSON string and return a Metadata2 object.
        """
        pass # implemented in subclasses