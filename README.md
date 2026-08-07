# Python AI Ecosystem Tracker

An automated data pipeline that monitors the Python and AI open-source ecosystem, tracks package releases and repository activity, preserves historical snapshots, and generates ecosystem analytics and reports.

The project runs automatically through GitHub Actions and builds a growing historical dataset of popular Python and machine-learning projects.

---

## Overview

The Python and AI ecosystem changes constantly. Packages release new versions, repositories gain contributors and stars, and project activity changes over time.

**Python AI Ecosystem Tracker** periodically collects this information and converts it into structured historical data that can be analyzed over time.

The pipeline currently monitors:

- PyPI package versions and release changes
- GitHub repository statistics
- Daily ecosystem snapshots
- Historical repository data
- Ecosystem-wide analytics
- Automatically generated reports

---

## Tracked Projects

### Python / AI Packages

The tracker currently monitors packages including:

| Package | Ecosystem |
|---|---|
| PyTorch | Deep Learning |
| Transformers | Machine Learning / LLMs |
| scikit-learn | Machine Learning |
| NumPy | Scientific Computing |
| pandas | Data Analysis |
| FastAPI | Backend / APIs |
| Django | Web Development |
| Flask | Web Development |

### GitHub Repositories

Repository statistics are collected for projects including:

- `pytorch/pytorch`
- `huggingface/transformers`
- `fastapi/fastapi`
- `scikit-learn/scikit-learn`
- `pandas-dev/pandas`
- `numpy/numpy`
- `langchain-ai/langchain`
- `django/django`

---

## Architecture

```text
                  ┌─────────────────────┐
                  │   GitHub Actions    │
                  │    Scheduler        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Daily Task Selector │
                  └──────────┬──────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
      PyPI API          GitHub API        Daily Snapshot
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Historical Dataset  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Analytics Engine    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Ecosystem Reports   │
                  └─────────────────────┘
```

---

## Project Structure

```text
python-ai-ecosystem-tracker/
│
├── .github/
│   └── workflows/
│       └── daily.yml
│
├── analytics/
│   ├── history/
│   └── latest_metrics.json
│
├── data/
│   ├── daily/
│   ├── github/
│   ├── latest/
│   └── releases/
│
├── reports/
│
├── scripts/
│   ├── daily_snapshot.py
│   ├── github_tracker.py
│   ├── pypi_release_tracker.py
│   ├── generate_analytics.py
│   ├── generate_report.py
│   └── select_daily_tasks.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Data Pipeline

### 1. Daily Ecosystem Snapshot

`daily_snapshot.py` queries PyPI and stores a dated snapshot of tracked packages.

Historical snapshots are stored under:

```text
data/daily/
```

This creates a time-series dataset rather than continuously overwriting previous observations.

### 2. GitHub Repository Tracking

`github_tracker.py` retrieves repository statistics through the GitHub API, including:

- Stars
- Forks
- Open issues
- Watchers
- Repository update timestamps

Historical observations are preserved in:

```text
data/github/
```

while the latest state is available under:

```text
data/latest/
```

### 3. PyPI Release Detection

`pypi_release_tracker.py` monitors package versions and detects when tracked Python projects publish new releases.

Version history is stored under:

```text
data/releases/
```

### 4. Analytics Engine

`generate_analytics.py` processes the collected datasets and generates aggregate ecosystem metrics.

Examples include:

- Total stars across tracked repositories
- Total forks
- Open issue counts
- Repository rankings
- Package statistics

Latest analytics are written to:

```text
analytics/latest_metrics.json
```

Historical analytics are preserved under:

```text
analytics/history/
```

### 5. Report Generation

`generate_report.py` converts collected metrics into a human-readable ecosystem report.

This provides a higher-level view of the tracked open-source ecosystem without requiring direct inspection of the raw JSON datasets.

---

## Automated Scheduling

The project uses **GitHub Actions** for unattended execution.

A deterministic daily task selector chooses a subset of monitoring and analysis operations for each scheduled run.

The daily snapshot acts as the baseline collection operation, while additional jobs can include:

```text
GitHub statistics
PyPI release monitoring
Analytics generation
Report generation
```

Task selection is deterministic for a given date, making workflow re-runs reproducible.

The workflow only creates commits when generated project data actually changes.

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/areyoukaran/python-ai-ecosystem-tracker.git
cd python-ai-ecosystem-tracker
```

Run a daily snapshot:

```bash
python scripts/daily_snapshot.py
```

Collect GitHub statistics:

```bash
python scripts/github_tracker.py
```

Check PyPI releases:

```bash
python scripts/pypi_release_tracker.py
```

Generate analytics:

```bash
python scripts/generate_analytics.py
```

Generate the ecosystem report:

```bash
python scripts/generate_report.py
```

Test the daily task selector:

```bash
python scripts/select_daily_tasks.py
```

---

## Data Sources

The tracker currently uses publicly available information from:

- PyPI JSON API
- GitHub REST API

No scraped HTML is required for the core data pipeline.

---

## Why Historical Data?

A single API request only tells us what a project looks like **right now**.

By preserving snapshots, the repository can eventually answer more useful questions such as:

- Which AI repositories are growing fastest?
- How quickly are popular Python packages releasing versions?
- How does repository activity change over several months?
- Which projects consistently gain stars?
- How do issue counts evolve?
- Which parts of the Python/AI ecosystem are becoming more active?

The value of the dataset therefore increases as the tracker continues running.

---

## Future Improvements

Potential extensions include:

- Repository growth-rate calculations
- Weekly and monthly trend reports
- Release-frequency analytics
- Star and fork growth visualizations
- Contributor activity tracking
- GitHub issue velocity analysis
- Package dependency analysis
- Interactive dashboard
- REST API for historical metrics
- Anomaly detection for unusual ecosystem activity

---

## Tech Stack

**Language:** Python 3.12  
**Automation:** GitHub Actions  
**APIs:** GitHub REST API, PyPI JSON API  
**Storage:** JSON-based historical datasets  
**Analytics:** Python  
**CI/CD:** GitHub Actions

---

## License

This project is intended for educational, analytical, and open-source ecosystem research purposes.