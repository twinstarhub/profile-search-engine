from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Behance(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Behance", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, 'html.parser')
            name = None
            name_element = soup.find('h1', class_='ProfileCard-userFullName-ule')
            if name_element is not None:
                name = name_element.text.strip()
            role = None
            role_element = soup.find('p', class_='ProfileCard-line-fVO e2e-Profile-occupation')
            if role_element is not None:
                role = role_element.text.strip()
            company = None
            company_element = soup.find('p', class_='ProfileCard-line-fVO e2e-Profile-company')
            if company_element is not None:
                company = company_element.text.strip()
            location = None
            location_element = soup.find('span', class_='e2e-Profile-location')
            if location_element is not None:
                location = location_element.text.strip()
            extra_metadata = {}
            stats_element = soup.select_one('table[class*="UserInfo-userStats"]')
            if stats_element is not None:
                for stat in stats_element.find_all('tr'):
                    extra_metadata[
                        stat.find("td").text.strip().replace(" ", "_").lower()
                    ] = self.numberize(
                        stat.select_one('td[class*="UserInfo-statValue"]')
                            .text.strip() or 0
                    )
            avatar = None
            avatar_element = soup.find('img', class_='AvatarImage-avatarImage-PUL')
            if avatar_element is not None:
                avatar = avatar_element.get('src')
            social_element = soup.select_one('ul[class*="UserInfo-socialLinks"]')
            if social_element is not None:
                extra_metadata["social_links"] = [link.get("href") for link in social_element.find_all("a")]
            bio_element = soup.select_one('div[class*="UserInfo-bio"]')
            if bio_element is not None:
                extra_metadata["bio"] = bio_element.select_one('div[class*="ReadMore-content"]').text.strip()
            links_element = soup.select_one('div[class*="UserInfo-links"]')
            if links_element is not None:
                extra_metadata["links"] = [link.get("href") for link in links_element.find_all("a")]
            work_experience_element = soup.select('li[class*="UserInfo-workExperienceEntry"]')
            if work_experience_element is not None:
                extra_metadata["work_experience"] = [
                    {
                        "title": work.select_one('div[class*="UserInfo-workExperienceTitle"]').text.strip(),
                        "company": work.select_one('div[class*="UserInfo-workExperienceSubtext"]').text.strip().split(" — ")[0],
                        "location": work.select_one('div[class*="UserInfo-workExperienceSubtext"]').text.strip().split(" — ")[1]
                    }
                    for work in work_experience_element
                ]
            return {
                "name": name,
                "avatar": avatar,
                "role": role,
                "company": company,
                "location": location,
                **extra_metadata
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
