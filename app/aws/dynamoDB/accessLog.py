import datetime
import logging
import os

from util.general import generate_unique_id

from .tables import access_log_table, users_table
from .user import get_user

thread_logger = logging.getLogger("ThreadLogger")


def get_all_logs(user_id: str = None):
    thread_logger.info("Attempting to retrieve logs.")
    response = None
    if user_id:
        thread_logger.info(f"\tSpecified User ID: {user_id}")
        response = access_log_table.scan(
            FilterExpression="UserID = :user_id",
            ExpressionAttributeValues={":user_id": str(user_id)},
        )
    else:
        response = access_log_table.scan()

    thread_logger.info(f"Get_All_Logs RESPONSE ->>>> {response.get('Items')}")
    return response.get("Items", [])


def register_entry(tag_id: str, user_id: str = None, file_object: str = None):
    entry = {
        "LogID": str(generate_unique_id()),
        "TagID": tag_id,
        "UserID": str(user_id),
        "Bucket": os.getenv("S3_BUCKET_NAME"),
        "FileObject": file_object,
        "Time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    access_log_table.put_item(Item=entry)

    if user_id:
        user = get_user(user_id)
        if user:
            user["LastScanned"] = datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
            users_table.put_item(Item=user)


def get_entries_count(user_id: str):
    user_logs = get_all_logs(user_id)
    return len(user_logs)
