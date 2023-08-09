import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://www.snapchat.com/add/{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            with open("file.html", "w") as file:
                file.write(content)
            soup = BeautifulSoup(content, 'html.parser')
    
            # Find the <meta> tag with the specified attributes
            meta_tag = soup.find('meta', {'data-react-helmet': 'true', 'property': 'og:title'})
            
            # Extract the content attribute of the <meta> tag
            content = meta_tag.get('content') if meta_tag else None
            name = content.replace(" on Snapchat", "")
            # name_element = soup.find('h2', class_='tiktok-1d3qdok-H2ShareSubTitle')
            
            # username = username_element.get_text(strip=True) if username_element else ""
            # name = name_element.get_text(strip=True) if name_element else ""
            
            return {
                "Username": username,
                "Name": name,
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
    usernames = ["taro"]
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