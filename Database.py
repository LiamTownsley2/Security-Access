import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional

client = None
database = None
users_col, access_log_col = None, None

def connect_to_database():
    global client, database, users_col, access_log_col
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client["cmp408"]
        users_col = database["users"]
        access_log_col = database["access-log"]

    except Exception as e:
        print(f"Exception occured whilst connecting to MongoDB: {e}")

def register_user(name:str):
    user = users_col.insert_one({ "name": name, "card_id": None })
    return user

def delete_user(_id:ObjectId):
    result =users_col.delete_one({ "_id": _id })
    return result.acknowledged and result.deleted_count > 0

def register_card_to_user(_id:ObjectId, card_id:str):
    user = get_user(_id)
    user['card_id'] = card_id
    result = users_col.replace_one({ "_id": _id }, user)
    return result

def register_entry(tag_id:str, _id:ObjectId):
    access_log_col.insert_one({ "tag_id": tag_id, "user_id": _id, "time": datetime.now() })
    if _id is not None:
        user = get_user(_id)
        user['last_scanned'] = datetime.now()
        users_col.replace_one({ "_id": _id }, user)

def get_user(_id:ObjectId):
    user = users_col.find_one({ "_id": _id })
    return user

def get_entries_count(_id:ObjectId):
    return access_log_col.count_documents({ "user_id": _id })

def get_user_by_card(card_id:int):
    if users_col is None: return False
    user = users_col.find_one({"card_id": str(card_id)})
    return user

def get_users_by_card(card_id:int):
    if users_col is None: return False
    users = list(users_col.find({"card_id": str(card_id)}))
    return users

def remove_all_links_to_card(card_id:int):
    if users_col is None: return False
    users = get_users_by_card(card_id)
    for user in users:
        user['card_id'] = None
        users_col.replace_one({ "_id": user['_id'] }, user)