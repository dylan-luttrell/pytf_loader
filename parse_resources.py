#!/usr/bin/env python

from collections import defaultdict
from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from pprint import pprint
import re
import csv
from sys import stdout
import json
import yaml
from _shared import parse_blocks


BLOCK_TYPE = "resource"
FILES = ["../example.tf"]

# @dataclass
# class Resource:
#     type: str
#     to_port: int
#     from_port: int
#     protocol: str
#     cidr_blocks: list | None = None
#     security_groups: list | None = None
#     prefix_list_ids: list | None = None
#     self: bool = False
#     description: str | None = None


resources = []

def _parse_resource_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    res_type = parts[1].strip("\"")
    res_name = parts[2].strip("\"")
    
    return {"resource_type":res_type, "name": res_name}

comment_pattern = re.compile(r"#.*")

KEYS = set()

# def _parse_resource(file: TextIOWrapper) -> dict[str, str]:
#     """
#     Parses a resource file and returns a dictionary containing key-value pairs.

#     Args:
#         file (TextIOWrapper): A file object representing the resource file to be parsed.

#     Returns:
#         dict[str, str]: A dictionary containing key-value pairs parsed from the resource file.
#     """
#     braces = 1
#     cur_key = ""
#     output = defaultdict(str)

#     while braces == 1:
#         line = next(file)
#         line = comment_pattern.sub("", line).strip()
#         if len(line) == 0:
#             continue
#         braces += line.count("{") - line.count("}")

#         if line == "}":
#             break
        
#         tokens = line.split("=")

#         if len(tokens) == 2:
#             cur_key = tokens[0].strip()
#             KEYS.add(cur_key)

#         output[cur_key] += tokens[-1].strip()

#     return output

     

def parse_resource_blocks(filename: Path | str, name_filter: str | None = None, type_filter: list[str] | None = None) -> list[dict[str, str]]:
    """
    Parse a Terraform file and extract resource information based on the provided type filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        type_filter (list[str] | None, optional): A list of resource types to filter. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed resource information.
    """

    lst_output = parse_blocks(filename, BLOCK_TYPE, name_filter)

    # with open(filename, mode = "r", encoding="utf-8") as file:

    #     while True:
    #         try:
    #             line = next(file)
    #         except StopIteration:
    #             break

    #         if not line.lstrip().startswith(BLOCK_TYPE):
    #             continue

    #         data = _parse_resource_header(line)
                
    #         if type_filter and data["resource_type"] not in type_filter:
    #             # ignore resource if does not match filter
    #             continue

    #         data.update(_parse_tf_block(file))

    #         lst_output.append(data)

    
    return [res for res in lst_output if res["resource_type"] in type_filter]

# pprint(parse_tf_file(FILES[0]) or "")

if __name__ == "__main__":
    data = parse_resource_blocks(FILES[0], type_filter=["aws_security_group_rule"])
    print(yaml.dump(data))

# keys = to_csv[0].keys()
# if __name__ == "__main__":
#     # with open('people.csv', 'w', newline='') as output_file:
#     keys = ["resource_type", "resource_name", "type", "from_port", "to_port", "protocol", "security_group_id", "prefix_list_ids", "description"]

#     dict_writer = csv.DictWriter(stdout, keys, extrasaction="ignore")
#     dict_writer.writeheader()
#     dict_writer.writerows(to_csv)