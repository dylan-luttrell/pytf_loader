def _parse_module_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    module_name = parts[1].strip("\"")
    
    return {"module_name": module_name, "source": ""}

def _parse_resource_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    res_type = parts[1].strip("\"")
    res_name = parts[2].strip("\"")
    
    return {"resource_type":res_type, "resource_name": res_name}

def _parse_data_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    res_type = parts[1].strip("\"")
    res_name = parts[2].strip("\"")
    
    return {"data_type":res_type, "data_name": res_name}