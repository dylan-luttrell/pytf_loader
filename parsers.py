# This file is a collection of parsers for Terraform block types
from .shared import parse_blocks
from pathlib import Path

def parse_data_blocks(filename: Path | str, name_filter: str | None = None, type_filter: list[str] | None = None) -> list[dict[str, str]]:
    """
    Parse a Terraform file and extract data information based on the provided type filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        type_filter (list[str] | None, optional): A list of data types to filter. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed data information.
    """

    lst_output = parse_blocks(filename, "data", name_filter)
    
    return [res for res in lst_output if type_filter is None or res["tf_data_type"] in type_filter]

def parse_module_blocks(filename: Path | str, module_name_filter: str | None = None) -> list[dict[str, str]]:
    """
    Parse a Terraform file and extract module information based on the provided name filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        modile_name_filter (str | None, optional): A regular expression to filter module names. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed resource information.
    """

    lst_output = parse_blocks(filename, "module", module_name_filter)
    
    return lst_output

def parse_resource_blocks(filename: Path | str, name_filter: str | None = None, type_filter: list[str] | None = None) -> list[dict[str, str]]:
    """
    Parse a Terraform file and extract resource information based on the provided type filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        type_filter (list[str] | None, optional): A list of resource types to filter. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed resource information.
    """

    lst_output = parse_blocks(filename, "resource", name_filter)
    
    return [res for res in lst_output if type_filter is None or res["tf_resource_type"] in type_filter]
