import pymongo

client = None
database = None

def connect_to_database():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["cmp408"]