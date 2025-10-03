from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['HealthCareSystem']

for collection in db.list_collection_names():
    db[collection].drop()