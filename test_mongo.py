# test_mongo.py
import os, sys
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import certifi
from urllib.parse import quote_plus

load_dotenv(find_dotenv())
uri = os.getenv("MONGO_DB_URL")
print("MONGO_DB_URL present:", bool(uri))
print("URI preview:", (uri[:120] + "...") if uri else None)

try:
    # force connection attempt (short timeout for fast feedback)
    client = MongoClient(uri, serverSelectionTimeoutMS=7000, tlsCAFile=certifi.where())
    info = client.server_info()    # forces immediate connection / raises on failure
    print("Connected. server version:", info.get("version"))
    print("Databases:", client.list_database_names())
except Exception as e:
    print("CONNECT ERROR:", type(e).__name__, "-", e)
    sys.exit(1)
