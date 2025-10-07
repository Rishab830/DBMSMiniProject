from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["HealthCareSystem"]

print(db['Dietary_Information'].distinct('Food_Aversions'))