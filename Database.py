import pymongo
from bson.objectid import ObjectId
from datetime import datetime
client = None
database = None
users_col, access_log_col = None

def connect_to_database():
    global client, database, users_col, access_log_col
    try:
        client = pymongo.MongoClient("mongodb://2.tcp.eu.ngrok.io:13446/")
        database = client["cmp408"]
        users_col = database["users"]
        access_log_col = database["access-log"]

    except Exception as e:
        print(f"Exception occured whilst connecting to MongoDB: {e}")

def register_user(name:str):
    user = users_col.insert_one({ "name": name, "card_id": None })
    return user

def register_card_to_user(_id:ObjectId, card_id:str):
    user = get_user(_id)
    user['card_id'] = card_id
    result = users_col.replace_one({ "_id": _id }, user)
    return result

def register_entry(_id:ObjectId, tag_id:str):
    user = get_user(_id)
    user['last_scanned'] = datetime.now()
    users_col.replace_one({ "_id": _id }, user)
    access_log_col.insert_one({ "tag_id": tag_id, "user_id": _id, "time": datetime.now() })
def get_user(_id:ObjectId):
    user = users_col.find_one({ "_id": _id })
    return user

def get_user_by_card(card_id:int):
    if users_col is None: return False
    user = users_col.find_one({"card_id": str(card_id)})
    return user