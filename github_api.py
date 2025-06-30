import os
import requests
from utils import get_github_credentials

GITHUB_TOKEN, GITHUB_USERNAME = get_github_credentials()

def create_github_repo(repo_name):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "name": repo_name,
        "private": True,
        "auto_init": False,
    }
    res = requests.post("https://api.github.com/user/repos", json=data, headers=headers)
    res.raise_for_status()
    return res.json()["clone_url"]

def create_pull_request(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/pulls"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "title": "Fake PR",
        "head": "main",
        "base": "main",
        "body": "This is a fake PR generated automatically."
    }
    try:
        requests.post(url, json=data, headers=headers)
    except:
        pass  # safe to fail silently here

