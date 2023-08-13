from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Pinterest(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Pinterest", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name = None
            name_element = soup.find('h2', class_='ProfileHeader-name')
            if name_element is not None:
                name = name_element.text.strip()
            bio = None
            bio_element = soup.find('div', class_='ProfileHeader-about')
            if bio_element is not None:
                bio = bio_element.text.strip()
            followers = None
            followers_element = soup.find('p', class_='ProfileCard-line-fVO e2e-Profile-company')
            if followers_element is not None:
                followers = followers_element.text.strip()
            following = None
            following_element = soup.find('span', class_='e2e-Profile-location')
            if following_element is not None:
                following = following_element.text.strip()
            avatar = None
            avatar_element = soup.find('img', class_='ProfileImage')
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            return {
                "name": name,
                "avatar": avatar,
                "followers": followers,
                "following": following,
                "bio": bio,
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
