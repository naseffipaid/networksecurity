from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://mymachines0_db_user:RXUWlv6G3kKBrDUl@cluster0.pzk1ofm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server   RXUWlv6G3kKBrDUl
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

   