from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Soundcloud(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Soundcloud", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name = None
            name_element = soup.find('h1', class_='profileHeaderInfo__userName')
            if name_element is not None:
                name = name_element.text.strip()
            bio = None
            bio_element = soup.find('div', class_='profileHeaderInfo__additionalInfo')
            if bio_element is not None:
                bio = bio_element.text.strip()
            followers = None
            followers_element = soup.find('a', class_='followers_count')
            if followers_element is not None:
                followers = followers_element.text.strip()
            tracks = None
            tracks_element = soup.find('a', class_='tracks_count')
            if tracks_element is not None:
                tracks = tracks_element.text.strip()
            location = None
            location_element = soup.find('div', class_='profileHeaderInfo__additionalInfo').find('span', class_='location')
            if location_element is not None:
                location = location_element.text.strip()     
            playlists = None
            playlists_element = soup.find('span', class_='playlists_count')
            if playlists_element is not None:
                playlists = playlists_element.text.strip()
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
