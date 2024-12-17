from .user import get_user
from ..db import users_table, thread_logger


def register_card_to_user(user_id: str, card_id: str):
    user = get_user(user_id)
    thread_logger.info(f"register_card_to_user:get_user ->> {user}")
    if user:
        user["CardID"] = str(card_id)
        users_table.put_item(Item=user)
        return True
    return False


def get_user_by_card(card_id: str, get_all=False):
    response = users_table.scan(
        FilterExpression="CardID = :card_id",
        ExpressionAttributeValues={":card_id": str(card_id)},
    )
    items = response.get("Items", [])
    if get_all:
        return items
    return items[0] if items else None


def remove_all_links_to_card(card_id: str):
    users = get_user_by_card(str(card_id), get_all=True)
    for user in users:
        user["CardID"] = None
        users_table.put_item(Item=user)
