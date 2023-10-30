from pathlib import Path
from ._shared import parse_blocks

BLOCK_TYPE = "data" 

def parse_data_blocks(filename: Path | str, name_filter: str | None = None, type_filter: list[str] | None = None) -> list[dict[str, str]]:
    """
    Parse a Terraform file and extract data information based on the provided type filter.

    Args:
        filename (Path | str): The path or name of the Terraform file to parse.
        type_filter (list[str] | None, optional): A list of data types to filter. Defaults to None.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the parsed data information.
    """

    lst_output = parse_blocks(filename, BLOCK_TYPE, name_filter)


    
    return [res for res in lst_output if type_filter is None or res["data_type"] in type_filter]


