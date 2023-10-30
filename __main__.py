import argparse

import yaml
from . import parse_module_blocks
from . import parse_resource_blocks
from pathlib import Path

BLOCK_TYPES = ["module", "resource"]



parser = argparse.ArgumentParser()

parser.add_argument("files", type=str, nargs="+", help="file or file glob to parse")
parser.add_argument("-t", "--type", required=False, type=str, default="all", help="type of block to parse. Seperate multiple values with commas. Defaults to all.")

args = parser.parse_args()

file_list = [Path(file) for file in args.files]
block_types = BLOCK_TYPES if args.type == "all" else args.type.split(",")


data = {str(file): dict() for file in file_list}
for file in file_list:
    file_data = data[str(file)]
    if "module" in block_types:
        file_data["modules"] = parse_module_blocks(file)
    if "resource" in block_types:
        file_data["resources"] = parse_resource_blocks(file)


print(yaml.dump(data, sort_keys=True))
