from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform

class Deezer(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Deezer", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            user_info = soup.find('div', class_='user-info')
            name = None
            name_element = user_info.find('span', class_='fullname')
            if name_element is not None:
                name = name_element.text.strip()
            bio = None
            bio_element = user_info.find('div', class_='bio')
            if bio_element is not None:
                bio = bio_element.text.strip()
            location = None
            location_element = user_info.find('span', class_='location')
            if location_element is not None:
                location = location_element.text.strip()  
            stats = soup.find('div', class_='stats')
            followers = None
            followers_element = stats.find('span', class_='fans')
            if followers_element is not None:
                followers = followers_element.text.strip()  
            following = None
            following_element = stats.find('span', class_='artists')
            if following_element is not None:
                following = following_element.text.strip()     
            playlists = None
            playlists_element = stats.find('span', class_='playlists')
            if playlists_element is not None:
                playlists = playlists_element.text.strip()     
            tracks = None
            tracks_element = stats.find('span', class_='tracks')
            if tracks_element is not None:
                tracks = tracks_element.text.strip()     
            return {
                "name": name,
                "location": location,
                "followers": followers,
                "following": following,
                "tracks": tracks,
                "playlists": playlists,
                "bio": bio,
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
