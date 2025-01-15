import os
import requests
import git
from datetime import datetime
from .utils import cool_output
from .llm import *
from colorama import Fore

now = datetime.now()
timestamp = now.timestamp()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
REPO_NAME = f"GeneratedSystemRepo_{timestamp}"
BRANCH_NAME = f"code-improvements_{timestamp}"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_pr_files(repo_owner, repo_name, pr_number):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch PR files: {response.status_code}, {response.json()}")
        return []

def get_file_content(repo_owner, repo_name, file_path, ref=None):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    params = {"ref": ref} if ref else {}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        content_base64 = response.json().get("content")
        if content_base64:
            return base64.b64decode(content_base64).decode("utf-8")
        else:
            print("No content found in the response.")
            return None
    else:
        print(f"Failed to fetch file content for {file_path}.")
        return None

def create_pull_request(repo_url, branch_name):
    try:
        pr_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/pulls"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        payload = {"title": "Code Improvements", "head": branch_name, "base": "main"}
        response = requests.post(pr_url, json=payload, headers=headers)
        if response.status_code == 201:
            cool_output(f"[✅] Pull request created: (https://github.com/{GITHUB_USER}/{REPO_NAME}/pull/1)", Fore.GREEN)
            review_pr(GITHUB_USER, REPO_NAME, 1)
        else:
            cool_output(f"[🚨] Failed to create pull request: {response.json()}")
    except Exception as e:
         cool_output(f"[🚨] Failed to create pull request: {e}", Fore.RED)
         raise Exception(e)

def leave_pr_comment(repo_owner, repo_name, pr_number, body, file_path, commit_id, position):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/comments"
    payload = {
        "body": body,
        "commit_id": commit_id,
        "path": file_path,
        "position": position
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print(f"Failed to post comment: {response.status_code}, {response.json()}")

def get_pr_commits(repo_owner, repo_name, pr_number):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/commits"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch commits: {response.status_code}, {response.json()}")
        return []

def review_pr(repo_owner, repo_name, pr_number):
    commits = get_pr_commits(repo_owner, repo_name, pr_number)
    if not commits:
        print(f"No commits found for PR #{pr_number}.")
        return

    for commit in commits:
        files = get_pr_files(repo_owner, repo_name, pr_number)
        for file in files:
            file_path = file["filename"]
            content = file.get("patch")  # Use the patch content for the diff
            if content:
                feedback = analyze_code(file_path, content)
                print(f"Feedback for {file_path}:\n{feedback}")
                # Leave the review as a comment on the first line of the file
                leave_pr_comment(repo_owner, repo_name, pr_number, feedback, file_path, commit["sha"], position=1)

def push_to_github(base_path):
    try:
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
            cool_output(f"[✅] Repository '{REPO_NAME}' created successfully.", Fore.GREEN)
        elif response.status_code == 422:
            cool_output(f"[❗] Repository '{REPO_NAME}' already exists.", Fore.YELLOW)
        else:
            cool_output(f"[🚨] Failed to create repository: {response.json()}", Fore.RED)
            return

        repo = git.Repo.init(base_path)
        repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
        origin = repo.create_remote("origin", repo_url)

        if not repo.head.is_valid():
            cool_output("Creating initial commit...")
            repo.git.checkout("-b", "main")
            repo.index.commit("Initial commit with generated code")
            origin.push("main")

    
            repo.git.checkout("-b", BRANCH_NAME)
            cool_output(f"Switching to branch '{BRANCH_NAME}'...")
            repo.git.add(all=True)
            repo.index.commit("Initial commit for improvements")
            origin.push(refspec=f"refs/heads/{BRANCH_NAME}:refs/heads/{BRANCH_NAME}")
            cool_output(f"Feature branch '{BRANCH_NAME}' pushed successfully.", Fore.GREEN)
            cool_output(f"Repository created: https://github.com/{GITHUB_USER}/{REPO_NAME}", Fore.GREEN)
            create_pull_request(repo_url, BRANCH_NAME)
    except Exception as e:
        cool_output(f"[🚨] Failed to push branch: {e}", Fore.RED)
        raise Exception(e)