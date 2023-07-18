import asyncio
from typing import TYPE_CHECKING

import aiohttp
from apps.scraper.manual.onlyfans import OnlyFans
from apps.scraper.manual.pornhub import Pornhub

if TYPE_CHECKING:
    from apps.scraper.base_model import Platform


PLATFORMS = [OnlyFans, Pornhub]


async def scrape_account(usernames: list[str]):
    """Scrape a single account."""
    tasks = []
    # Use the same session to scrape all the platforms.
    # This will reduce the overhead of reinitializing the session.
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(),
        connector=aiohttp.TCPConnector(limit=None)
    ) as session:
        # For each username, create a task for each platform.
        for username in usernames:
            for platform in PLATFORMS:
                platform: Platform = platform(session=session)
                task = asyncio.create_task(platform.scrape(username))
                tasks.append(task)
        # Wait for all the tasks to complete.
        responses = await asyncio.gather(*tasks)
    # Filter out the empty responses.
    return [response for response in responses if response]
