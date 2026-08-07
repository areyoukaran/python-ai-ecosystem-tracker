import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path


TASKS = [
    "github",
    "pypi",
    "analytics",
    "report",
]

# Snapshot always runs, guaranteeing at least one useful daily task.
GUARANTEED_TASK = "snapshot"


def write_github_outputs(tasks):
    """
    Send the selected tasks to GitHub Actions.

    When running locally, GITHUB_OUTPUT does not exist,
    so this function simply does nothing.
    """
    output_path = os.getenv("GITHUB_OUTPUT")

    if not output_path:
        return

    selected = set(tasks)

    with open(output_path, "a", encoding="utf-8") as file:
        for task in ["snapshot", "github", "pypi", "analytics", "report"]:
            value = "true" if task in selected else "false"
            file.write(f"{task}={value}\n")


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Same date = same selection, even if workflow is re-run.
    rng = random.Random(today)

    # Randomly select 1-5 tasks.
    target_count = rng.randint(1, 5)

    # Snapshot already counts as one.
    optional_count = target_count - 1
    selected = rng.sample(TASKS, optional_count)

    tasks = [GUARANTEED_TASK] + selected

    # Make selections available to GitHub Actions.
    write_github_outputs(tasks)

    result = {
        "date": today,
        "target_count": target_count,
        "tasks": tasks,
    }

    root = Path(__file__).resolve().parent.parent

    runtime = root / ".runtime"
    runtime.mkdir(exist_ok=True)

    output = runtime / "daily_tasks.json"

    with open(output, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    print(f"Daily target: {target_count}")
    print(f"Selected tasks: {', '.join(tasks)}")


if __name__ == "__main__":
    main()