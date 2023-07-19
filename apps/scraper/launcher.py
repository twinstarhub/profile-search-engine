import asyncio
import time
from typing import TYPE_CHECKING

import aiohttp
from apps.scraper.manual.behance import Behance
from apps.scraper.manual.deviantart import DeviantArt
from apps.scraper.manual.dribble import Dribble
from apps.scraper.manual.github import Github
from apps.scraper.manual.lastfm import LastFM
from apps.scraper.manual.onlyfans import OnlyFans
from apps.scraper.manual.pornhub import Pornhub
from apps.scraper.manual.replit import Replit
from apps.scraper.special.codecademy import CodeAcademy
from apps.scraper.special.facebook_ import Facebook
from apps.scraper.special.reddit import Reddit
from apps.scraper.special.tiktok import TikTok
from apps.scraper.special.tumblr import Tumblr
from apps.scraper.special.youtube import Youtube

if TYPE_CHECKING:
    from apps.scraper.base_model import Platform


PLATFORMS = [
    OnlyFans, Pornhub, LastFM, CodeAcademy, TikTok,
    Tumblr, Facebook, Reddit, Youtube, Behance, DeviantArt,
    Dribble, Github, Replit
]


async def scrape_account(usernames: list[str]):
    """Scrape a single account."""
    st_time = time.monotonic()
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
    print(f"Scraped [{len(usernames) * len(PLATFORMS)}] sources in [{time.monotonic() - st_time:.2f}s].")
    # Filter out the empty responses.
    return [response for response in responses if response]
