from bs4 import BeautifulSoup
from apps.scraper.base_model import Platform


class Pornhub(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Pornhub", *args, **kwargs)

    def parse_response(self, name, response):
        """Parse the response from Pornhub."""
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name = None
            name_element = soup.find('div', class_="profileUserName")
            if name_element is not None:
                name = name_element.find('a').text.strip()
            avatar = None
            avatar_element = soup.find('img', id='getAvatar')
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            bio = None
            bio_element = soup.find('p', class_='aboutMeText')
            if bio_element is not None:
                bio = bio_element.text.strip()
            subscriber_count = None
            friends_count = None
            videos_count = None
            subs_info_element = soup.find('ul', class_='subViewsInfoContainer')
            res = []
            if subs_info_element:
                res = [
                    self.numberize(li.find('span', class_='number').text.strip() or 0)
                    for li in subs_info_element.find_all('li')
                ]
            if len(res) == 3:
                subscriber_count, friends_count, videos_count = res
            more_info = soup.find('dl', class_='moreInformation')
            more_metadata = {}
            if more_info is not None:
                more_metadata = {
                    self._get_key(info_elem): self.numberize(info_elem.text.strip())
                    for info_elem in more_info.find_all('dd')
                }
            return {
                "name": name,
                "avatar": avatar,
                "bio": bio,
                "subscriber_count": subscriber_count,
                "friends_count": friends_count,
                "videos_count": videos_count,
                **more_metadata
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": name})
            return None

    @staticmethod
    def _get_key(info_elem):
        """Get the key from the info element."""
        return info_elem.find_previous_sibling('dt').text.strip().replace(':', '')
