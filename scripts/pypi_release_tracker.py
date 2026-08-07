import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


PACKAGES = [
    "fastapi",
    "django",
    "flask",
    "numpy",
    "pandas",
    "torch",
    "transformers",
    "scikit-learn",
]


def get_latest_version(package):
    url = f"https://pypi.org/pypi/{package}/json"

    with urlopen(url, timeout=20) as response:
        data = json.load(response)

    return data["info"]["version"]


def load_previous_versions(file_path):
    if not file_path.exists():
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    root = Path(__file__).resolve().parent.parent
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_directory = root / "data" / "releases"
    history_directory = output_directory / "history"

    output_directory.mkdir(parents=True, exist_ok=True)
    history_directory.mkdir(parents=True, exist_ok=True)

    versions_file = output_directory / "current_versions.json"
    changes_file = output_directory / "release_changes.json"

    previous_versions = load_previous_versions(versions_file)

    current_versions = {}
    changes = []

    for package in PACKAGES:
        try:
            version = get_latest_version(package)
            current_versions[package] = version

            old_version = previous_versions.get(package)

            print(f"{package}: {old_version} -> {version}")

            if old_version is not None and old_version != version:
                changes.append(
                    {
                        "package": package,
                        "previous_version": old_version,
                        "new_version": version,
                    }
                )

        except Exception as error:
            print(f"Failed to check {package}: {error}")

            # Preserve the previous version if PyPI cannot be reached.
            if package in previous_versions:
                current_versions[package] = previous_versions[package]

    # Store the latest known versions.
    with open(versions_file, "w", encoding="utf-8") as file:
        json.dump(current_versions, file, indent=2, sort_keys=True)

    if changes:
        release_data = {
            "date": today,
            "releases": changes,
        }

        # Current/latest detected changes.
        with open(changes_file, "w", encoding="utf-8") as file:
            json.dump(release_data, file, indent=2)

        # Permanent historical record.
        history_file = history_directory / f"{today}.json"

        if history_file.exists():
            # If multiple tracked packages release on the same day,
            # merge them into the same historical file.
            with open(history_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)

            existing_releases = existing_data.get("releases", [])

            for release in changes:
                if release not in existing_releases:
                    existing_releases.append(release)

            release_data["releases"] = existing_releases

        with open(history_file, "w", encoding="utf-8") as file:
            json.dump(release_data, file, indent=2)

        print(f"\nDetected {len(changes)} package release(s).")
        print(f"Release history updated: {today}")

    else:
        # Prevent yesterday's changes from appearing as today's changes.
        if changes_file.exists():
            changes_file.unlink()

        print("\nNo new package releases detected.")


if __name__ == "__main__":
    main()