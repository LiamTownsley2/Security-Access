import pymongo

client, database, collection = None, None, None

def connect_to_database():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["cmp408"]
    collection = database["users"]
    
def get_user_by_card(card_id:str):
    user = collection.find_one({"card_id": card_id}, {})
    return user