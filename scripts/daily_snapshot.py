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


def get_package_data(package):
    url = f"https://pypi.org/pypi/{package}/json"

    with urlopen(url, timeout=20) as response:
        data = json.load(response)

    info = data["info"]

    return {
        "name": info["name"],
        "version": info["version"],
        "python_requires": info["requires_python"],
    }


def main():
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    packages = []

    for package in PACKAGES:
        try:
            packages.append(get_package_data(package))
        except Exception as error:
            print(f"Failed to fetch {package}: {error}")

    snapshot = {
        "date": today,
        "collected_at": now.isoformat(),
        "packages": packages,
    }

    root = Path(__file__).resolve().parent.parent

    daily_directory = root / "data" / "daily"
    latest_directory = root / "data" / "latest"

    daily_directory.mkdir(parents=True, exist_ok=True)
    latest_directory.mkdir(parents=True, exist_ok=True)

    daily_file = daily_directory / f"{today}.json"
    latest_file = latest_directory / "packages.json"

    with open(daily_file, "w", encoding="utf-8") as file:
        json.dump(snapshot, file, indent=2)

    with open(latest_file, "w", encoding="utf-8") as file:
        json.dump(snapshot, file, indent=2)

    print(f"Snapshot created for {today}")


if __name__ == "__main__":
    main()