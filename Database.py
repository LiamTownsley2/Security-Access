import pymongo

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

def get_user_by_card(card_id:int):
    if collection is None: return False
    user = collection.find_one({"card_id": str(card_id)})
    return user