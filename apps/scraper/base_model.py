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
        self.session = None

    def __repr__(self) -> str:
        return f"<Platform: {self.name}>"

    async def send_request(self, username: str, *args, **kwargs):
        """Send a request to the platform."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(),
                connector=aiohttp.TCPConnector(limit=None)
            )
        if not kwargs.get("proxy") and self.proxies:
            kwargs["proxy"] = random.choice(self.proxies)
        try:
            resp = await self.session.get(
                self.base_url.format(username),
                **kwargs
            )
            return resp
        except (aiohttp.ClientConnectorError, asyncio.TimeoutError):
            return None

    async def scrape(self, username: str, *args, **kwargs):
        """Perform the scraping for the platform."""
        response = await self.send_request(username, *args, **kwargs)
        if response is None:
            return {}
        return {
            "title": username,
            "link": self.base_url.format(username),
            "snippet": json.dumps(self.parse_response(await response.text()))
        }


    @abstractmethod
    def parse_response(self, response):
        """Parse the response from the platform."""
        pass
