from github import get_pull_requests, filter_prs_by_date
from email_build import build_list_to_email, send_email


def main():
    prs = get_pull_requests()
    filtered_prs_by_date = filter_prs_by_date(prs)
    body_email = build_list_to_email(filtered_prs_by_date)
    send_email("projectdcd@outlook.com", "projectdcd@gmail.con", body_email)


def lambda_handler(event, context):
    main()
