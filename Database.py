import pymongo

client = None
database = None
collection = None

def connect_to_database():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client["cmp408"]
        collection = database["users"]
    except Exception as e:
        print(f"Exception occured whilst connecting to MongoDB: {e}")

def get_user_by_card(card_id:str):
    user = collection.find_one({"card_id": card_id}, {})
    return user