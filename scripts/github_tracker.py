import json
import os
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

    repositories = []

    for repository in REPOSITORIES:
        try:
            print(f"Fetching {repository}...")
            repositories.append(get_repository_data(repository))
        except Exception as error:
            print(f"Failed to fetch {repository}: {error}")

    output = {
        "repositories": repositories,
    }

    root = Path(__file__).resolve().parent.parent

    output_directory = root / "data" / "latest"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "github_repositories.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("GitHub repository statistics updated.")


if __name__ == "__main__":
    main()