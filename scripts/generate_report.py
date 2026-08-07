import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_number(number):
    return f"{number:,}"


def build_report(analytics):
    date = analytics.get("date", "Unknown")

    summary = analytics.get("summary", {})
    top_by_stars = analytics.get("top_by_stars", [])
    top_by_forks = analytics.get("top_by_forks", [])
    daily_growth = analytics.get("daily_growth", [])
    package_versions = analytics.get("package_versions", {})

    lines = []

    # --------------------------------
    # Header
    # --------------------------------

    lines.append(f"# Python AI Ecosystem Report — {date}")
    lines.append("")
    lines.append(
        "Automatically generated from the repository's "
        "daily ecosystem dataset."
    )
    lines.append("")

    # --------------------------------
    # Ecosystem summary
    # --------------------------------

    lines.append("## Ecosystem Summary")
    lines.append("")

    lines.append(
        f"- **Repositories tracked:** "
        f"{summary.get('repositories_tracked', 0)}"
    )

    lines.append(
        f"- **Packages tracked:** "
        f"{summary.get('packages_tracked', 0)}"
    )

    lines.append(
        f"- **Combined GitHub stars:** "
        f"{format_number(summary.get('total_stars', 0))}"
    )

    lines.append(
        f"- **Combined forks:** "
        f"{format_number(summary.get('total_forks', 0))}"
    )

    lines.append(
        f"- **Combined open issues:** "
        f"{format_number(summary.get('total_open_issues', 0))}"
    )

    lines.append("")

    # --------------------------------
    # Top repositories by stars
    # --------------------------------

    lines.append("## Top Repositories by Stars")
    lines.append("")

    lines.append("| Rank | Repository | Stars |")
    lines.append("| ---: | --- | ---: |")

    for rank, repository in enumerate(
        top_by_stars[:10],
        start=1,
    ):
        lines.append(
            f"| {rank} | "
            f"{repository['repository']} | "
            f"{format_number(repository['stars'])} |"
        )

    lines.append("")

    # --------------------------------
    # Top repositories by forks
    # --------------------------------

    lines.append("## Top Repositories by Forks")
    lines.append("")

    lines.append("| Rank | Repository | Forks |")
    lines.append("| ---: | --- | ---: |")

    for rank, repository in enumerate(
        top_by_forks[:10],
        start=1,
    ):
        lines.append(
            f"| {rank} | "
            f"{repository['repository']} | "
            f"{format_number(repository['forks'])} |"
        )

    lines.append("")

    # --------------------------------
    # Daily growth
    # --------------------------------

    lines.append("## Daily Repository Growth")
    lines.append("")

    if daily_growth:

        lines.append(
            "| Repository | Stars | Forks | Issues |"
        )
        lines.append(
            "| --- | ---: | ---: | ---: |"
        )

        for repository in daily_growth:

            lines.append(
                f"| {repository['repository']} | "
                f"{repository['stars_change']:+} | "
                f"{repository['forks_change']:+} | "
                f"{repository['issues_change']:+} |"
            )

    else:

        lines.append(
            "Growth data is not yet available. "
            "At least two historical snapshots are required."
        )

    lines.append("")

    # --------------------------------
    # Package versions
    # --------------------------------

    lines.append("## Tracked Python Package Versions")
    lines.append("")

    lines.append("| Package | Version |")
    lines.append("| --- | --- |")

    for package, version in sorted(package_versions.items()):

        lines.append(
            f"| {package} | `{version}` |"
        )

    lines.append("")

    # --------------------------------
    # Footer
    # --------------------------------

    lines.append("---")
    lines.append("")
    lines.append(
        "Generated automatically by "
        "`python-ai-ecosystem-tracker`."
    )
    lines.append("")

    return "\n".join(lines)


def main():
    root = Path(__file__).resolve().parent.parent

    analytics_file = (
        root / "analytics" / "latest_metrics.json"
    )

    if not analytics_file.exists():
        print(
            "Analytics data not found. "
            "Run generate_analytics.py first."
        )
        return

    analytics = load_json(analytics_file)

    today = analytics.get(
        "date",
        datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )

    reports_directory = root / "reports"
    history_directory = reports_directory / "history"

    reports_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    history_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = build_report(analytics)

    # --------------------------------
    # Latest report
    # --------------------------------

    latest_file = reports_directory / "latest.md"

    with open(
        latest_file,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report)

    # --------------------------------
    # Historical report
    # --------------------------------

    history_file = history_directory / f"{today}.md"

    if not history_file.exists():

        with open(
            history_file,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(report)

        print(f"Created historical report: {today}")

    else:

        print(
            f"Historical report already exists: {today}"
        )

    print("Latest ecosystem report generated.")


if __name__ == "__main__":
    main()