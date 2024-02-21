from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
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


def build_list_to_email(filtered_prs: Dict[str, Any]) -> List[Dict[str, Any]]:
    if filtered_prs:
        to_send_list: List[Dict[str, Any]] = []
        for entry in filtered_prs:
            dict_entry = {}
            dict_entry["url"] = entry["html_url"]
            dict_entry["state"] = entry["state"]
            dict_entry["locked"] = entry["locked"]
            dict_entry["created_at"] = entry["created_at"]
            dict_entry["assignees"] = entry["assignees"]
            dict_entry["created_by"] = entry["user"]["login"]
            dict_entry["requested_reviewers"] = []
            if entry["requested_reviewers"]:
                dict_entry["requested_reviewer"] = [
                    user["login"] for user in entry["requested_reviewers"]
                ]
            to_send_list.append(dict_entry)
        return dict_entry
    return []


prs = get_pull_requests()
filtered = filter_prs_by_date(prs)
listed = build_list_to_email(filtered)
print(listed)
