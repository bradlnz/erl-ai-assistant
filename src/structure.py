import os
import json
from typing import TypedDict, List, Optional, Tuple, Union
from .utils import cool_output
from colorama import Fore

def analyze_and_format_code(code: str, language: str) -> Tuple[bool, Union[str, None]]:
    """
    Analyzes and formats the provided code for supported languages.

    Args:
        code (str): The code to be analyzed and formatted.
        language (str): The programming language of the code. Supported languages are Python, JavaScript, C#, Java, and Go.

    Returns:
        Tuple[bool, Union[str, None]]: A tuple where the first element is a boolean indicating
                                       whether the code is valid, and the second element is the
                                       formatted code (or an error message if invalid).
    """
    try:
        language = language.lower()

        if language == "python":
            # Analyze and format Python code without using external libraries
            lines = code.splitlines()
            formatted_code = []
            indent_level = 0

            for line in lines:
                stripped_line = line.strip()

                # Adjust indentation based on Python syntax
                if stripped_line.startswith("def ") or stripped_line.startswith("class ") or stripped_line.endswith(":"):
                    formatted_code.append("    " * indent_level + stripped_line)
                    indent_level += 1
                elif stripped_line == "":
                    formatted_code.append("")  # Preserve blank lines
                else:
                    if stripped_line.startswith("return") or stripped_line.startswith("pass") or stripped_line.startswith("break") or stripped_line.startswith("continue"):
                        formatted_code.append("    " * max(indent_level - 1, 0) + stripped_line)
                    else:
                        formatted_code.append("    " * indent_level + stripped_line)

            return True, "\n".join(formatted_code)

        elif language in {"javascript", "java", "csharp", "c#", "go"}:
            # Formatting for JavaScript, Java, C#, and Go
            lines = code.splitlines()
            formatted_code = []
            indent_level = 0

            for line in lines:
                stripped_line = line.strip()

                # Adjust indent level for closing braces
                if stripped_line.startswith("}"):
                    indent_level = max(indent_level - 1, 0)

                # Apply indentation
                formatted_code.append("    " * indent_level + stripped_line)

                # Adjust indent level for opening braces
                if stripped_line.endswith("{"):
                    indent_level += 1

            return True, "\n".join(formatted_code)
        else:
            return False, f"Unsupported language: {language}. Supported languages are Python, JavaScript, C#, Java, and Go."
    except Exception as e:
        cool_output(f"[🚨] Failed to complete code formatting: {e}", Fore.RED)
        raise Exception(e)

def extract_file_details(structure):
    """
    Extract file names and their contents from a given structure.

    :param structure: A nested dictionary representing the folder and file structure.
    :return: A dictionary where keys are file names and values are file contents.
    """
    file_details = []
    try:
        # Check if the structure contains the expected "code" key
        if "code" in structure:
            for file_name, file_content in structure["code"].items():
                file_details.append({f"{file_name}" : f"{file_content}"})
        else:
            print("No 'code' key found in the structure")
    except json.JSONDecodeError:
        print("Invalid JSON structure")
    except Exception as e:
        print(f"Error while extracting file details: {e}")
    
    return file_details

def create_structure(base_path: str, structure: dict):
    """
    Recursively create directories and files based on a nested dictionary structure.

    :param base_path: The root directory where the structure will be created.
    :param structure: A nested dictionary representing the folder and file structure.
    """
    try:
        # Ensure the input is a dictionary, not a string
        if isinstance(structure, str):
            structure = json.loads(structure)

        # Extract file details (list of dictionaries)
        file_details = extract_file_details(structure)

        # Iterate through the list of file details
        for item in file_details:
            # Extract file name and content
            for file_name, file_content in item.items():
                file_path = os.path.join(base_path, file_name)
                cool_output(f"CONTENT: {file_content}")
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Write the file content
                with open(file_path, 'w') as f:
                    f.write(file_content)

                # Validate and format the code if needed
                with open(file_path, 'r') as file:
                    content = file.read()
                    valid, result = analyze_and_format_code(content, structure.get("language", "text"))
                    if valid:
                        with open(file_path, 'w') as f:
                            f.write(result)

                # Log success
                cool_output(f"[✅] Created file: {file_path}", Fore.WHITE)

    except Exception as e:
        # Handle exceptions and log errors
        cool_output(f"[🚨] Failed to create file structure", Fore.RED)
        raise Exception(e)

