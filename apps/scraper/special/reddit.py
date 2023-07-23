import os
from bs4 import BeautifulSoup
from datetime import datetime

from apps.scraper.base_model import Platform

ZENROW_API_KEY = os.getenv("ZENROW_API_KEY", "7b26afa746c5aa85d837d1440875a2c44279615a")

class Reddit(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Reddit", *args, **kwargs)
        # self.proxies = [f'http://{ZENROW_API_KEY}:@proxy.zenrows.com:8001']

    def parse_response(self, username, response):
        """Parse the response from Reddit."""
        try:
            soup = BeautifulSoup(response, 'html.parser')
            # Find the element containing the karma
            karma_element = soup.find("span", id="profile--id-card--highlight-tooltip--karma")
            karma_text = None  # Assign a default value
            if karma_element is not None:
                karma_text = karma_element.text.strip()
            # Find the element containing the cake day
            cake_day_element = soup.find("span", id="profile--id-card--highlight-tooltip--cakeday")
            cake_day_text = None  # Assign a default value
            account_age = None  # Assign a default value
            if cake_day_element is not None:
                cake_day_text = cake_day_element.text.strip()
                self.logger.debug("Cake Day: %s", cake_day_text, extra={"username": username})
                # Calculate the age of the account
                current_year = datetime.now().year
                cake_day = datetime.strptime(cake_day_text, "%B %d, %Y")
                account_age = current_year - cake_day.year
            avatar = None  # Assign a default value
            avatar_element = soup.find("img", alt="User avatar")
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            return {
                "avatar": avatar,
                "karma": karma_text,
                "cake_day": cake_day_text,
                "account_age": account_age
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
