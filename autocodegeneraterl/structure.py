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
    language = language.lower()

    if language == "python":
        # Step 1: Analyze syntax
        try:
            ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

        # Step 2: Format code using black
        try:
            formatted_code = black.format_str(code, mode=Mode())
            return True, formatted_code
        except black.InvalidInput as e:
            return False, f"Formatting Error: {e}"

    elif language == "javascript":
        # Basic formatting for JavaScript using Python logic (indentation and braces)
        try:
            lines = code.splitlines()
            formatted_code = "\n".join(line.strip() for line in lines if line.strip())
            return True, formatted_code
        except Exception as e:
            return False, f"Formatting Error: {e}"

    elif language == "java":
        # Basic formatting for Java (naive approach)
        try:
            lines = code.splitlines()
            formatted_code = "\n".join(line.strip() for line in lines if line.strip())
            return True, formatted_code
        except Exception as e:
            return False, f"Formatting Error: {e}"

    elif language == "c#":
        # Basic formatting for C# (naive approach)
        try:
            lines = code.splitlines()
            formatted_code = "\n".join(line.strip() for line in lines if line.strip())
            return True, formatted_code
        except Exception as e:
            return False, f"Formatting Error: {e}"

    elif language == "go":
        # Basic formatting for Go (naive approach)
        try:
            lines = code.splitlines()
            formatted_code = "\n".join(line.strip() for line in lines if line.strip())
            return True, formatted_code
        except Exception as e:
            return False, f"Formatting Error: {e}"

    else:
        return False, f"Unsupported language: {language}. Supported languages are Python, JavaScript, C#, Java, and Go."

def create_structure(base_path: str, structure: dict):
    """
    Recursively create directories and files based on a nested dictionary structure.

    :param base_path: The root directory where the structure will be created.
    :param structure: A nested dictionary representing the folder and file structure.
    """
    if not isinstance(structure, dict):
        raise ValueError("Provided structure is not a valid dictionary.")
    print(structure["code"])
    
    for file_name, file_data in structure["code"].items():
        print(f"FN: {file_name}")
        print(f"FD: {file_data}")
        file_path = os.path.join(base_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        valid, result = analyze_and_format_code(file_data, structure["language"])
        print(result)
        with open(file_path, 'w') as f:
            f.write(result)
            cool_output(f"Created file: {file_path}", Fore.GREEN)
