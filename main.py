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

REPO_PREFIX = "fake-commit-repo"


def main(start_year=2020, end_year=2024, max_commits_per_day=5):
    for year in range(start_year, end_year + 1):
        repo_name = f"{REPO_PREFIX}-{year}"
        print(f"[+] Creating repo: {repo_name}")
        remote_url = create_github_repo(repo_name)

        local_path = Path.cwd() / repo_name
        local_path.mkdir(exist_ok=True)
        initialize_local_repo(local_path)

        start = date(year, 1, 1)
        end = date(year, 12, 31)

        for commit_day in generate_workdays(start, end):
            for dt in generate_commits(datetime.combine(commit_day, datetime.min.time()), max_commits_per_day):
                commit_with_date(local_path, dt)

        push_to_github(local_path, remote_url)
        create_pull_request(repo_name)
        print(f"[✔] Pushed {repo_name} to GitHub")


if __name__ == "__main__":
    main()

