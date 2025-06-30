import os
import subprocess
import random
import requests
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

# how can I get yolo badge

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

def generate_random_repo_name(year):
    suffix = uuid.uuid4().hex[:6]
    return f"{REPO_PREFIX}-{year}-{suffix}"

def main():
    start_year = COMMIT_SETTINGS["start_year"]
    end_year = COMMIT_SETTINGS["end_year"]
    max_commits_per_day = COMMIT_SETTINGS["max_commits_per_day"]

    for year in range(start_year, end_year + 1):
        repo_name = generate_random_repo_name(year)
        print(f"[+] Creating repo: {repo_name}")
        remote_url = create_github_repo(repo_name)

        local_path = Path.cwd() / repo_name
        local_path.mkdir(exist_ok=True)
        initialize_local_repo(local_path)

        start = date(year, 1, 1)
        end = date(year, 12, 31)

        for commit_day in generate_workdays(start, end, COMMIT_SETTINGS["commit_probability"]):
            for dt in generate_commits(datetime.combine(commit_day, datetime.min.time()), max_commits_per_day):
                commit_with_date(local_path, dt)

        push_to_github(local_path, remote_url)
        create_pull_request(repo_name)
        print(f"[✔] Pushed {repo_name} to GitHub")

if __name__ == "__main__":
    main()
