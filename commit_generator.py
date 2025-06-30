import os
import subprocess
import random
from datetime import date, datetime, timedelta
from pathlib import Path

COMMIT_MESSAGES = ["fix bug", "update readme", "refactor code", "improve docs", "add tests"]

LANG_EXTENSIONS = [
    "py", "js", "ipynb", "ts", "html", "liquid", "php", "java", "cs", "kt", "swift"
]

def initialize_local_repo(path):
    subprocess.run(["git", "init"], cwd=path)
    Path(path, "log.txt").write_text("initial\n")
    subprocess.run(["git", "add", "log.txt"], cwd=path)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=path)

def generate_workdays(start_date, end_date, commit_probability):
    day = start_date
    while day <= end_date:
        if day.weekday() < 5 and random.random() < commit_probability:
            yield day
        day += timedelta(days=1)

def generate_commits(commit_day, max_commits):
    commits = random.randint(0, max_commits)
    times = sorted([random.randint(9, 17) for _ in range(commits)])
    return [(commit_day.replace(hour=t, minute=random.randint(0,59), second=random.randint(0,59))) for t in times]

def modify_random_files(path: Path, commit_dt):
    num_files = random.randint(1, 3)
    chosen_exts = random.sample(LANG_EXTENSIONS, num_files)

    for ext in chosen_exts:
        file_name = f"file_{ext}.{ext}"
        file_path = path / file_name
        content = f"# Modified at {commit_dt.isoformat()} for language {ext}\n"

        if file_path.exists():
            with open(file_path, "a") as f:
                f.write(content)
        else:
            with open(file_path, "w") as f:
                f.write(content)

def commit_with_date(path, commit_dt):
    modify_random_files(Path(path), commit_dt)
    subprocess.run(["git", "add", "."], cwd=path)
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
