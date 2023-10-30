from pathlib import Path
from ._shared import parse_blocks


BLOCK_TYPE = "module"



resources = []

def _parse_module_header(header: str) -> str:
    parts = header.split(" ")

    module_name = parts[1].strip("\"")
    
    return module_name

# comment_pattern = re_compile(r"#.*")

# KEYS = set()

# def _parse_module(file: TextIOWrapper) -> dict[str, str]:
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

     

def parse_module_blocks(filename: Path | str, module_name_filter: str | None = None) -> list[dict[str, str]]:
    """
    Parse a Terraform file and extract module information based on the provided name filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        modile_name_filter (str | None, optional): A regular expression to filter module names. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed resource information.
    """

    lst_output = parse_blocks(filename, BLOCK_TYPE, module_name_filter)
    
    return lst_output