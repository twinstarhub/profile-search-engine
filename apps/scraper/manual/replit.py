from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Replit(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Replit.com", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, "html.parser")
            full_name_element = soup.find("div", class_="css-fx43vb")
            full_name = full_name_element.find("h1", class_="css-1iqbb3j").text.strip() if full_name_element else None
            follower_count = None
            following_count = None
            stats_element = soup.find("div", class_="css-1mcxwcz")
            res = []
            if stats_element:
                res = [
                    self.numberize((span.text.strip().split() or [0])[0])
                    for span in stats_element.find_all("span", class_="css-10z1dta")
                ]
            if len(res) == 2:
                follower_count, following_count = res
            avatar_element = soup.find("meta", property="og:image")
            avatar = avatar_element.get("content") if avatar_element else None
            return {
                "name": full_name,
                "avatar": avatar,
                "follower_count": follower_count,
                "following_count": following_count
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
