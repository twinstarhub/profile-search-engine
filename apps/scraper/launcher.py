from __future__ import annotations

import asyncio
from functools import wraps
from itertools import chain
import os
import time
from typing import TYPE_CHECKING

import aiohttp

from apps.scraper.manual import (
    Behance, DeviantArt, Dribble, Github, LastFM,
    Pornhub, Replit, Telegram,
    # OnlyFans
)
from apps.scraper.special import (
    CodeAcademy, Reddit,
    TikTok, Tumblr, Youtube,
    # Facebook
)
from apps.ugen.generator import UserNameGenerator
from apps.utils import analyse, Cacher, save_profiles

if TYPE_CHECKING:
    from apps.scraper.base_model import Platform


def ensure_session(func):
    """Ensure that the session is initialized before calling the function."""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120.0),
                connector=aiohttp.TCPConnector(limit=None)
            )
        return await func(self, *args, **kwargs)
    return wrapper


class RequestTransformer:
    """A class to transform the requests to a specific format."""

    @classmethod
    def flatten_response(cls, response: dict) -> list:
        """Flatten the response."""
        response = response or {}
        return list(chain.from_iterable(response.values()))

    @classmethod
    def dictify_requests(cls, req_map):
        mapping = {}
        for key, sent_reqs in req_map.items():
            payload = {}
            for req in sent_reqs:
                if req.request_log[0]['status'] == 200:
                    continue
                if req.request_log[0]['status'] not in payload:
                    payload[req.request_log[0]['status']] = []
                payload[req.request_log[0]['status']].append(req.request_log[0])
            mapping[key] = payload
        return mapping


class AsyncScrapper:
    """A class to scrape multiple platforms asynchronously."""

    def __init__(self,
        use_cache: bool = True,
        analyse_results: bool = True,
        save_data: bool = True,
        test_mode: bool = False
    ):
        self.cacher = None
        if use_cache:
            self.cacher = Cacher(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=os.getenv('REDIS_PORT', 6379),
                password=os.getenv('REDIS_PASSWORD', None)
            )
        self.analyse_results = analyse_results
        self.save_data = save_data
        self.test_mode = test_mode
        self.platforms = [
            Pornhub, LastFM, CodeAcademy, TikTok,
            Tumblr, Reddit, Youtube, Behance, DeviantArt,
            Dribble, Github, Replit, Telegram
        ]
        if self.test_mode:
            self.cacher = None
            self.save_data = False
            self.analyse_results = True
            self.platforms = [
                CodeAcademy, Tumblr, Reddit, Youtube,
                Behance, DeviantArt, Dribble, Replit, Telegram
            ]
        self.platform_mapping = {
            platform().name: platform
            for platform in self.platforms
        }
        # Use the same session to scrape all the platforms.
        # This will reduce the overhead of reinitializing the session.
        self.session = None

    async def _iterator(self, key: list[str]) -> tuple[type[Platform], str]:
        """
        Iterate over the platforms and usernames.
        If the key is found in the cache, get the usernames from the cache.
        Otherwise, generate the usernames.

        :param cacher: The cacher instance.
        :param key: The key to search for in the cache.
        :return: A generator of platform and username pairs.
        """
        results = []
        if self.cacher is not None:
            async with self.cacher as cacher:
                results = await cacher.get(key)
        results = RequestTransformer.flatten_response(results)
        if results:
            for result in results:
                platform_cls = self.platform_mapping[result['platform']]
                username = result['username']
                yield platform_cls, username
        else:
            usernames = UserNameGenerator(*key, 4000).updated_username_generator()
            if self.test_mode:
                usernames = usernames[:100]
            # For each username, create a task for each platform.
            for username in usernames:
                for platform_cls in self.platforms:
                    yield platform_cls, username


    @ensure_session
    async def scrape_account(self, key: list[str]):
        """Scrape a single account."""
        st_time = time.monotonic()
        tasks = []
        sent_reqs = []

        async with self.session as session:
            async for platform_cls, username in self._iterator(key):
                platform: Platform = platform_cls(session=session)
                task = asyncio.create_task(platform.scrape(username))
                sent_reqs.append(platform)
                tasks.append(task)
            # Wait for all the tasks to complete.
            responses = await asyncio.gather(*tasks)
        print(f"Scraped [{len(sent_reqs)}] sources in [{time.monotonic() - st_time:.2f}s].")
        if self.cacher is not None:
            records = RequestTransformer.dictify_requests({Cacher.to_key(key): sent_reqs})
            async with self.cacher as cacher:
                await cacher.insert(key, records[Cacher.to_key(key)])
        if self.analyse_results:
            analyse(sent_reqs)
        # Filter out the empty responses.
        filtered_responses = [response for response in responses if response]
        if self.save_data:
            save_profiles(filtered_responses)
        return filtered_responses


    @ensure_session
    async def retry_429_links(self):
        """Retry the links that returned 429."""
        st_time = time.monotonic()
        tasks = []
        sent_reqs = []
        req_map = {}

        async with self.cacher as cacher:
            async with self.session as session:
                results = await cacher.search_by_status(429)
                # Then search for the value in the values
                for key, requests in results.items():
                    req_map[key] = []
                    for value in requests:
                        platform_cls = self.platform_mapping[value['platform']]
                        username = value['username']
                        platform: Platform = platform_cls(session=session)
                        task = asyncio.create_task(platform.scrape(username))
                        sent_reqs.append(platform)
                        req_map[key].append(platform)
                        tasks.append(task)
                # Wait for all the tasks to complete.
                responses = await asyncio.gather(*tasks)
            print(f"Retried [{len(sent_reqs)}] sources in [{time.monotonic() - st_time:.2f}s].")
            mapping = RequestTransformer.dictify_requests(req_map)
            await cacher.bulk_update_by_status(mapping)
            filtered_responses = [response for response in responses if response]
            if self.save_data:
                save_profiles(filtered_responses)
