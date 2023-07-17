import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def scrape_user_info(session, username):
    url = f"https://www.tumblr.com/{username}"
    async with session.get(url) as response:
        html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

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

    # Return the scraped information as a dictionary
    user_info = {
        'full_name': full_name,
        'username': username,
        'website': website,
        'bio': bio
    }

    return user_info

async def scrape_multiple_users(usernames):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = scrape_user_info(session, username)
            tasks.append(task)

        # Gather all the tasks to run them concurrently
        results = await asyncio.gather(*tasks)

    return results

# Example usage
usernames = ['fourbrickstall', 'thebrickdwarf', 'toy-story-yana']  # Add more usernames as needed
loop = asyncio.get_event_loop()
results = loop.run_until_complete(scrape_multiple_users(usernames))

for result in results:
    print(result)
    print("----------------------")
