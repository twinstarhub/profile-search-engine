import os
import re
from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform

ZENROW_API_KEY = os.getenv("ZENROW_API_KEY", "7b26afa746c5aa85d837d1440875a2c44279615a")
LAST_ACTIVE_PATT = re.compile(r'Last active.+\s(\d+\syears)')

class CodeAcademy(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Codecademy", *args, **kwargs)
        # self.proxies = [f'http://{ZENROW_API_KEY}:@proxy.zenrows.com:8001']

    def parse_response(self, username, response):
        """Parse the response from Codecademy."""
        try:
            soup = BeautifulSoup(response, 'html.parser')
            # Find the element containing the fullname
            fullname_element = soup.find("p", {'data-testid': "full-name-section"})
            karma_text = None  # Assign a default value
            if fullname_element is not None:
                karma_text = fullname_element.text.strip()
            else:  # Dummy page
                return None
            # Find the element containing the joined day
            date_section = soup.find('div', attrs={'data-testid': 'date-section'})
            last_active = None
            join_date = None
            if date_section is not None:
                for p_tag in date_section.find_all('p'):
                    if "Joined" in p_tag.text:
                        join_date = p_tag.text.strip().replace("Joined ", "")
                        
                    if "Last active" in p_tag.text:
                        last_active = LAST_ACTIVE_PATT.search(p_tag.text).group(1)
            avatar = None
            avatar_element = soup.select_one('img[alt~="avatar"]')
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            return {
                "fullname": karma_text,
                "avatar": avatar,
                "join_day": join_date,
                "last_active": last_active
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
