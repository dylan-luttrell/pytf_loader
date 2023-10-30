import argparse
from pprint import pprint
from typing import Any

import yaml

from parse_tf.parse_data import parse_data_blocks
from . import parse_module_blocks
from . import parse_resource_blocks
from pathlib import Path

BLOCK_TYPES = ["module", "resource", "data"]

def _consulidate_types(blocks: list[dict[str, Any]], _type: str) -> dict[str, list[Any]]:
    key = {"modules": "source", "resources": "tf_resource_type", "data": "tf_data_type"}[_type]
    output: dict[str, list[Any]] = {block[key]: [] for block in blocks}

    for block in blocks:
        output[block[key]].append(block)
        del block[key]
    return output

parser = argparse.ArgumentParser()

parser.add_argument("files", type=str, nargs="+", help="file or file glob to parse")
parser.add_argument("-t", "--type", required=False, type=str, default="all", help="type of block to parse. Seperate multiple values with commas. Defaults to all.")
parser.add_argument("-g", "--group", required=False, action="store_true", help="group blocks by type/source")
parser.add_argument("-s", "--sort", required=False, action="store_true", help="sort output alphanumerically")

args = parser.parse_args()

file_list = [Path(file) for file in args.files]
block_types = BLOCK_TYPES if args.type == "all" else args.type.split(",")


data = {str(file): dict() for file in file_list}
for file in file_list:
    file_data = data[str(file)]
    if "data" in block_types:
        file_data["data"] = parse_data_blocks(file) or None
    if "module" in block_types:
        file_data["modules"] = parse_module_blocks(file) or None
    if "resource" in block_types:
        file_data["resources"] = parse_resource_blocks(file) or None
    if args.group:
        data[str(file)] = {_type: _consulidate_types(block, _type) for _type, block in file_data.items() if block}


print(yaml.dump(data, sort_keys=args.sort, default_flow_style=False))
