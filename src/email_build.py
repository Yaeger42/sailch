import boto3
from botocore.exceptions import ClientError

from typing import List, Dict, Any
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

LOGGER = logging.getLogger(__name__)


def build_list_to_email(filtered_prs: Dict[str, Any]) -> str:
    if not filtered_prs:
        LOGGER.info("Empty filtered prs")
        return ""
    to_send_list: List[Dict[str, Any]] = []
    for entry in filtered_prs:
        dict_entry: Dict[str, Any] = {}
        dict_entry["url"] = entry["html_url"]
        dict_entry["state"] = entry["state"]
        dict_entry["locked"] = entry["locked"]
        dict_entry["created_at"] = entry["created_at"]
        if entry["assignees"]:
            dict_entry["assignees"] = [
                assignee["login"] for assignee in entry["assignees"]
            ]
        else:
            dict_entry["assignees"] = []
        dict_entry["created_by"] = entry["user"]["login"]
        dict_entry["requested_reviewers"] = []
        if entry["requested_reviewers"]:
            dict_entry["requested_reviewers"] = [
                user["login"] for user in entry["requested_reviewers"]
            ]
        else:
            dict_entry["requested_reviewers"] = []
        to_send_list.append(dict_entry)
    body_email_str = "Here's the list of issues from today and 1 week ago \n"
    for issue in to_send_list:
        (
            body_email_str
            + f"""
        URL: {issue["url"]} 
        Status: {issue["state"]}
        IsLocked: {str(issue["locked"])} 
        Creation date: {issue["created_at"]}
        """
        )
        if issue["assignees"]:
            body_email_str += f"""\nAssignees: {' '.join(issue["assignees"])}"""
        if issue["requested_reviewers"]:
            body_email_str += (
                f"""\nRequested reviewers: {' '.join(issue["requested_reviewers"])}"""
            )
    return body_email_str


def send_email(sender_email: str, recipient_email: str, body: str):
    ses_client = boto3.client("ses")
    message = {
        "Subject": {"Data": "Daily PRs Report"},
        "Body": {"Text": {"Data": body}},
    }
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={"ToAddresses": [recipient_email]},
            Message=message,
        )
    except ClientError as e:
        LOGGER.error(f'Failed to send email: {e.response["Error"]["Message"]}')
    else:
        LOGGER.info("Email sent successfully")
        LOGGER.info(f'Message ID: {response["MessageId"]}')
