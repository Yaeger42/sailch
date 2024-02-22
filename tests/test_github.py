from datetime import datetime, timedelta
from src.github import filter_prs_by_date
from freezegun import freeze_time


@freeze_time("2024-02-20 03:21:34", tz_offset=-4)
def test_filter_prs_by_date():
    prs = [
        {"created_at": "2024-02-19T14:49:40Z"},
        {"created_at": "2024-02-20T14:49:40Z"},
        {"created_at": "2024-02-21T14:49:40Z"},
    ]
    today = datetime.today()
    one_week_ago = today - timedelta(days=7)
    filtered_prs = filter_prs_by_date(prs)
    assert len(filtered_prs) == 3
    for pr in filtered_prs:
        assert datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ") >= one_week_ago
