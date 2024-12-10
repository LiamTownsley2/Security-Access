from user import get_user
from ..db import users_table, access_log_table, thread_logger

def register_card_to_user(user_id: str, card_id: str):
    user = get_user(user_id)
    thread_logger.info(f"register_card_to_user:get_user ->> {user}")
    if user:
        user['CardID'] = card_id
        users_table.put_item(Item=user)
        return True
    return False

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