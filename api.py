from flask import Flask, request, jsonify
import os
import requests
import git
import json
import re
from openai import OpenAI
from typing import TypedDict, List, Optional
from datetime import datetime
from autocodegeneraterl import *

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI()

def process_output(response):
    json_data_string = extract_json_content_string(response)
    return json_data_string


def get_commit_files(repo_owner, repo_name, commit_id):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        files = response.json().get("files", [])
        cool_output(f"Fetched {len(files)} files for commit {commit_id}.", Fore.GREEN)
        return files
    else:
        cool_output(f"Failed to fetch files for commit {commit_id}: {response.status_code}, {response.json()}", Fore.RED)
        return []

def get_file_content(repo_owner, repo_name, file_path, ref=None):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    params = {"ref": ref} if ref else {}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        content_base64 = response.json().get("content")
        if content_base64:
            cool_output(f"Fetched content for file {file_path}.", Fore.GREEN)
            return base64.b64decode(content_base64).decode("utf-8")
        else:
            cool_output(f"No content found in the response for {file_path}.", Fore.YELLOW)
            return None
    else:
        cool_output(f"Failed to fetch file content for {file_path}: {response.status_code}, {response.json()}", Fore.RED)
        return None

def analyze_with_llm(file_name, file_content):
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

def leave_commit_comment(repo_owner, repo_name, commit_id, body, file_path, position):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/comments"
    payload = {
        "body": body,
        "commit_id": commit_id,
        "path": file_path,
        "position": position
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        cool_output(f"Comment posted successfully for {file_path}.", Fore.GREEN)
    else:
        cool_output(f"Failed to post comment for {file_path}: {response.status_code}, {response.json()}", Fore.RED)

def review_commit(repo_owner, repo_name, commit_id):
    files = get_commit_files(repo_owner, repo_name, commit_id)
    if not files:
        cool_output(f"No files found for commit {commit_id}.", Fore.RED)
        return

    for file in files:
        file_path = file.get("filename")
        content = file.get("patch")  # Use the patch content for the diff
        if content:
            feedback = analyze_with_llm(file_path, content)
            cool_output(f"Feedback for {file_path}:{feedback}", Fore.CYAN)
            # Leave the review as a comment on the first line of the file
            leave_commit_comment(repo_owner, repo_name, commit_id, feedback, file_path, position=1)


def generate_code(user_input):
    print("Generating code...")
    
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
                "content": "Generate a JSON response like `{\"language\": {\"{language}\"},\"code\":{\"{full_path_to_file}\":\"{content}\"}}` for every file needed to support the product"
            }
        ]
    )
    print("Code generation complete.")
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()

@app.route('/codereview', methods=['POST'])
def code_review():
    data = request.get_json()
    if not data or 'commit_id' not in data:
        return jsonify({"error": "No commit id provided"}), 400
    if not data or 'repo_name' not in data:
        return jsonify({"error": "No repo name provided"}), 400
    commit_id = data['commit_id']
    repo_name = data['repo_name']

    repo_owner, repo_name = repo_name.split("/")
    review_commit(repo_owner, repo_name, args.commit_id)
    return jsonify({"success": "OK"}), 200

@app.route('/files', methods=['POST'])
def generate_files():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data['prompt']
    content = generate_code(prompt)
    json_data = process_output(content)
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)