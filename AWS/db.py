import boto3
import os
import logging

dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), aws_session_token=os.getenv('AWS_SESSION_TOKEN'), region_name=os.getenv('AWS_REGION'))
users_table = dynamodb.Table('Users')
access_log_table = dynamodb.Table('AccessLog')

thread_logger = logging.getLogger("ThreadLogger")

from .DynamoDB.user import get_user, delete_user, generate_unique_id, register_user, get_all_users, edit_user
from .DynamoDB.cards import get_user_by_card, register_card_to_user, remove_all_links_to_card
from .DynamoDB.accessLog import register_entry, get_entries_count, get_all_logs

__all__ = [
    "dynamodb",
    "users_table",
    "access_log_table",
    
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
    "get_all_logs"
]