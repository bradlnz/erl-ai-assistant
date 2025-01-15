import json
import sys
import time
from colorama import Fore, Style, init

animation_loading = True

def extract_json_content(text: str) -> dict:
    """
    Extract structured JSON content from a response.

    :param text: A string containing JSON content.
    :return: A dictionary parsed from the extracted JSON content.
    """
    try:
        cool_output(f"[🔍] Parsing JSON", Fore.GREEN)
        parsed_json = json.loads(text)
        return parsed_json
    except Exception as e:
        cool_output(f"[🚨] Failed to extract JSON", Fore.RED)


def extract_json_content_string(text: str) -> dict:
    """
    Extract JSON content enclosed between ```json and ``` markers.

    :param text: A string containing JSON content within ```json markers.
    :return: A dictionary parsed from the extracted JSON content.
    """
    try:
        cool_output(f"[🔍] Extracting JSON content")
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
        cool_output(json_string)
        return json_string   
    except Exception as e:
        cool_output(f"[🚨] Failed to extract JSON", Fore.RED)
        raise Exception(e)

def set_animation_loading(loading):
    animation_loading = loading

def display_loading_animation():
    """
    Function to display a non-blocking loading animation.
    """
    animation = "|/-\\"
    while animation_loading:
        for i in range(len(animation)):
            if not animation_loading:
                break
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
            time.sleep(0.2)  # Adjust speed of the animation here
    sys.stdout.write("\rDone!\n")

# Helper Functions
def write_file(file_path, content):
    try:
        cool_output(f"[🔨] Writing file {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        cool_output(f"[🚨] Failed to write file {file_path}", Fore.RED)
        raise Exception(e)

def process_output(response):
    try:
        cool_output("[🔨] Processing output...")
        content = extract_json_content_string(response)
        cool_output(content, Fore.GREEN)
        json_data = content
        return json_data
    except Exception as e:
        cool_output(f"[🚨] Failed to process output", Fore.RED)
        raise Exception(e)

def cool_output(message, color=Fore.CYAN, bold=True):
    """Prints messages with styled output."""
    prefix = Style.BRIGHT if bold else ""
    print(f"{prefix}{color}{message}{Style.RESET_ALL}")
