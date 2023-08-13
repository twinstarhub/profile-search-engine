import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://en.geneanet.org/profil/{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')

            name_element = soup.find('h1')
              # Get Avatar Url
            avatar_url=""
            div_element = soup.find('div', class_='tc_photo')
            if div_element:
                # Get the style attribute value
                avatar_img = div_element.find('img')

                # Extract the image URL from the style attribute
                avatar_url = avatar_img['src']
            else:
                avatar_url=""
            name = name_element.get_text(strip=True) if name_element else ""
            
            return {
                "Username": username,
                "Name": name,
                "Avatar-link": avatar_url,
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
    usernames = ["donnalynn1"]

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