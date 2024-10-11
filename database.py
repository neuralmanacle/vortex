from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://arjunshenoy23:OXnpTwUdvwXcRzBr@cluster0.wgymm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(MONGO_URI)

try:

    client.admin.command("ismaster")
    print("MongoDB connected successfully!")
except ConnectionFailure:
    print("Could not connect to MongoDB")

db = client["vortex"]

items_collection = db["items"]
clock_in_collection = db["clock_in_records"]