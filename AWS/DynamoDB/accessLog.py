import datetime
from typing import Optional
from Util import generate_unique_id
from ..db import users_table, access_log_table, thread_logger, get_user
import os

def get_all_logs(user_id: str = None):
    thread_logger.info("Attempting to retrieve logs.")
    
    if user_id:
        thread_logger.info(f"\tSpecified User ID: {user_id}")
    
    if user_id:
        FilterExpression = "UserID = :user_id"
        ExpressionAttributeValues = {":user_id": str(user_id)}
    else:
        FilterExpression = None
        ExpressionAttributeValues = None
    
    response = access_log_table.scan(
        FilterExpression=FilterExpression, 
        ExpressionAttributeValues=ExpressionAttributeValues
    )
    
    thread_logger.info(f"Get_All_Logs RESPONSE ->>>> {response.get('Items')}")
    return response.get('Items', [])

def register_entry(tag_id: str, user_id: Optional[str], file_object: Optional[str]):
    entry = {
        "LogID": str(generate_unique_id()),
        "TagID": str(tag_id),
        "UserID": str(user_id),
        "Bucket": os.getenv("S3_BUCKET_NAME"),
        "FileObject": str(file_object),
        "Time": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    access_log_table.put_item(Item=entry)

    if user_id:
        user = get_user(user_id)
        if user:
            user['LastScanned'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            users_table.put_item(Item=user)

def get_entries_count(user_id: str):
    user_logs = get_all_logs(user_id)
    return len(user_logs)