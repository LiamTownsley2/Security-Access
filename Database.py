import pymongo
from bson.objectid import ObjectId

client = None
database = None
collection = None

def connect_to_database():
    global client, database, collection
    try:
        client = pymongo.MongoClient("mongodb://2.tcp.eu.ngrok.io:13446/")
        database = client["cmp408"]
        collection = database["users"]
    except Exception as e:
        print(f"Exception occured whilst connecting to MongoDB: {e}")

def register_user(name:str):
    user = collection.insert_one({ "name": name, "card_id": None })
    return user

def register_card_to_user(_id:ObjectId, card_id:str):
    user = get_user(_id)
    user['card_id'] = card_id
    result = collection.replace_one({ "_id": _id }, user)
    return result

def get_user(_id:ObjectId):
    user = collection.find_one({ "_id": _id })
    return user

def get_user_by_card(card_id:int):
    if collection is None: return False
    user = collection.find_one({"card_id": str(card_id)})
    return user