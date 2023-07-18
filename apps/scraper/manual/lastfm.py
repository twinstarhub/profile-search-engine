from bs4 import BeautifulSoup
from apps.scraper.base_model import Platform


class LastFM(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("last.fm", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')

            # Extract the title
            title_element = soup.find('h1', class_='header-title')
            title = title_element.find('a').text.strip()
            # Extract the scrobble since
            scrobble_since_element = soup.find('span', class_='header-scrobble-since')
            scrobble_since = scrobble_since_element.text.strip().split('since ')[1]

            # Extract the display name
            display_name_element = soup.find('span', class_='header-title-display-name')
            display_name = display_name_element.text.strip()
            # Extract the scrobbles
            scrobbles_element = soup.find('div', class_='header-metadata-display')
            scrobbles = scrobbles_element.find('a').text.strip()

            return {
                "title": title,
                "scrobble_since": scrobble_since,
                "display_name": display_name,
                "scrobbles": scrobbles
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
