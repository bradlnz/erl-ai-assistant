from flask import Flask, request, jsonify
import os
import requests
import git
import json
from openai import OpenAI
from typing import TypedDict, List, Optional
from datetime import datetime
from src import *
import logging
from flasgger import Swagger

app = Flask(__name__)

# Load Swagger JSON from file
with open('api_spec.json', 'r') as file:
    swagger_template = json.load(file)

# Initialize Swagger with the loaded template
swagger = Swagger(app, template=swagger_template)

app.config['PROPAGATE_EXCEPTIONS'] = True

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
base_path = "src"

@app.route('/review', methods=['POST'])
def code_review():
    data = request.get_json()
    if not data or 'repo_name' not in data:
        return jsonify({"error": "No repo_name provided"}), 400
    if not data or 'pr_number' not in data:
        return jsonify({"error": "No pr_number provided"}), 400
    repo_name = data['repo_name']
    pr_number = data['pr_number']

    repo_owner = GITHUB_USER
    repo_name = repo_name
    review_pr(repo_owner, repo_name, pr_number)
    return jsonify({"success": "OK"}), 200

@app.route('/files', methods=['POST'])
def generate_files():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
    prompt = data['prompt']
    cool_output(prompt)
    content = generate_code(prompt, base_path)
    return content

@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    # Log the exception
    app.logger.error(f"An error occurred: {e}")
    # Optionally re-raise the exception to bubble up
    raise e

if __name__ == '__main__':
    app.run(debug=True)