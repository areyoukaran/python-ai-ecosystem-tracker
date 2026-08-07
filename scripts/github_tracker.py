import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


REPOSITORIES = [
    "pytorch/pytorch",
    "huggingface/transformers",
    "fastapi/fastapi",
    "scikit-learn/scikit-learn",
    "pandas-dev/pandas",
    "numpy/numpy",
    "langchain-ai/langchain",
    "django/django",
]


def get_repository_data(repository):
    url = f"https://api.github.com/repos/{repository}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "python-ai-ecosystem-tracker",
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)

    with urlopen(request, timeout=20) as response:
        data = json.load(response)

    return {
        "repository": repository,
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"],
        "watchers": data["subscribers_count"],
        "updated_at": data["updated_at"],
    }


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    repositories = []

    for repository in REPOSITORIES:
        try:
            print(f"Fetching {repository}...")
            repositories.append(get_repository_data(repository))
        except Exception as error:
            print(f"Failed to fetch {repository}: {error}")

    output = {
        "date": today,
        "repositories": repositories,
    }

    root = Path(__file__).resolve().parent.parent

    # Latest repository statistics
    latest_directory = root / "data" / "latest"

    # Historical repository statistics
    history_directory = root / "data" / "github"

    latest_directory.mkdir(parents=True, exist_ok=True)
    history_directory.mkdir(parents=True, exist_ok=True)

    latest_file = latest_directory / "github_repositories.json"
    history_file = history_directory / f"{today}.json"

    # Always refresh latest statistics
    with open(latest_file, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    # Historical snapshot should only be created once per day
    if not history_file.exists():
        with open(history_file, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=2)

        print(f"Created GitHub history snapshot: {today}")
    else:
        print(f"GitHub history snapshot already exists: {today}")

    print("GitHub repository statistics updated.")


if __name__ == "__main__":
    main()