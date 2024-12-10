import datetime
from typing import Optional
from Util import generate_unique_id
from ..db import users_table, access_log_table, thread_logger, get_user

def get_all_logs(user_id:str = None):
    thread_logger.info(f"Attempting to retrieve logs {" for {user_id}." if user_id else None}")
    FilterExpression = "UserID = :user_id" if user_id else None
    ExpressionAttributeValues= {":user_id": user_id} if user_id else None
    
    response = access_log_table.scan(FilterExpression=FilterExpression, ExpressionAttributeValues=ExpressionAttributeValues)
    thread_logger.info(f"Get_All_Logs RESPONSE ->>>> {response.get('Items')}")
    return response.get('Items')


def register_entry(tag_id: str, user_id: Optional[str], bucket_name: Optional[str], file_object: Optional[str]):
    entry = {
        "LogID": str(generate_unique_id()),
        "TagID": tag_id,
        "UserID": user_id,
        "Bucket": bucket_name,
        "FileObject": file_object,
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