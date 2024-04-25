import chromadb
import json
import os
from .exceptions import DataNotFoundException
def load_config(config_path='config.json'):
    """Load configuration from a JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, config_path)
    with open(config_file_path, 'r') as file:
        return json.load(file)

def connect(config):
    """Connect to ChromaDB and return the context_tags collection."""
    try:
        chroma_client = chromadb.HttpClient(host=config['host'], port=config['port'])
        collection = chroma_client.get_or_create_collection(name=config['chroma_collection_name'])
        return collection
    except Exception as e:
        raise Exception(f"Failed to connect to Chroma's context tags database: {str(e)}")

def get_chroma_closest_data(tags, userId):
    """Query the closest conversation data for given tags and user ID."""
    try:
        collection = connect(load_config())
        response = collection.query(
            query_texts=tags,
            n_results=1,
            where={"name": userId}
        )
        # Check if the response is empty or does not meet expected conditions
        if not response or not len(response.get('documents'))==1:  # Adjust depending on actual response structure
            raise DataNotFoundException("Failed to find any conversations for user ID: {}".format(userId))
        return response
    except DataNotFoundException as e:
        # You can handle known cases directly in the calling function
        raise e
    except Exception as e:
        # Handle other unexpected exceptions
        raise Exception("Failed to query data due to an error: " + str(e))
    
def add_chroma_data(id, tags, name):
    """Save an object to the specified collection."""
    try:
        collection = connect(load_config())
        tags_string = ', '.join(tags)
        response = collection.add(
            ids=str(id),
            documents=tags_string,
            metadatas={"name": name})
        return response
    except Exception as e:
        raise Exception("Failed to add conversation to database: " + str(e))

def hard_reset():
    """Perform a hard reset on the collection, deleting all entries."""
    try:
        collection = connect(load_config())
        response = collection.delete()
        return "Database reset successfully."
    except Exception as e:
        raise Exception("Failed to reset database: " + str(e))

def rollback_chroma_data(document_id):
    try:
        collection = connect(load_config())
        collection.delete(ids=document_id)
    except Exception as e:
        print(f"Failed to rollback Chroma data: {str(e)}")
