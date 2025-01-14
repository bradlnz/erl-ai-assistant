import json
from colorama import Fore, Style, init

def extract_json_content(text: str) -> dict:
    """
    Extract structured JSON content from a response.

    :param text: A string containing JSON content.
    :return: A dictionary parsed from the extracted JSON content.
    """
    try:
        parsed_json = json.loads(text)
        return parsed_json
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")


def extract_json_content_string(text: str) -> dict:
    """
    Extract JSON content enclosed between ```json and ``` markers.

    :param text: A string containing JSON content within ```json markers.
    :return: A dictionary parsed from the extracted JSON content.
    """
    start_marker = "```json"
    end_marker = "```"
    content = []

    inside_block = False
    for line in text.split("\n"):
        line = line.rstrip()
        if line.startswith(start_marker):
            inside_block = True
            continue
        elif line.startswith(end_marker):
            inside_block = False
            break  # Assuming only one block of JSON
        if inside_block:
            content.append(line)

    json_string = "\n".join(content).strip()
    return json_string   

# Helper Functions
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def process_output(response):
    cool_output("Processing output...", Fore.GREEN)
    json_data = extract_json_content(response)
    return json_data

def cool_output(message, color=Fore.CYAN, bold=True):
    """Prints messages with styled output."""
    prefix = Style.BRIGHT if bold else ""
    print(f"{prefix}{color}{message}{Style.RESET_ALL}")
