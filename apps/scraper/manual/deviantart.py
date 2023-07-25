from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class DeviantArt(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("DeviantART", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, "html.parser")
            name = None
            name_element = soup.find("div", class_="_33syq")
            if name_element is not None:
                name = name_element.get_text(strip=True)
            avatar = None
            avatar_element = soup.select_one(f'img[alt="{username}\'s avatar"]')
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            extra_metadata = {}
            for span in soup.find_all("span", class_="_1thFP"):
                extra_metadata[span.contents[-1].text.strip().lower()] = self.numberize(
                    span.select_one(':first-child').text.strip() or 0
                )
            if avatar is None and not extra_metadata:  # Dummy Page
                return None
            return {
                "name": name,
                "avatar": avatar,
                **extra_metadata
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None

    def user_check(self, username, tracked_usernames):
        """Prevent duplicate records for usernames with underscores."""
        if username.replace("_", "") in (user.replace("_", "") for user in tracked_usernames):
            return False
        return True
