import os
import requests
from urllib.parse import urlencode
from apps.scraper.base_model import Platform

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyA5mLlnwmzjTZujIB1l4bOsoU9Rp1Yz4so")


class Youtube(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Youtube", *args, **kwargs)
        params = {
            "part": "snippet,contentDetails,statistics",
            "key": YOUTUBE_API_KEY
        }
        self.base_url = f"{self.base_url}?{urlencode(params)}&forUsername={{}}"

    async def get_data(self, response):
        data = await response.json()
        return data

    def parse_response(self, username, response):
        try:
            if "items" in response:
                item = response["items"][0]
                # Extract the desired information from the response
                return {
                    "username": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "subscriber_count": item["statistics"]["subscriberCount"],
                    "view_count": item["statistics"]["viewCount"],
                    "video_count": item["statistics"]["videoCount"]
                }
            else:
                return None
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None

# def scrape_user_profile(api_key, username):
#     url = f"https://www.googleapis.com/youtube/v3/channels"
#     params = {
#         "part": "snippet,contentDetails,statistics",
#         "forUsername": username,
#         "key": api_key
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     if "items" in data:
#         item = data["items"][0]
#         # Extract the desired information from the response
#         profile_data = {
#             "username": item["snippet"]["title"],
#             "description": item["snippet"]["description"],
#             "subscriber_count": item["statistics"]["subscriberCount"],
#             "view_count": item["statistics"]["viewCount"],
#             "video_count": item["statistics"]["videoCount"]
#         }
#         return profile_data

#     return None

# # API key obtained from the Google Developer Console
# api_key = "AIzaSyA5mLlnwmzjTZujIB1l4bOsoU9Rp1Yz4so"

# # List of usernames to scrape
# usernames = ["pewdiepie", "tseries", "checkgate", "setindia", "WWEFanNation", "corycotton", "zeemusiccompany", "EdSheeran", "NewOnNetflix", "BuzzFeedVideo", "NatGeoWild"]  # Add more usernames as needed

# for username in usernames:
#     profile_data = scrape_user_profile(api_key, username)
#     if profile_data:
#         # Process the profile data as needed
#         print(profile_data)
#     else:
#         print(f"Profile data not found for username: {username}")