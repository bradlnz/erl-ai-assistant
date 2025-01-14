import os
import requests
import git
from datetime import datetime
from .utils import cool_output
from colorama import Fore

now = datetime.now()
timestamp = now.timestamp()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
REPO_NAME = f"GeneratedSystemRepo_{timestamp}"
BRANCH_NAME = f"code-improvements_{timestamp}"

def create_pull_request(repo_url, branch_name):
    pr_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"title": "Code Improvements", "head": branch_name, "base": "main"}
    response = requests.post(pr_url, json=payload, headers=headers)
    if response.status_code == 201:
        cool_output("Pull request created successfully.")
    else:
        cool_output(f"Failed to create pull request: {response.json()}")

def push_to_github(base_path):
    cool_output("Initializing GitHub repository...", Fore.BLUE)
    os.makedirs(base_path, exist_ok=True)
    create_repo_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": REPO_NAME,
        "private": True,
        "description": "Repository for generated code with improvements"
    }
    response = requests.post(create_repo_url, headers=headers, json=payload)
    if response.status_code == 201:
        cool_output(f"Repository '{REPO_NAME}' created successfully.", Fore.GREEN)
    elif response.status_code == 422:
        cool_output(f"Repository '{REPO_NAME}' already exists.", Fore.YELLOW)
    else:
        cool_output(f"Failed to create repository: {response.json()}", Fore.RED)
        return

    repo = git.Repo.init(base_path)
    repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
    origin = repo.create_remote("origin", repo_url)

    if not repo.head.is_valid():
        cool_output("Creating initial commit...")
        repo.git.checkout("-b", "main")
        repo.index.commit("Initial commit with generated code")
        origin.push("main")

    try:
        repo.git.checkout("-b", BRANCH_NAME)
        cool_output(f"Switching to branch '{BRANCH_NAME}'...")
        repo.git.add(all=True)
        repo.index.commit("Initial commit for improvements")
        origin.push(refspec=f"refs/heads/{BRANCH_NAME}:refs/heads/{BRANCH_NAME}")
        cool_output(f"Feature branch '{BRANCH_NAME}' pushed successfully.", Fore.GREEN)
        create_pull_request(repo_url, BRANCH_NAME)
    except Exception as e:
        cool_output(f"Failed to push branch: {e}", Fore.RED)