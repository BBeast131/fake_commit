import os
import subprocess
import random
import requests
from datetime import date, datetime, timedelta
from pathlib import Path

from github_api import create_github_repo, create_pull_request
from commit_generator import (
    initialize_local_repo,
    generate_workdays,
    generate_commits,
    commit_with_date,
    push_to_github,
)
from settings import COMMIT_SETTINGS

REPO_PREFIX = "fake-commit-repo"


def main():
    start_date = datetime.strptime(COMMIT_SETTINGS["start_date"], "%Y-%m-%d").date()
    end_date = datetime.strptime(COMMIT_SETTINGS["end_date"], "%Y-%m-%d").date()
    max_commits_per_day = COMMIT_SETTINGS["max_commits_per_day"]

    repo_name = "fake-commit-repo"

    # Use a single repo for the whole range OR
    # you can split by year if you want, here I just do a single repo
    print(f"[+] Creating repo: {repo_name}")
    remote_url = create_github_repo(repo_name)

    local_path = Path.cwd() / repo_name
    local_path.mkdir(exist_ok=True)
    initialize_local_repo(local_path)

    for commit_day in generate_workdays(start_date, end_date, COMMIT_SETTINGS["commit_probability"]):
        for dt in generate_commits(datetime.combine(commit_day, datetime.min.time()), max_commits_per_day):
            commit_with_date(local_path, dt)

    push_to_github(local_path, remote_url)
    create_pull_request(repo_name)
    print(f"[✔] Pushed {repo_name} to GitHub")


if __name__ == "__main__":
    main()