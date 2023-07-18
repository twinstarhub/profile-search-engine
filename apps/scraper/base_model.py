from abc import ABC, abstractmethod
import asyncio
import json
import os
import random
import aiohttp


dir_name = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(dir_name)
platform_metadata = os.path.join(working_dir, 'urlfinder/resources/platform_list.json')
with open(platform_metadata, "r") as file:
    PLATFORM_METADATA = json.load(file)


class Platform(ABC):
    """An Abstract Base Class which provides a skeleton for all scraping platforms."""
    def __init__(self, name, *args, **kwargs):
        self.name: str = name
        self.base_url: str = PLATFORM_METADATA[name]["url"]
        self.headers = []
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
                **kwargs
            )
            # Add the sent request to the log.
            self.request_log.append(self.base_url.format(username))
            return resp
        except (aiohttp.ClientConnectorError, asyncio.TimeoutError):
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
            "snippet": json.dumps(self.parse_response(username, await response.text()))
        }


    @abstractmethod
    def parse_response(self, username, response):
        """Parse the response from the platform."""
        pass
