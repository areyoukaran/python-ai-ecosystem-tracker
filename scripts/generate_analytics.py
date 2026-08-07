import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_previous_snapshot(history_directory, today):
    """
    Find the most recent GitHub snapshot before today.
    """
    if not history_directory.exists():
        return None

    files = sorted(history_directory.glob("*.json"))

    previous_files = [
        file for file in files
        if file.stem < today
    ]

    if not previous_files:
        return None

    return load_json(previous_files[-1])


def calculate_growth(current_repositories, previous_snapshot):
    """
    Compare current GitHub statistics with the previous
    historical snapshot.
    """
    if previous_snapshot is None:
        return []

    previous_repositories = {
        repo["repository"]: repo
        for repo in previous_snapshot.get("repositories", [])
    }

    growth = []

    for repo in current_repositories:
        name = repo["repository"]

        if name not in previous_repositories:
            continue

        previous = previous_repositories[name]

        growth.append({
            "repository": name,
            "stars_change": (
                repo["stars"] - previous["stars"]
            ),
            "forks_change": (
                repo["forks"] - previous["forks"]
            ),
            "issues_change": (
                repo["open_issues"] - previous["open_issues"]
            ),
        })

    return growth


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    root = Path(__file__).resolve().parent.parent

    # -----------------------------
    # Input paths
    # -----------------------------

    github_latest_file = (
        root / "data" / "latest" / "github_repositories.json"
    )

    github_history_directory = (
        root / "data" / "github"
    )

    versions_file = (
        root / "data" / "releases" / "current_versions.json"
    )

    # -----------------------------
    # Output paths
    # -----------------------------

    analytics_directory = root / "analytics"
    analytics_history_directory = (
        analytics_directory / "history"
    )

    analytics_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    analytics_history_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------
    # Load GitHub data
    # -----------------------------

    if not github_latest_file.exists():
        print("GitHub repository data not found.")
        return

    github_data = load_json(github_latest_file)

    repositories = github_data.get("repositories", [])

    if not repositories:
        print("No repository data available.")
        return

    # -----------------------------
    # Rankings
    # -----------------------------

    ranked_by_stars = sorted(
        repositories,
        key=lambda repo: repo["stars"],
        reverse=True,
    )

    ranked_by_forks = sorted(
        repositories,
        key=lambda repo: repo["forks"],
        reverse=True,
    )

    # -----------------------------
    # Ecosystem totals
    # -----------------------------

    total_stars = sum(
        repo["stars"]
        for repo in repositories
    )

    total_forks = sum(
        repo["forks"]
        for repo in repositories
    )

    total_open_issues = sum(
        repo["open_issues"]
        for repo in repositories
    )

    # -----------------------------
    # Historical growth
    # -----------------------------

    previous_snapshot = get_previous_snapshot(
        github_history_directory,
        today,
    )

    growth = calculate_growth(
        repositories,
        previous_snapshot,
    )

    growth_by_stars = sorted(
        growth,
        key=lambda repo: repo["stars_change"],
        reverse=True,
    )

    # -----------------------------
    # Package versions
    # -----------------------------

    package_versions = {}

    if versions_file.exists():
        package_versions = load_json(versions_file)

    # -----------------------------
    # Construct analytics
    # -----------------------------

    analytics = {
        "date": today,

        "summary": {
            "repositories_tracked": len(repositories),
            "packages_tracked": len(package_versions),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_open_issues": total_open_issues,
        },

        "top_by_stars": [
            {
                "repository": repo["repository"],
                "stars": repo["stars"],
            }
            for repo in ranked_by_stars
        ],

        "top_by_forks": [
            {
                "repository": repo["repository"],
                "forks": repo["forks"],
            }
            for repo in ranked_by_forks
        ],

        "daily_growth": growth_by_stars,

        "package_versions": package_versions,
    }

    # -----------------------------
    # Latest analytics
    # -----------------------------

    latest_file = (
        analytics_directory / "latest_metrics.json"
    )

    with open(
        latest_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            analytics,
            file,
            indent=2
        )

    # -----------------------------
    # Historical analytics
    # -----------------------------

    history_file = (
        analytics_history_directory /
        f"{today}.json"
    )

    if not history_file.exists():

        with open(
            history_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                analytics,
                file,
                indent=2
            )

        print(
            f"Created analytics snapshot: {today}"
        )

    else:
        print(
            f"Analytics snapshot already exists: {today}"
        )

    print("Analytics generated successfully.")

    if growth_by_stars:

        fastest = growth_by_stars[0]

        print(
            "Fastest growing repository: "
            f"{fastest['repository']} "
            f"({fastest['stars_change']:+} stars)"
        )

    else:

        print(
            "Growth analytics unavailable until "
            "another historical day exists."
        )


if __name__ == "__main__":
    main()