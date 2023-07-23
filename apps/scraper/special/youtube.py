import os
from urllib.parse import urlencode
from apps.scraper.base_model import Platform

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyA5mLlnwmzjTZujIB1l4bOsoU9Rp1Yz4so")


class Youtube(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Youtube", *args, **kwargs)
        params = {
            "part": "snippet,statistics",
            "key": YOUTUBE_API_KEY
        }
        self.base_url = f"{self.base_url}?{urlencode(params)}&forUsername={{}}"

    async def get_data(self, response):
        try:
            data = await response.json()
            return data
        except Exception:
            return None

    def parse_response(self, username, response):
        try:
            if "items" in response:
                item = response["items"][0]
                # Extract the desired information from the response
                return {
                    "description": item["snippet"]["description"],
                    "custom_url": item["snippet"]["customUrl"],
                    "avatar": item["snippet"]["thumbnails"].get("high", item["snippet"]["thumbnails"]["medium"])["url"],
                    "country": item["snippet"].get("country"),
                    "subscriber_count": self.numberize(item["statistics"]["subscriberCount"]),
                    "view_count": self.numberize(item["statistics"]["viewCount"]),
                    "video_count": self.numberize(item["statistics"]["videoCount"])
                }
            else:
                return None
        except KeyError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
