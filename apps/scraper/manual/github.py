from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Github(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("GitHub", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, "html.parser")
            fullname_element = soup.find("span", class_="p-name vcard-fullname d-block overflow-hidden")
            fullname = fullname_element.get_text(strip=True) if fullname_element else None
            location_element = soup.find("li", class_="vcard-detail pt-1 hide-sm hide-md", itemprop="homeLocation")
            location = location_element.find("span", class_="p-label").get_text(strip=True) if location_element else None
            organization_element = soup.find("li", class_="vcard-detail pt-1 hide-sm hide-md", itemprop="worksFor")
            organization = organization_element.find("span", class_="p-org").get_text(strip=True) if organization_element else None
            social_links = soup.find_all("li", itemprop="social")
            social_links_list = [link.find("a", class_="Link--primary").get("href") for link in social_links] if social_links else None
            website_element = soup.find("li", itemprop="url")
            website = website_element.find("a").get("href") if website_element else None
            followers_element = soup.find("span", class_="text-bold color-fg-default")
            followers = self.numberize(followers_element.get_text(strip=True) or 0) if followers_element else None
            following_element = soup.find("a", class_="Link--secondary no-underline no-wrap")
            following = self.numberize(following_element.find("span").get_text(strip=True) or 0) if following_element else None
            avatar_element = soup.select_one('img[class*="avatar"]')
            avatar = avatar_element.get('src') if avatar_element else None
            bio_element = soup.find("div", class_="p-note user-profile-bio mb-3 js-user-profile-bio f4")
            bio = bio_element.get_text(strip=True) if bio_element else None
            repository_element = soup.find("a", {"data-tab-item": "repositories"})
            repository_count = self.numberize(
                repository_element.find("span", class_="Counter").get_text(strip=True) or 0
            ) if repository_element else None
            extra_metadata = {}
            pinned_repos_element = soup.find("div", class_="js-pinned-items-reorder-container")
            if pinned_repos_element is not None:
                pinned_repos = pinned_repos_element.find_all("li", class_="mb-3 d-flex flex-content-stretch col-12 col-md-6 col-lg-6")
                for repo in pinned_repos:
                    repo_name = None
                    repo_description = None
                    repo_language = None
                    star_count = None
                    fork_count = None
                    public = False
                    if repo_name := repo.find("span", class_="repo"):
                        repo_name = repo_name.get_text(strip=True)
                    if repo_description := repo.find("p", class_="pinned-item-desc"):
                        repo_description = repo_description.get_text(strip=True)
                    if repo_language := repo.find("span", itemprop="programmingLanguage"):
                        repo_language = repo_language.get_text(strip=True)
                    if star_count := repo.select_one('a[href$="/stargazers"]'):
                        star_count = self.numberize(star_count.get_text(strip=True) or 0)
                    if fork_count := repo.select_one('a[href$="/forks"]'):
                        fork_count = self.numberize(fork_count.get_text(strip=True) or 0)
                    if public := repo.find("span",
                        class_="Label Label--secondary v-align-middle mt-1 no-wrap v-align-baseline Label--inline"
                    ):
                        public = public.get_text(strip=True) == "Public"
                    if not any([repo_name, repo_description, repo_language, star_count, fork_count, public]):
                        continue
                    if "pinned_repos" not in extra_metadata:
                        extra_metadata["pinned_repos"] = []
                    extra_metadata["pinned_repos"].append({
                        "name": repo_name,
                        "description": repo_description,
                        "language": repo_language,
                        "star_count": star_count,
                        "fork_count": fork_count,
                        "public": public
                    })
            return {
                "name": fullname,
                "avatar": avatar,
                "bio": bio,
                "location": location,
                "organization": organization,
                "social_links": social_links_list,
                "website": website,
                "followers": followers,
                "following": following,
                "repository_count": repository_count,
                **extra_metadata
            }
        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None
