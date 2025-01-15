import os
from openai import OpenAI
from .utils import *
import logging

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI()

def analyze_code(file_name, file_content):
    prompt = f"""
    You are an expert software engineer reviewing a commit. Review the following file for best practices, code quality, and potential improvements:
    
    ### File: {file_name}
    ```
    {file_content}
    ```

    Provide your feedback in a concise and constructive manner.
    """
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a code reviewer."}, {"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    feedback = response.choices[0].message.content.strip()
    cool_output(f"Generated feedback for {file_name}.", Fore.CYAN)
    return feedback

def generate_code(user_input, base_path):
    cool_output("Generating code...")
    
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert software engineer."
            }, 
            {
                "role": "user",
                "content": f"Based on the input:\n{user_input}"
            },
            {
                "role": "user",
                "content": f"The base_path is {base_path}"
            }, 
            {
                "role": "user",
                "content": "Generate a valid JSON response like `{\"language\": {\"{language}\"},\"code\":{\"{base_path}/{full_path_to_file}\":\"{content}\"}}` for every file needed to support the product"
            },
            {
                "role": "user",
                "content": "Clean up and return a valid JSON string"
            }
        ]
    )
    cool_output("Code generation complete.")
    cool_output(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
