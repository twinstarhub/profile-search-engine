import asyncio
from typing import TYPE_CHECKING
from apps.scraper.manual.onlyfans import OnlyFans
from apps.scraper.manual.pornhub import Pornhub

if TYPE_CHECKING:
    from apps.scraper.base_model import Platform


PLATFORMS = [OnlyFans, Pornhub]


async def scrape_account(usernames: list[str]):
    """Scrape a single account."""
    tasks = []
    for username in usernames:
        for platform in PLATFORMS:
            platform: Platform = platform()
            task = asyncio.create_task(platform.scrape(username))
            tasks.append(task)
    responses = await asyncio.gather(*tasks)
    return [response for response in responses if response]
