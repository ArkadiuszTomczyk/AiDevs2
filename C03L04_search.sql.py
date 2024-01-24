import json
import uuid

from requests import get

from store.collection import Collection, Document
from utils.ai_devs_api_client import get_auth_token, get_task, post_response

ROWS_TO_SAVE = 300
COLLECTION_NAME = 'search-archiwe-1'
INIT_COLLECTION = False


class Metadata:
    def __init__(self, url, date):
        self.url = url
        self.date = date


def map_to_documents(data):
    data = data[:ROWS_TO_SAVE]
    documents = []
    for row in data:
        metadata = Metadata(
            url=row['url'],
            date=row['date']
        )
        temp_doc = Document(
            id=uuid.uuid4(),
            content=f'{row["title"]}\n\n{row["info"]}',
            metadata=metadata
        )
        documents.append(temp_doc)
        pass
    return documents


def init_collection(c: Collection):
    archive = get('https://unknow.news/archiwum.json')
    archive_object = map_to_documents(archive.json())
    c.load_documents(archive_object)


collection = Collection(COLLECTION_NAME)
if INIT_COLLECTION:
    init_collection(collection)

token = get_auth_token('search')
task = get_task(token)
response = collection.search(task['question'], 1)
post_response(response[0].payload['url'], token)
