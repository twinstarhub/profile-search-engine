from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Tumblr(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Tumblr", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            # Full name
            full_name_element = soup.find('h1', class_='vfPi2')
            full_name = full_name_element.text if full_name_element else None
            # Username
            username_element = soup.find('a', class_='Da0mp')
            username = username_element.text if username_element else None
            # Website
            website_element = soup.find('a', class_='Da0mp BSUG4')
            website = website_element['href'] if website_element else None
            # Bio
            bio_element = soup.find('div', class_='a15fm mjAxW')
            bio = bio_element.text if bio_element else None
            # Avatar
            avatar_element = soup.select_one('img[alt="Avatar"]')
            avatar = avatar_element.get('src') if avatar_element else None
            # Posts
            posts = [
                fig.find('img').get('srcset').split(', ')[-1].split()[0]
                for fig in soup.find_all('figure')
            ]
            if posts:
                posts = posts[:10]
            else:
                posts = None
            return {
                'full_name': full_name,
                'username': username,
                'avatar': avatar,
                'website': website,
                'bio': bio,
                'posts': posts
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
