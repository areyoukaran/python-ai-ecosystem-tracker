import json
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

    output_directory = root / "data" / "releases"
    output_directory.mkdir(parents=True, exist_ok=True)

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
                changes.append({
                    "package": package,
                    "previous_version": old_version,
                    "new_version": version,
                })

        except Exception as error:
            print(f"Failed to check {package}: {error}")

            # Preserve previous data if API request fails
            if package in previous_versions:
                current_versions[package] = previous_versions[package]

    with open(versions_file, "w", encoding="utf-8") as file:
        json.dump(current_versions, file, indent=2, sort_keys=True)

    if changes:
        with open(changes_file, "w", encoding="utf-8") as file:
            json.dump(changes, file, indent=2)

        print(f"\nDetected {len(changes)} package release(s).")
    else:
        # We don't want an old release_changes file hanging around
        if changes_file.exists():
            changes_file.unlink()

        print("\nNo new package releases detected.")


if __name__ == "__main__":
    main()