import boto3
import datetime
import random
from typing import Optional
import os

print(f"Access Key: {os.getenv('AWS_ACCESS_KEY_ID')}\nSecret Key: {os.getenv('AWS_SECRET_ACCESS_KEY')}\nRegion:{os.getenv('AWS_REGION')}")
dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), aws_session_token=os.getenv('AWS_SESSION_TOKEN'), region_name=os.getenv('AWS_REGION'))
users_table = dynamodb.Table('Users')
access_log_table = dynamodb.Table('AccessLog')

def generate_unique_id():
    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    random_number = random.randint(1000, 9999)
    return f"{timestamp}{random_number}"

def register_user(name: str):
    response = users_table.put_item(
        Item={
            "UserID": str(generate_unique_id()),
            "Name": name,
            "CardID": None
        }
    )
    return response

def delete_user(user_id: str):
    response = users_table.delete_item(
        Key={"UserID": user_id}
    )
    return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200

def register_card_to_user(user_id: str, card_id: str):
    user = get_user(user_id)
    if user:
        user['CardID'] = card_id
        users_table.put_item(Item=user)
        return True
    return False

def register_entry(tag_id: str, user_id: Optional[str]):
    entry = {
        "LogID": str(generate_unique_id()),  # Generate unique log ID
        "TagID": tag_id,
        "UserID": user_id,
        "Time": datetime.datetime.now(datetime.timezone().utc).isoformat()
    }
    access_log_table.put_item(Item=entry)

    if user_id:
        user = get_user(user_id)
        if user:
            user['LastScanned'] = datetime.datetime.now(datetime.timezone().utc).isoformat()
            users_table.put_item(Item=user)

def get_user(user_id: str):
    response = users_table.get_item(Key={"UserID": user_id})
    return response.get('Item')

def get_entries_count(user_id: str):
    response = access_log_table.scan(
        FilterExpression="UserID = :user_id",
        ExpressionAttributeValues={":user_id": user_id}
    )
    return len(response.get('Items', []))

def get_user_by_card(card_id: str):
    response = users_table.scan(
        FilterExpression="CardID = :card_id",
        ExpressionAttributeValues={":card_id": card_id}
    )
    items = response.get('Items', [])
    return items[0] if items else None

def get_users_by_card(card_id: str):
    response = users_table.scan(
        FilterExpression="CardID = :card_id",
        ExpressionAttributeValues={":card_id": card_id}
    )
    return response.get('Items', [])

def remove_all_links_to_card(card_id: str):
    users = get_users_by_card(card_id)
    for user in users:
        user['CardID'] = None
        users_table.put_item(Item=user)