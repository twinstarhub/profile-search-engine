"""A wrapper to cache data in Redis."""
import os
from typing import Any
import redis.asyncio as redis
from redis.commands.json.path import Path


class Cacher:
    """A wrapper to cache data in Redis."""

    def __init__(self, host: str, port: int, password: str):
        """Initialize the Cacher."""
        self.host = host
        self.port = int(port)
        self.password = password
        self.client = None

    async def connect(self):
        """Connect to Redis."""
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=True,
            auto_close_connection_pool=False
        )

    async def disconnect(self):
        """Disconnect from Redis."""
        await self.client.close()

    async def get(self, key: list[str]):
        """Get a value from Redis asynchronously."""
        key = self.to_key(key)
        return await self.client.json().get(key)

    async def insert(self, key: list[str], values: list[dict[str, Any]]):
        """Writes to Redis asynchronously."""
        if isinstance(key, list):
            key = self.to_key(key)
        await self.client.json().set(key, Path.root_path(), values)

    async def search_by_status(self, status: str | int) -> list[dict]:
        """Search all the rquests for a specific status."""
        # First get all the keys
        keys = await self.client.keys('*')
        # Then get the values for those keys
        records = await self.client.json().mget(keys, Path.root_path())
        results = {}
        for key, record in zip(keys, records):
            results[key] = record[str(status)]
        return results

    async def update_by_status(self, key: str, status: str | int, records: list[dict]):
        """Update the value of a specific status."""
        # First get the value for the key
        value = await self.client.json().get(key, Path.root_path())
        # Then update the value
        value[str(status)] = records
        # Then set the value back to the key
        await self.client.json().set(key, Path.root_path(), value)

    async def bulk_update_by_status(self, mapping: dict[str, str | list[dict]]):
        """Update the value of a specific status."""
        async with self.client.pipeline(transaction=True) as pipe:
            for key, payload in mapping.items():
                for status, records in payload.items():
                    pipe.json().set(key, f'$.{status}', records)
            await pipe.execute()

    async def __aenter__(self):
        """Connect to Redis."""
        await self.connect()
        return self

    async def __aexit__(self, *args):
        """Disconnect from Redis."""
        await self.disconnect()

    @staticmethod
    def to_key(args):
        """Convert arguments to a Redis key."""
        return ':'.join(args)
