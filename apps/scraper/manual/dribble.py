from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Dribble(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Dribbble", *args, **kwargs)
        self.base_url += '/about'

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, "html.parser")
            name = None
            name_element = soup.find("h1", class_="masthead-profile-name")
            if name_element is not None:
                name = name_element.text.strip()
            location = None
            location_element = soup.find("p", class_="masthead-profile-locality")
            if location_element is not None:
                location = location_element.text.strip()
            bio = None
            bio_element = soup.find("div", class_="bio")
            if bio_element is not None:
                bio = bio_element.p.text.strip()
            avatar = None
            image_element = soup.find("img", class_="profile-avatar")
            if image_element is not None:
                avatar = image_element["src"]
            member_since = None
            member_since_element = soup.find("p", class_="info-item created")
            if member_since_element is not None:
                member_since = member_since_element.span.text.strip()
            extra_metadata = {}
            skills_element = soup.find("ul", class_="skills-list")
            if skills_element is not None:
                extra_metadata["skills"] = [
                    skill.text.strip()
                    for skill in skills_element.find_all("a")
                ]
            return {
                'name': name,
                'location': location,
                'bio': bio,
                'avatar': avatar,
                'member_since': member_since,
                **extra_metadata
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
