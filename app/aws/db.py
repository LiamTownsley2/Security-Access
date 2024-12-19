import boto3
import os

from .dynamoDB.user import (
    get_user,
    delete_user,
    generate_unique_id,
    register_user,
    get_all_users,
    edit_user,
)
from .dynamoDB.cards import (
    get_user_by_card,
    register_card_to_user,
    remove_all_links_to_card,
)
from .dynamoDB.accessLog import register_entry, get_entries_count, get_all_logs

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_REGION"),
)

__all__ = [
    "dynamodb",
    # user
    "get_user",
    "delete_user",
    "generate_unique_id",
    "register_user",
    "get_all_users",
    "edit_user",
    # Cards
    "get_user_by_card",
    "register_card_to_user",
    "remove_all_links_to_card",
    # Access Log
    "get_entries_count",
    "register_entry",
    "get_all_logs",
]
