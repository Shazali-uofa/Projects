import sys
from pymongo import MongoClient
import json

# If there are not 2 command line arguments given it raises an error
if len(sys.argv)!=3:
    print("Usage: python3 load-json.py <filename.json> <port>")
    sys.exit(1)

# Creating a program which imports the json file into the database
file_name=sys.argv[1]
port=int(sys.argv[2])
client = MongoClient(f"mongodb://localhost:{port}") 
print("The client connection was successfull")

# Created Data base for Miniproject2
db=client["291db"]

# If there exist an article collection drop it 
if "articles" in db.list_collection_names():
    print("This already exists so dropping your existing database")
    db.articles.drop()

# If there is no article then create one
collection=db.articles

# Read JSON FILE in small batches

batch_size=5000
batch=[]
count=0

with open(file_name, "r",encoding="utf-8") as f:
    for line in f:
        # Skip the empty lines and fill the batches
        if line.strip():
            try:
                batch.append(json.loads(line))
            except:
                continue


        
        if len(batch)==batch_size:
            collection.insert_many(batch)
            count+=len(batch)
            batch=[]


if batch:
    collection.insert_many(batch)
    count+=len(batch)
    batch=[]
print(f"Collection 'articles' successfully created with {count} documents.")
print("Done!")