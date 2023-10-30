from cgi import parse_header
from collections import defaultdict
from io import StringIO, TextIOWrapper
from re import match as re_match, compile as re_compile
from typing import Any
from .header_parsers import _parse_data_header, _parse_module_header, _parse_resource_header
from pathlib import Path

# market to indicate new line in nested block
NEW_LINE_SUBSTITUTE = '\0'
NEW_LINE = '\n'

comment_pattern = re_compile(r"#.*")

def _parse_terraform_map(map_str: str) -> dict[str, str]:
    # return {kv_pair.split("=", 1)[0].strip(): _convert_value_type(kv_pair.split("=", 1)[1].strip()) 
            
    #         for kv_pair in kv_pairs}
    output = {}
    for pair in map_str.split(NEW_LINE_SUBSTITUTE):
        key, value = pair.split("=", 1)
        output[key.strip()] = _convert_value_type(value.strip())
    
    return output

def _convert_value_type(value: str) -> Any:
    """
    Convert the given value to the appropriate data type.

    Args:
        value (str): The value to be converted.

    Returns:
        Any: The converted value.

    """
    # Check if the value is a numeric string
    if value.replace('.', '', 1).replace('-', '', 1).isnumeric():
        return float(value) if '.' in value else int(value)
    
    # Check if the value is a string enclosed in quotes
    elif value[0] in ['"', "'"] and value[-1] == value[0]:
        return value[1:-1]
    
    # Check if the value is a list
    elif value[0] == '[' and value[-1] == ']':
        return list(value[1:-1].split(','))
    
    # Check if the value is a map
    elif value[0] == '{' and value[-1] == '}':
        return _parse_terraform_map(value[1:-1])
    
    # Revert temporary line substitution back to new line
    return value.replace(NEW_LINE_SUBSTITUTE, NEW_LINE)

KEYS = set()


def _grab_block(file: TextIOWrapper) -> str:
    """
    This function reads a file and grabs a block of code enclosed in braces.
    
    Args:
        file (TextIOWrapper): The file object to read from.
        
    Returns:
        str: The grabbed block of code as a string.
    """
    braces = 1
    squares = 0
    parenthesis = 0
    block = ""
    while braces > 0:
        line = next(file)
        # strip comments from line
        line = comment_pattern.sub("", line).strip()
        # skip if line is empty
        if len(line) == 0:
            continue

        # count nested block markers
        braces += line.count("{") - line.count("}")
        squares += line.count("[") - line.count("]")
        parenthesis += line.count("(") - line.count(")")

        block += f"{line}"
        if braces > 1 or squares > 0 or parenthesis > 0:
            # substitute new line in nested blocks for easier parsing
            block += NEW_LINE_SUBSTITUTE
        else:
            block += '\n'
    # clean up block consulidating syntax
    block = block.replace('{' + NEW_LINE_SUBSTITUTE, '{').replace(NEW_LINE_SUBSTITUTE + '}', '}')

    # remove final curly brace and return
    return block.strip('}\n')

def _parse_tf_block(file: TextIOWrapper) -> dict[str, str]:
    """
    Parses a Terraform block and returns a dictionary containing key-value pairs.

    Args:
        file (TextIOWrapper): A file object representing the Terraform file to be parsed.

    Returns:
        dict[str, str]: A dictionary containing key-value pairs parsed from the resource file.
    """
    block = StringIO(_grab_block(file))
 
    key_value_pairs = defaultdict(str)
    tokens = [None]
    cur_key = None
    for line in block.readlines():
        line = comment_pattern.sub("", line).strip()
        if len(line) == 0:
            continue
        tokens = line.split("=", maxsplit=1)

        cur_key = tokens[0].strip()
        KEYS.add(cur_key)
        key_value_pairs[cur_key] += tokens[-1].strip()


    # convert values into an appropriate type and return as a dictionary
    return {key: _convert_value_type(value)
            for key, value
            in key_value_pairs.items()
            }


_header_parser = {
    "module": _parse_module_header,
    "resource": _parse_resource_header,
    "data": _parse_data_header
}

def parse_blocks(filename: Path | str, block_type: str, name_filter: str | None = None) -> list[dict[str, Any]]:
    """
    Parse a Terraform file and extract resource information based on the provided type filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        type_filter (list[str] | None, optional): A list of resource types to filter. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed resource information.
    """

    lst_output = []

    parse_header = _header_parser[block_type]

    with open(filename, mode = "r", encoding="utf-8") as file:

        while True:
            try:
                line = next(file).strip()
                # strip comments from line
                line = comment_pattern.sub("", line).strip()
            except StopIteration:
                break

            if not (line.startswith(block_type) and line.endswith("{")):
                # if line not a block of type given, skip
                continue

            data: dict[str, Any] = parse_header(line)

            if name_filter and not re_match(name_filter, data["name"]):
                # ignore module if does not match filter
                continue


            data["arguments"] = _parse_tf_block(file)

            lst_output.append(data)
    
    return lst_output
