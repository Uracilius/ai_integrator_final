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
    image_loader = ImageLoader()
    embedding_function = OpenCLIPEmbeddingFunction()
    chroma_client = chromadb.HttpClient(host=config['host'], port=config['port'])
    collection = chroma_client.get_or_create_collection(name=config['collection_name'], embedding_function=embedding_function, data_loader=image_loader)
    return collection

def save_image(face_data):
    """Save an object to the specified collection."""
    collection = connect(load_config())
    response = collection.add(
        ids=['2'],
        images=[face_data],
        metadatas=[{'name': 'Ainur'}]
    )
    return response

def hard_reset ():
    collection = connect(load_config())
    response = collection.delete()
    return response

def get_first_thing_in_collection():
    collection = connect(load_config())
    response = collection.peek()
    return response

def get_closest_face(face_data):
    collection = connect(load_config())
    response = collection.query(
        query_images=[face_data],
        n_results=1)
    return response