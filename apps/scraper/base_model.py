from abc import ABC, ABCMeta, abstractmethod
import asyncio
import json
import os
import random
import aiohttp

from apps.utils.custom_logger import get_logger


dir_name = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(dir_name)
platform_metadata = os.path.join(working_dir, 'urlfinder/resources/platform_list.json')
with open(platform_metadata, "r") as file:
    PLATFORM_METADATA = json.load(file)


class LoggerSetter(type):
    """A metaclass which sets the logger for the class."""
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls.logger = get_logger(new_cls.__name__)
        return new_cls


class AbstractLoggerSetter(LoggerSetter, ABCMeta):
    pass

class Platform(ABC, metaclass=AbstractLoggerSetter):
    """An Abstract Base Class which provides a skeleton for all scraping platforms."""
    def __init__(self, name, *args, **kwargs):
        self.name: str = name
        self.base_url: str = PLATFORM_METADATA[name]["url"]
        self.headers = [
            ("User-Agent", " ".join([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/114.0.0.0 Safari/537.36"])
            )
        ]
        self.proxies = []
        self.session = kwargs.get("session")
        self.request_log = []

    def __repr__(self) -> str:
        return f"<Platform: {self.name}>"

    async def send_request(self, username: str, *args, **kwargs):
        """Send a request to the platform."""
        # For special usecases where we want a unique session for the platform.
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(),
                connector=aiohttp.TCPConnector(limit=None)
            )
        # Select a random proxy if one is not provided.
        if not kwargs.get("proxy") and self.proxies:
            kwargs["proxy"] = random.choice(self.proxies)
        try:
            # Send the request.
            resp = await self.session.get(
                self.base_url.format(username),
                verify_ssl=False,
                **kwargs
            )
            # Add the sent request to the log.
            self.request_log.append({
                "username": username,
                "url": self.base_url.format(username),
                "status": resp.status,
                "platform": self.name
            })
            return resp
        except (
            aiohttp.ClientConnectorError,
            aiohttp.ClientOSError,
            aiohttp.ServerDisconnectedError,
            asyncio.TimeoutError,
            ConnectionResetError
        ):
            self.request_log.append({
                "username": username,
                "url": self.base_url.format(username),
                "status": 500,
                "platform": self.name
            })
            return None

    async def scrape(self, username: str, *args, **kwargs):
        """Perform the scraping for the platform."""
        response = await self.send_request(username, *args, **kwargs)
        # If the response is None, then the request failed.
        if response is None:
            return {}
        return {
            "title": username,
            "link": self.base_url.format(username),
            "platform": self.name,
            "snippet": json.dumps(self.parse_response(username, await self.get_data(response)))
        }

    async def get_data(self, response):
        """Get the data from the response."""
        data = await response.text()
        return data

    @abstractmethod
    def parse_response(self, username, response):
        """Parse the response from the platform."""
        pass
