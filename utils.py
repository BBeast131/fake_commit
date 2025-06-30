
from dotenv import load_dotenv

load_dotenv()

def get_github_credentials():
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    if not token or not username:
        raise EnvironmentError("Missing GITHUB_TOKEN or GITHUB_USERNAME in environment or .env file")
    return token, username

def say_hello():
    print("Welcome to Fake Commit Tool!")