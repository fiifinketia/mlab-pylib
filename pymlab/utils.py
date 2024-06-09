import os
import subprocess

def parse_list(value):
    # Check if the value is a list
    if value.startswith('[') and value.endswith(']'):
        # Remove brackets
        value = value[1:-1]
        result = []
        nested_level = 0
        start = 0

        # Iterate through characters in the value
        for i, char in enumerate(value):
            if char == '[':
                nested_level += 1
            elif char == ']':
                nested_level -= 1
            elif char == ',' and nested_level == 0:
                # Split at the top level commas
                result.append(parse_list(value[start:i]))
                start = i + 1

        # Add the last part after the last comma (or whole value if no commas)
        result.append(parse_list(value[start:]))

        return result
    else:
        # If it's not a list, return the value itself
        return convert_type(value)

def convert_type(value):
    # Convert string to appropriate type
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return str(value)

def fetch_parameters(config_path):
    parameters = {}
    with open(config_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 4 and parts[0] == 'PARAM':
                param_name = parts[1]
                param_type = parts[2]
                param_value = ' '.join(parts[3:])

                if param_type.startswith('list'):
                    # If it's a list type, parse the value accordingly
                    parameters[param_name] = parse_list(param_value)
                else:
                    if param_type == 'int':
                        parameters[param_name] = int(param_value)
                    elif param_type == 'float':
                        parameters[param_name] = float(param_value)
                    elif param_type == 'bool':
                        parameters[param_name] = param_value.lower() == 'true'
                    else:
                        parameters[param_name] = str(param_value)

    return parameters

def run_in_dir(directory: str, commands: list[str]) -> None:
    os.chdir(directory)
    for command in commands:
        subprocess.run(command, shell=True, check=True)


def make_file(result_id: str, file_name: str, content: str | None = None):
    """Create a file with the given content."""
    file_path = f"results/{result_id}/{file_name}"
    if not os.path.exists(f"results/{result_id}"):
        os.makedirs(f"results/{result_id}")
    with open(file_path, "w") as f:
        if content is not None:
            f.write(content)
        else :
            f.write("")
    return file_path

def clean_files(result_id: str):
    """Remove all files in the result directory."""
    result_dir = f"results/{result_id}"
    if not os.path.exists(result_dir):
        return
    for file_name in os.listdir(result_dir):
        file_path = os.path.join(result_dir, file_name)
        os.remove(file_path)