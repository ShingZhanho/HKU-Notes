# get-metadata.py
# This script takes two arguments:
#   1. The metadata.json file to read
#   2. The key to extract and print

import mttools
import sys

if __name__ == "__main__":
    # get parameters from command line
    metadata_file = sys.argv[1]
    key = sys.argv[2]

    # read the metadata file
    reader = mttools.Reader(metadata_file)
    metadata = reader.parse()

    # get the value
    value = getattr(metadata, key, "")
    value = "" if value is None else value
    
    # format the value by type
    if type(value) == type([]):
        # an array
        # print each element on a new line
        for item in value:
            print(item)
    else:
        # a string
        # print the value
        print(value)
