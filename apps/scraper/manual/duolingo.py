# https://substack.com/@henry

import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://www.duolingo.com/profile/{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            
            with open("file.html", "w") as file:
                file.write(content)


            soup = BeautifulSoup(content, 'html.parser')

            # Get Name
            name_element = soup.find('h1', class_='frontend-pencraft-Text-module__header1--fN7A4')

            # Get Avatar Url
            avatar_url=""
            div_element = soup.find('div', class_='frontend-reader2-ProfilePage-module__avatar--fwwNi')
            if div_element:
                # Get the style attribute value
                avatar_img = div_element.find('img')

                # Extract the image URL from the style attribute
                avatar_url = avatar_img['src']
            else:
                avatar_url=""

            div_element_bio = soup.find_all('div',"pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-14--Ume6q frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-normal--s54Wf frontend-pencraft-Text-module__font-text--QmNJR frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__body4--Pl3xY")[0]
            user_bio_element = div_element_bio.find('span')


            name = name_element.get_text(strip=True) if name_element else ""
            # following_count = following_count_element.get_text(strip=True) if following_count_element else ""
            # follower_count = follower_count_element.get_text(strip=True) if follower_count_element else ""
            user_bio = user_bio_element.get_text(strip=True) if user_bio_element else ""
            
            return {
                "Username": username,
                "Name": name,
                "User-bio": user_bio,
                "Avatar-link": avatar_url,
                "Link": url
            }
        else:
            print(f"Error retrieving data for user: {username}")
            return None

async def scrape_users(usernames):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = asyncio.ensure_future(scrape_user_info(session, username))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


if __name__ == '__main__':
    usernames = ["henry","TaroAkira","michael"]
    # usernames = ["bareandneutral", "sirbalocomedy_", "melekazad", "gracino___", "anthonumeh"]

    try:
        loop = asyncio.get_event_loop()
        scraped_data = loop.run_until_complete(scrape_users(usernames))
        for data in scraped_data:
            if data:
                for key, value in data.items():
                    print(f"{key}: {value}")
                print("---------------------------")
    except RuntimeError as e:
        if str(e) == "Event loop is closed":
            pass
        else:
            raise  # Re-raise other RuntimeError exceptions
    finally:
        loop.close()