# Fake Commit Tool

Automatically creates private GitHub repositories and generates realistic fake commit histories with optional pull requests.

---

## Features

- Creates private GitHub repositories automatically
- Generates 0–5 commits per workday randomly with adjustable frequency
- Supports configurable start and end years for commit history generation
- Pushes commits and opens a fake pull request on GitHub
- Uses `.env` file for GitHub authentication securely

---

## Setup

1. Clone this repository or copy files to your local machine.

2. Install Python dependencies:

```bash
pip install requests python-dotenv
