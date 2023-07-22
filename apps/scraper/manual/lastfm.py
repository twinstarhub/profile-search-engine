from bs4 import BeautifulSoup
from apps.scraper.base_model import Platform


class LastFM(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("last.fm", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            # Extract the title
            title = None
            title_element = soup.find('h1', class_='header-title')
            if title_element is not None:
                title = title_element.find('a').text.strip()
            # Extract the avatar
            avatar = None
            avatar_element = soup.select_one('img[alt*="Avatar"]')
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            # Extract the scrobble since
            scrobble_since = None
            scrobble_since_element = soup.find('span', class_='header-scrobble-since')
            if scrobble_since_element is not None:
                scrobble_since = scrobble_since_element.text.strip().split('since ')[1]
            # Extract the display name
            display_name = None
            display_name_element = soup.find('span', class_='header-title-display-name')
            if display_name_element is not None:
                display_name = display_name_element.text.strip()
            # Extract the scrobbles
            scrobbles = None
            artists = None
            metadata_element = soup.find('ul', class_='header-metadata')
            res = []
            if metadata_element is not None:
                res = [
                    self.numberize(elem.text.strip() or 0)
                    for elem in metadata_element.find_all('a')
                ]
            if len(res) == 2:
                scrobbles, artists = res
            return {
                "title": title,
                "avatar": avatar,
                "scrobble_since": scrobble_since,
                "display_name": display_name,
                "scrobbles": scrobbles,
                "artists": artists
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
