from typing import Dict, Any
from datetime import datetime, timedelta
import requests

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
URL = "https://api.github.com/repos/docker/compose/pulls"


def get_pull_requests() -> Dict[str, Any]:

    response = requests.get(url=URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []


def filter_prs_by_date(prs: Dict[str, Any]) -> Dict[str, Any]:
    today = datetime.today()
    one_week_ago = today - timedelta(days=7)
    if prs:
        dates_last_week = [
            entry
            for entry in prs
            if datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            >= one_week_ago
        ]
        return dates_last_week
    return {}
