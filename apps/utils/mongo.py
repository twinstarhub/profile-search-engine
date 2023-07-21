"""MongoDB Connector"""
import os
import threading
import time

from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError


class MongoDBConnector:
    """MongoDB Connector."""

    def __init__(self,
        host: str = os.getenv('MONGO_HOST', 'localhost'),
        username: str = os.getenv('MONGO_USERNAME', None),
        password: str = os.getenv('MONGO_PASSWORD', None),
        database: str = os.getenv('MONGO_DATABASE', 'Trustle')
    ):
        """Initialize the MongoDB Connector."""
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.client = None

    def connect(self):
        """Connect to MongoDB."""
        uri = f"mongodb+srv://{self.username}:{self.password}@{self.host}/?retryWrites=true&w=majority"
        self.client = MongoClient(uri, server_api=ServerApi('1'))


    def disconnect(self):
        """Disconnect from MongoDB."""
        self.client.close()

    def get_collection(self, collection: str):
        """Get a collection from MongoDB."""
        return self.client[self.database][collection]

    def drop_collection(self, collection: str):
        """Drop a collection from MongoDB."""
        return self.client[self.database].drop_collection(collection)

    def create_document(self, collection: str, document: dict):
        """Create a document in MongoDB."""
        return self.client[self.database][collection].insert_one(document)

    def create_documents(self, collection: str, documents: list[dict]):
        """Create multiple documents in MongoDB."""
        return self.client[self.database][collection].insert_many(documents)

    def update_document(self, collection: str, query: dict, document: dict):
        """Update a document in MongoDB."""
        return self.client[self.database][collection].update_one(query, document)

    def update_documents(self, collection: str, query: dict, document: dict):
        """Update multiple documents in MongoDB."""
        return self.client[self.database][collection].update_many(query, document)

    def delete_document(self, collection: str, query: dict):
        """Delete a document in MongoDB."""
        return self.client[self.database][collection].delete_one(query)

    def delete_documents(self, collection: str, query: dict):
        """Delete multiple documents in MongoDB."""
        return self.client[self.database][collection].delete_many(query)

    def find_document(self, collection: str, query: dict):
        """Find a document in MongoDB."""
        return self.client[self.database][collection].find_one(query)

    def find_documents(self, collection: str, query: dict):
        """Find multiple documents in MongoDB."""
        return self.client[self.database][collection].find(query)

    def bulk_upsert(self, collection: str, documents: list[dict]):
        """Bulk upsert documents in MongoDB."""
        st_time = time.monotonic()
        bulk_operations = []
        for record in documents:
            link_filter = {"link": record["link"]}
            bulk_operations.append(
                UpdateOne(filter=link_filter, update={"$set": record}, upsert=True)
            )

        try:
            result = self.client[self.database][collection].bulk_write(bulk_operations)
            print(f"Updated Profiles in [{time.monotonic() - st_time:.2f}]s")
            print(f"Inserted {result.upserted_count} new records.")
            print(f"Modified {result.modified_count} existing records.")
        except BulkWriteError as bwe:
            print(f"Bulk write error: {bwe.details}")

    def __enter__(self):
        """Enter the context manager."""
        self.connect()
        return self

    def __exit__(self, *args):
        """Exit the context manager."""
        self.disconnect()
        return False


def save_profiles(data: dict):
    """Save the scraped data to MongoDB."""
    def save(data):
        with MongoDBConnector() as connector:
            connector.bulk_upsert('Profiles', data)
    mongo_thread = threading.Thread(target=save, args=(data,), name='MongoDB')
    mongo_thread.start()
