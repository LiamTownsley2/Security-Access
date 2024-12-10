import datetime
import random
import time
from typing import Optional

from ..db import users_table, access_log_table, thread_logger

def generate_unique_id():
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000, 9999)
    return f"{timestamp}{random_number}"

def register_user(name: str):
    user_id = generate_unique_id()
    users_table.put_item(
        Item={
            "UserID": user_id,
            "Name": name,
        }
    )
    return user_id

def delete_user(user_id: str):
    response = users_table.delete_item(
        Key={"UserID": user_id}
    )
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200

def get_user(user_id: str):
    thread_logger.info(f"Attempting to retrieve user with UserID: {user_id}")
    response = users_table.get_item(Key={"UserID": user_id})
    thread_logger.info(f"Get_User RESPONSE ->>>> {response.get('Item')}")
    return response.get('Item')

def register_entry(tag_id: str, user_id: Optional[str]):
    entry = {
        "LogID": str(generate_unique_id()),
        "TagID": tag_id,
        "UserID": user_id,
        "Time": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    access_log_table.put_item(Item=entry)

    if user_id:
        user = get_user(user_id)
        if user:
            user['LastScanned'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            users_table.put_item(Item=user)


def get_entries_count(user_id: str):
    response = access_log_table.scan(
        FilterExpression="UserID = :user_id",
        ExpressionAttributeValues={":user_id": user_id}
    )
    return len(response.get('Items', []))