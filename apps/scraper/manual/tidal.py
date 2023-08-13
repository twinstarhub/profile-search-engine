from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform

class Tidal(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Tidal", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name = None
            name_element = soup.find('div', class_='name')
            if name_element is not None:
                name = name_element.text.strip()
            bio = None
            bio_element = soup.find('div', class_='bio')
            if bio_element is not None:
                bio = bio_element.text.strip()
            location = None
            location_element = soup.find('div', class_='location')
            if location_element is not None:
                location = location_element.text.strip()  
            followers = None
            followers_element = soup.find('div', class_='followers')
            if followers_element is not None:
                followers = followers_element.text.strip()  
            following = None
            following_element = soup.find('div', class_='following')
            if following_element is not None:
                following = following_element.text.strip()     
            return {
                "name": name,
                "location": location,
                "followers": followers,
                "following": following,
                "bio": bio,
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
