from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Telegram(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Telegram", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name_element = soup.find('div', class_='tgme_page_title')
            description_element = soup.find('div', class_='tgme_page_description')
            avatar_element = soup.find('img', class_='tgme_page_photo_image')
            name = name_element.get_text(strip=True) if name_element else None
            description = description_element.get_text(strip=True) if (description_element and name) else None
            avatar = avatar_element.get('src') if avatar_element else None
            return {
                "name": name,
                "description": description,
                "avatar": avatar
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
