import os
import subprocess
import random
from datetime import date, datetime, timedelta
from pathlib import Path

COMMIT_MESSAGES = ["fix bug", "update readme", "refactor code", "improve docs", "add tests"]

def initialize_local_repo(path):
    subprocess.run(["git", "init"], cwd=path)
    Path(path, "log.txt").write_text("initial\n")
    subprocess.run(["git", "add", "log.txt"], cwd=path)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=path)

def generate_workdays(start_date, end_date):
    day = start_date
    while day <= end_date:
        if day.weekday() < 5 and random.random() > 0.2:
            yield day
        day += timedelta(days=1)

def generate_commits(commit_day, max_commits):
    commits = random.randint(0, max_commits)
    times = sorted([random.randint(9, 17) for _ in range(commits)])
    return [(commit_day.replace(hour=t, minute=random.randint(0,59), second=random.randint(0,59))) for t in times]

def commit_with_date(path, commit_dt):
    with open(Path(path, "log.txt"), "a") as f:
        f.write(f"{commit_dt.isoformat()}\n")
    subprocess.run(["git", "add", "log.txt"], cwd=path)
    env = os.environ.copy()
    date_str = commit_dt.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    msg = random.choice(COMMIT_MESSAGES)
    subprocess.run(["git", "commit", "-m", msg], cwd=path, env=env)

def push_to_github(local_path, remote_url):
    subprocess.run(["git", "branch", "-M", "main"], cwd=local_path)
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=local_path)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=local_path)

