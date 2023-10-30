def _parse_module_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    module_name = parts[1].strip("\"")
    
    return {"name": module_name}

def _parse_resource_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    res_type = parts[1].strip("\"")
    res_name = parts[2].strip("\"")
    
    return {"tf_resource_type":res_type, "tf_resource_name": res_name}

def _parse_data_header(header: str) -> dict[str, str]:
    parts = header.split(" ")

    res_type = parts[1].strip("\"")
    res_name = parts[2].strip("\"")
    
    return {"tf_data_type":res_type, "tf_data_name": res_name}