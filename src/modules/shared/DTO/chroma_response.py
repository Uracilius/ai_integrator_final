class ChromaResponse:
    def __init__(self, response_data):
        self.ids = response_data.get('ids', [])
        self.distances = response_data.get('distances', [])
        self.embeddings = response_data.get('embeddings')
        self.metadatas = response_data.get('metadatas', [])
        self.documents = response_data.get('documents', [])
        self.uris = response_data.get('uris')
        self.data = response_data.get('data')

    def get_first_item(self):
        return {
            "id": self.ids[0][0] if self.ids else None,
            "distance": self.distances[0][0] if self.distances else None,
            "metadata": self.metadatas[0][0] if self.metadatas else None,
            "document": self.documents[0][0] if self.documents else None,
        }
