import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
# Global variables to hold the database and collection handles
db = None
collection = None

def initialize_mongo_db(config_path='config.json'):
    """
    Initializes the MongoDB client, database, and collection using settings from the config.json file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, config_path)
    
    global db, collection

    with open(config_file_path, 'r') as file:
        config = json.load(file)
    
    client = MongoClient(config['mongo_uri'])
    db = client.context
    #HARDCODED COLLECTION NAME
    collection = db[config['mongo_collection_name']]


def add_mongo_data(text):
    """
    Add a new entry to the MongoDB collection.
    :param text: The text to store in the collection.
    :return: The ID of the newly added item.
    """
    document = {'text': text}
    result = collection.insert_one(document)
    return str(result.inserted_id)

def get_mongo_data(document_id):
    """
    Retrieve an entry from the MongoDB collection based on its ID.
    :param document_id: The ID of the document to retrieve.
    :return: The document retrieved from the collection.
    """
    document = collection.find_one({'_id': ObjectId(document_id)})
    return document


def rollback_mongo_data(document_id):
    try:
        collection.delete_one({'_id': ObjectId(document_id)})
    except Exception as e:
        print(f"Failed to rollback MongoDB data: {str(e)}")
