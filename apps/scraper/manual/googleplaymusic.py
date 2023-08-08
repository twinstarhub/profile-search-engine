from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class GooglePlayMusic(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("GooglePlayMusic", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name = None
            name_element = soup.find('span', class_='full-name')
            if name_element is not None:
                name = name_element.text.strip()
            bio = None
            bio_element = soup.find('div', class_='bio')
            if bio_element is not None:
                bio = bio_element.text.strip()
            location = None
            location_element = soup.find('span', class_='location')
            if location_element is not None:
                location = location_element.text.strip()     
            return {
                "name": name,
                "location": location,
                "followers": followers,
                "playlists": playlists,
                "tracks": tracks,
                "bio": bio,
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
