"""MongoDB Connector"""
from __future__ import annotations
from functools import wraps
import os
import threading
import time
from typing import TYPE_CHECKING

from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError, ConnectionFailure

from apps.utils.custom_logger import MongoLogger

if TYPE_CHECKING:
    import logging


def ensure_connection(func):
    """Ensure that the connection to MongoDB is established before executing the function."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapper function."""
        if not self.client:
            self.logger.warning('MongoDB connection not established. Skipping DB operations.')
            return
        try:
            return func(self, *args, **kwargs)
        except Exception as exp:
            self.logger.error(f'Error while executing {func.__name__}:\n{exp}')
    return wrapper


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
        self.logger: logging.Logger = MongoLogger()

    def connect(self):
        """Connect to MongoDB."""
        uri = f"mongodb+srv://{self.username}:{self.password}@{self.host}/?retryWrites=true&w=majority"
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
        except Exception:
            self.logger.warning('Unable to connect to MongoDB.')

    def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client is not None:
            self.client.close()

    @ensure_connection
    def get_collection(self, collection: str):
        """Get a collection from MongoDB."""
        return self.client[self.database][collection]

    @ensure_connection
    def drop_collection(self, collection: str):
        """Drop a collection from MongoDB."""
        return self.client[self.database].drop_collection(collection)

    @ensure_connection
    def create_document(self, collection: str, document: dict):
        """Create a document in MongoDB."""
        return self.client[self.database][collection].insert_one(document)

    @ensure_connection
    def create_documents(self, collection: str, documents: list[dict]):
        """Create multiple documents in MongoDB."""
        return self.client[self.database][collection].insert_many(documents)

    @ensure_connection
    def update_document(self, collection: str, query: dict, document: dict):
        """Update a document in MongoDB."""
        return self.client[self.database][collection].update_one(query, document)

    @ensure_connection
    def update_documents(self, collection: str, query: dict, document: dict):
        """Update multiple documents in MongoDB."""
        return self.client[self.database][collection].update_many(query, document)

    @ensure_connection
    def delete_document(self, collection: str, query: dict):
        """Delete a document in MongoDB."""
        return self.client[self.database][collection].delete_one(query)

    @ensure_connection
    def delete_documents(self, collection: str, query: dict):
        """Delete multiple documents in MongoDB."""
        return self.client[self.database][collection].delete_many(query)

    @ensure_connection
    def find_document(self, collection: str, query: dict):
        """Find a document in MongoDB."""
        return self.client[self.database][collection].find_one(query)

    @ensure_connection
    def find_documents(self, collection: str, query: dict):
        """Find multiple documents in MongoDB."""
        return list(self.client[self.database][collection].find(query))

    @ensure_connection
    def get_all_documents(self, collection: str):
        """Get all documents from MongoDB."""
        return self.find_documents(collection, {})

    @ensure_connection
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
            self.logger.success(f"Updated Profiles in [{time.monotonic() - st_time:.2f}]s")
            self.logger.info(f"Inserted {result.upserted_count} new records.")
            self.logger.info(f"Modified {result.modified_count} existing records.")
        except BulkWriteError as bwe:
            self.logger.error(f"Bulk write error: {bwe.details}")

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
