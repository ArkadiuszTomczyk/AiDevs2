from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from utils.chat_gpt_api_client import get_embedding


class Document:
    def __init__(self, id, content='', metadata={}):
        self.id = str(id)
        self.content = content
        self.metadata = metadata


class Collection:

    def __init__(self, name):
        self.name = name
        self._qdrant_client = QdrantClient(host='localhost', port=6333)
        self._init_collections()

    def load_documents(self, docs: list):
        if all(isinstance(element, str) for element in docs):
            raise Exception('Invalid format')
        points = []
        count = len(docs)
        current = 0
        for doc in docs:
            current += 1
            print(f'Generating embedding for {current} of {count} documents')
            self.load_document(doc)
            embedding = get_embedding(doc.content)
            point = PointStruct(
                    id=str(doc.id),
                    vector=embedding,
                    payload={'url': doc.metadata.url, 'date': doc.metadata.date}
                )
            points.append(point)
        print('Start inserting points to qdrant')
        self._qdrant_client.upsert(
            collection_name=self.name,
            wait=True,
            points=points
        )
        print('End inserting points to qdrant')

    def load_document(self, doc: Document):
        embedding = get_embedding(doc.content)
        self._qdrant_client.upsert(
            collection_name=self.name,
            points=[
                PointStruct(
                    id=str(doc.id),
                    vector=embedding,
                    payload={'url': doc.metadata.url, 'date': doc.metadata.date}
                )
            ]
        )

    def search(self, phrase, limit):
        embedding = get_embedding(phrase)
        return self._qdrant_client.search(
            collection_name=self.name,
            query_vector=embedding,
            limit=limit
        )

    def _init_collections(self):
        collections = self._qdrant_client.get_collections()
        exists = any(collection.name == self.name for collection in collections.collections)
        if exists:
            return
        self._qdrant_client.create_collection(
            collection_name=self.name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE, on_disk=True)
        )
