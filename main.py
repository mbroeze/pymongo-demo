from pymongo import MongoClient
import requests

mongo_client = MongoClient()

data = requests.get("https://statsapi.web.nhl.com/api/v1/schedule").json()

db = mongo_client.nhl_schedule
print(f"DB Name: {db.name}")


db.nhl_schedule.insert_one(data)

for item in db.nhl_schedule.find():
    print(item)


