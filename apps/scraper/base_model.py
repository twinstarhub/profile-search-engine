from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
import json
import os
import random
from typing import TYPE_CHECKING

import aiohttp

from apps.utils.custom_logger import PlatformLogger

if TYPE_CHECKING:
    import logging


dir_name = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(dir_name)
platform_metadata = os.path.join(working_dir, 'urlfinder/resources/platform_list.json')
with open(platform_metadata, "r") as file:
    PLATFORM_METADATA = json.load(file)


class LoggerSetter(type):
    """A metaclass which sets the logger for the class."""
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls.logger: logging.Logger = PlatformLogger(new_cls.__name__)
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
        except Exception:
            self.request_log.append({
                "username": username,
                "url": self.base_url.format(username),
                "status": 500,
                "platform": self.name
            })
            return None

    async def scrape(self, username: str, *args, **kwargs):
        """Perform the scraping for the platform."""
        try:
            response = await self.send_request(username, *args, **kwargs)
            # If the response is None or status is 40x or 50x, then the request failed.
            if response is None or response.status >= 400:
                return {}
            return {
                "title": username,
                "link": self.base_url.format(username),
                "platform": self.name,
                "snippet": await self.get_snippet(username, response)
            }
        except Exception:
            return {}

    async def get_snippet(self, username, response):
        """Get the snippet from the response."""
        response = await self.get_data(response)
        if response is None:
            return None
        snippet = self.parse_response(username, response) or {}
        missing_fields = [key for key, value in snippet.items() if value is None]
        if len(missing_fields) == len(snippet):
            return None
        elif missing_fields:
            self.logger.warning(
                "Following fields not found for user: [%s]",
                ", ".join(missing_fields),
                extra={"username": username}
            )
        return snippet

    async def get_data(self, response):
        """Get the data from the response."""
        try:
            data = await response.text()
            return data
        except Exception:
            return None

    @abstractmethod
    def parse_response(self, username, response):
        """Parse the response from the platform."""
        pass

    @staticmethod
    def numberize(text):
        """Convert the text to a number."""
        if text is None:
            return None
        if isinstance(text, (int, float)):
            return text
        try:
            text = text.replace(',', '')
            if "k" in text.lower():
                return int(float(text.replace('k', '')) * 1000)
            elif "m" in text.lower():
                return int(float(text.replace('m', '')) * 1000000)
            elif "b" in text.lower():
                return int(float(text.replace('b', '')) * 1000000000)
            elif "." in text:
                return float(text)
            return int(text)
        except ValueError:
            return text
