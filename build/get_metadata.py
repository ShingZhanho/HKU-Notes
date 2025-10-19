# get-metadata.py
# This script takes two arguments:
#   1. The metadata.json file to read
#   2. The key to extract and print

import inspect
import mttools
import sys

def get_value_from_metadata(metadata, key):
    """
    Extract a value from the Metadata object using a key path with dot notation.
    
    Examples:
        - "name" -> metadata.name
        - "build.requires" -> metadata.build.requires
        - "static_site.primary_button.text" -> metadata.static_site.primary_button.text
        - "computed.is_pdf_target" -> metadata.computed.is_pdf_target
    """
    # Split the key by . to handle nested attributes
    parts = key.split(".")
    
    # Navigate through the nested structure
    current_obj = metadata
    for part in parts:
        if not hasattr(current_obj, part):
            return None
        current_obj = getattr(current_obj, part)
    
    # Check if we got a Value object (has a .get() method)
    if hasattr(current_obj, 'get') and callable(current_obj.get):
        return current_obj.get()
    
    # Check if we got a bound method (for computed values)
    if inspect.ismethod(current_obj):
        return current_obj()
    
    # Otherwise return the object itself
    return current_obj

if __name__ == "__main__":
    # get parameters from command line
    metadata_file = sys.argv[1]
    key = sys.argv[2]

    # read the metadata file
    reader = mttools.Reader(metadata_file)
    metadata = reader.parse()

    # get the value
    value = get_value_from_metadata(metadata, key)
    
    # handle None values
    if value is None:
        value = ""
    
    # format the value by type
    if type(value) == type([]):
        # an array
        # print each element on a new line
        for item in value:
            print(item)
    elif type(value) == bool:
        # a boolean
        # print lowercase "true" or "false" for matching GitHub Actions
        print("true" if value else "false")
    else:
        # a string
        # print the value
        print(value)
