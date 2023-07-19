import asyncio
import aiohttp
from bs4 import BeautifulSoup

from apps.scraper.base_model import Platform


class Substack(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Substack", *args, **kwargs)

    def parse_response(self, username, response):
        try:
            soup = BeautifulSoup(response, "html.parser")
            # Extract the name
            name_element = soup.find("h1", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-32--oRWIM frontend-pencraft-Text-module__weight-bold--Ps9DB frontend-pencraft-Text-module__font-display--KlbfE frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__header1--fN7A4")
            name = None
            if name_element is not None:
                name = name_element.text.strip()

            # Extract the username
            username_element = soup.find("a", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-11--k1e8b frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-medium--x7khA frontend-pencraft-Text-module__font-meta--U_nxy frontend-pencraft-Text-module__color-secondary--WRADg frontend-pencraft-Text-module__transform-uppercase--IDkUL frontend-pencraft-Text-module__decoration-hover-underline--BEYAn frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__meta--jzHdd")
            username = None
            if username_element is not None:
                username = username_element.text.strip()

            # Extract the bio
            bio_element = soup.find("div", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-14--Ume6q frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-normal--s54Wf frontend-pencraft-Text-module__font-text--QmNJR frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__body4--Pl3xY")
            bio = None
            if bio_element is not None:
                bio = bio_element.text.strip()

            # Extract the social links
            social_elements = soup.select('button[data-href]:has(svg)')
            socials_links = []
            for btn in social_elements:
                socials_links.append({
                    'name': btn['data-href'].split('/')[3],
                    'platform': btn['data-href'].split('/')[2],
                    'url': btn['data-href']
                })


            return {
                'name': name,
                'username': username,
                'bio': bio,
                'socials_links': socials_links
            }

        except AttributeError:
            self.logger.warning('Some elements not found for user.', extra={"username": username})
            return None


# # List of users to scrape
# users = ["twinstar", "example1", "example2", ...]

# async def scrape_user(session, user):
#     url = f"https://substack.com/@{user}"

#     try:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 content = await response.text()

#                 soup = BeautifulSoup(content, "html.parser")

#                 # Extract the name
#                 name_element = soup.find("h1", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-32--oRWIM frontend-pencraft-Text-module__weight-bold--Ps9DB frontend-pencraft-Text-module__font-display--KlbfE frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__header1--fN7A4")
#                 name = name_element.text.strip()

#                 # Extract the username
#                 username_element = soup.find("a", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-11--k1e8b frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-medium--x7khA frontend-pencraft-Text-module__font-meta--U_nxy frontend-pencraft-Text-module__color-secondary--WRADg frontend-pencraft-Text-module__transform-uppercase--IDkUL frontend-pencraft-Text-module__decoration-hover-underline--BEYAn frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__meta--jzHdd")
#                 username = username_element.text.strip()

#                 # Extract the bio
#                 bio_element = soup.find("div", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-14--Ume6q frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-normal--s54Wf frontend-pencraft-Text-module__font-text--QmNJR frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__body4--Pl3xY")
#                 bio = bio_element.text.strip()

#                 # Store the scraped data in the desired persistent storage (e.g., database, file system)

#                 print("Name:", name)
#                 print("Username:", username)
#                 print("Bio:", bio)

#                 print("------------------------------------")  # Separator

#             else:
#                 print(f"Error scraping user {user}. Status code: {response.status}")

#     except Exception as e:
#         print(f"Error scraping user {user}: {str(e)}")

# async def main():
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for user in users:
#             task = asyncio.create_task(scrape_user(session, user))
#             tasks.append(task)

#         await asyncio.gather(*tasks)

# # Run the scraping process
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
