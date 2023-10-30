from pathlib import Path
import re
from ._shared import parse_blocks


BLOCK_TYPE = "resource"

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


    
    return [res for res in lst_output if type_filter is None or res["resource_type"] in type_filter]


