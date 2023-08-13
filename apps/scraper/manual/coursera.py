import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://www.coursera.org/user/{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()

            with open("file.html", "w") as file:
                file.write(content)

            soup = BeautifulSoup(content, 'html.parser')

            # Get Name
            name_element = soup.find('h1', class_='_1gruew7')

            # Get Profile Image URL
            profile_img = soup.find('img', class_='_1tl4f02')

            name = name_element.get_text(strip=True) if name_element else ""
            profile_img_url = profile_img['src'] if profile_img else ""

            return {
                "Username": username,
                "Name": name,
                "Profile Image URL": profile_img_url,
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
    usernames = ["johnsmith", "janedoe", "johndoe"]

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
