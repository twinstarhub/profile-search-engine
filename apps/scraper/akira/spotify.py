# https://open.spotify.com/user/michael
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://open.spotify.com/user/{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            with open(f"file_{username}.html", "w") as file:
                file.write(content)
            soup = BeautifulSoup(content, 'html.parser')
            username_element = soup.find('h1', class_='Type__TypeElement-sc-goli3j-0')
            username = username_element.get_text(strip=True) if username_element else ""

            return {
                "Username": username,
                "Following Count": following_count + " following",
                "Follower Count": follower_count + " followers",
                "User-bio": user_bio,
                "Avatar-link": avatar_url,
                "Link": link

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
    usernames = ["twinstar","henry","michael"]
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