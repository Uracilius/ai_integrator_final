import chromadb
import json
import os
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction

def load_config(config_path='config.json'):
    """Load configuration from a JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, config_path)
    with open(config_file_path, 'r') as file:
        return json.load(file)

def connect(config):
    """Connect to ChromaDB and return the specified collection."""
    try:
        image_loader = ImageLoader()
        embedding_function = OpenCLIPEmbeddingFunction()
        chroma_client = chromadb.HttpClient(host=config['host'], port=config['port'])
        collection = chroma_client.get_or_create_collection(name=config['collection_name'], embedding_function=embedding_function, data_loader=image_loader)
        return collection
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {str(e)}")

def save_new_user(face_data, name):
    """Save an object to the specified collection."""
    try:
        collection = connect(load_config())
        response = collection.update(
            ids=['1'],
            images=[face_data],
            metadatas=[{'name': name}]
        )
        return "Friend with name " + name + " has been added to the database."
    except Exception as e:
        raise Exception("There has been an error with connection to the database: " + str(e))

def hard_reset():
    """Perform a hard reset on the collection, deleting all entries."""
    try:
        collection = connect(load_config())
        response = collection.delete()
        return "Database reset successfully."
    except Exception as e:
        raise Exception("Failed to reset database: " + str(e))

def get_first_thing_in_collection():
    """Retrieve the first item in the collection."""
    try:
        collection = connect(load_config())
        response = collection.peek()
        return response
    except Exception as e:
        raise Exception("Failed to retrieve the first item: " + str(e))

def get_closest_face(face_data):
    """Find and return the closest matching face in the collection."""
    try:
        collection = connect(load_config())
        response = collection.query(
            query_images=[face_data],
            n_results=1)
        if response['metadatas'] != [[None]]:
            return response
        raise Exception("No matching faces found.")
    except Exception as e:
        raise Exception("Failed to find the closest face: " + str(e))
