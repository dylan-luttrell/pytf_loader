from cgi import parse_header
from collections import defaultdict
from io import StringIO, TextIOWrapper
from re import match as re_match, compile as re_compile
from header_parsers import _parse_module_header, _parse_resource_header
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

def _convert_value_type(value: str) -> str:

    if value.replace('.', '', 1).replace('-', '', 1).isnumeric():
        return float(value) if '.' in value else int(value)
    elif value[0] in ['"', "'"] and value[-1] == value[0]:
        return value[1:-1]
    elif value[0] == '[' and value[-1] == ']':
        return list(value[1:-1].split(','))
    elif value[0] == '{' and value[-1] == '}':
        return _parse_terraform_map(value[1:-1])
    
    return value.replace(NEW_LINE_SUBSTITUTE, NEW_LINE)

KEYS = set()


def _grab_block(file: TextIOWrapper) -> str:
    braces = 1
    squares = 0
    parenthases = 0
    block = ""
    while braces > 0:
        line = next(file)
        line = comment_pattern.sub("", line).strip()
        if len(line.strip()) == 0:
            continue
        braces += line.count("{") - line.count("}")
        squares += line.count("[") - line.count("]")
        parenthases += line.count("(") - line.count(")")

        block += f"{line}"
        if braces > 1 or squares > 0 or parenthases > 0:
            # consulidate nested blocks into single line for easier parsing later
            block += NEW_LINE_SUBSTITUTE
        else:
            block += '\n'
    # clean up block consulidating syntax
    block = block.replace('{' + NEW_LINE_SUBSTITUTE, '{').replace(NEW_LINE_SUBSTITUTE + '}', '}')
    # print(block)
    # exit()
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
            
    # braces = 1
    # cur_key = ""
    # key_value_pairs = defaultdict(str)

    # while braces > 0:
    #     line = next(file)
    #     line = comment_pattern.sub("", line).strip()
    #     if len(line) == 0:
    #         continue
    #     braces += line.count("{") - line.count("}")

    #     if line == "}":
    #         break
        
    #     tokens = line.split("=", maxsplit=1)
    #     if len(tokens) == 2:
    #         cur_key = tokens[0].strip()
    #         KEYS.add(cur_key)

    #     key_value_pairs[cur_key] += tokens[-1].strip()

    # convert values into an appropriate type and return as a dictionary
    return {key: _convert_value_type(value)
            for key, value
            in key_value_pairs.items()
            }


_header_parser = {
    "module": _parse_module_header,
    "resource": _parse_resource_header
}

def parse_blocks(filename: Path | str, block_type: str, name_filter: str | None = None) -> list[dict[str, str]]:
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

            data = parse_header(line)

            if name_filter and not re_match(name_filter, data["name"]):
                # ignore module if does not match filter
                continue


            data.update(_parse_tf_block(file))

            lst_output.append(data)
    
    return lst_output
