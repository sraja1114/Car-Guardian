from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv()

cluster_user = os.getenv("cluster_user")
cluster_password = os.getenv("cluster_password")
cluster_uri = os.getenv("cluster_uri")
uri = f"mongodb+srv://{cluster_user}:{cluster_password}@{cluster_uri}/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
except Exception as e:
    print(e)


# Access the 'sample_supplies' database
sample_supplies_db = client.sample_supplies

# Access the 'sales' collection within the 'sample_supplies' database
sales_collection = sample_supplies_db.sales

# Read a single entry from the 'sales' collection
entry = sales_collection.find_one()

# Print the retrieved entry
print(entry)