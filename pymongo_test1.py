# this script shows how to use the official Python driver to create a connection
# to an atlas cluster - could change connection string to connect locally too.
import os

import bson

import insert1_doc
import insert_many_doc
import pprint
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId




load_dotenv()

# use a connection string to connect to the database
#MONGO_DB_URI = "mongodb+srv://stevealbury:bUNjDyrUCQijKyZN@developmentenvironments.q74ao.mongodb.net/?retryWrites=true&w=majority&appName=developmentEnvironments0"

#Rather than doing it directly it's better to do it
# using an environment variable
MONGO_DB_URI = os.environ['MONGO_LOCAL_URI']
client = MongoClient(MONGO_DB_URI)

for db_name in client.list_database_names():
    print(db_name)
db = client['cities']
collection = db['cities']
result = collection.insert_one(insert1_doc.new_doc)

new_id = result.inserted_id
print(f"The object id of the 1 inserted document is > {new_id}")

result_many = collection.insert_many(insert_many_doc.new_many_doc)

new_ids = result_many.inserted_ids
num_docs = str(len(new_ids))
print(f"number of new docs inserted > " + num_docs)
print(f"The object id of the {num_docs} inserted documents is > {new_ids}")

document_to_find = collection.find_one({'_id': ObjectId(new_id)})
pprint.pprint(document_to_find)

#build a quesry pattern
# I have used a regex but can be any mongo query such $eq, $gt, $lt etc
regx = bson.regex.Regex('Big Ski')
document_to_find_many = collection.find({"name": {'$regex': 'Big Ski'}}, {"name": 1,"_id": 1})

num_docs = 0
for doc in document_to_find_many:
    num_docs += 1
    pprint.pprint(doc)

print(f"number of docs found > {num_docs}")



# remember to close the client!!
client.close()


