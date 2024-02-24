from src.email_build import build_list_to_email


def test_build_list_to_email():
    filtered_prs = [
        {
            "html_url": "https://github.com/docker/compose/pull/11525",
            "state": "open",
            "locked": False,
            "created_at": "2024-02-19T14:49:40Z",
            "assignees": [],
            "created_by": "ndeloof",
            "requested_reviewers": [],
            "user": {"login": "randomuser1"},
        },
        {
            "html_url": "https://github.com/docker/compose/pull/11513",
            "state": "open",
            "locked": False,
            "created_at": "2024-02-16T16:17:33Z",
            "assignees": [{"login": "glours"}],
            "created_by": "glours",
            "requested_reviewers": [],
            "user": {"login": "randomuser2"},
        },
    ]
    email_body = build_list_to_email(filtered_prs)
    assert email_body is not None
    assert email_body.startswith("Here's the list of issues")
