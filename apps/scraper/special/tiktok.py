from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class TikTok(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("TikTok", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name_element = soup.find('h2', class_='tiktok-1d3qdok-H2ShareSubTitle')
            following_count_element = soup.find('strong', {'data-e2e': 'following-count'})
            follower_count_element = soup.find('strong', {'data-e2e': 'followers-count'})
            user_bio_element = soup.find('h2', class_='tiktok-vdfu13-H2ShareDesc')
            link_element = soup.find('span', class_='tiktok-847r2g-SpanLink')
            avatar_element = soup.select_one('img[class*="ImgAvatar"]')
        
            name = name_element.get_text(strip=True) if name_element else None
            following_count = self.numberize(
                following_count_element.get_text(strip=True) or 0
            ) if following_count_element else None
            follower_count = self.numberize(
                follower_count_element.get_text(strip=True) or 0
            ) if follower_count_element else None
            user_bio = user_bio_element.get_text(strip=True) if user_bio_element else None
            link = link_element.get_text(strip=True) if link_element else None
            avatar = None
            if avatar_element:
                avatar = avatar_element.get('src')
        
            return {
                "name": name,
                "avatar": avatar,
                "following_count": following_count,
                "follower_count": follower_count,
                "bio": user_bio,
                "link": link
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
