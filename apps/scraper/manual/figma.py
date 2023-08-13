from zenrows import ZenRowsClient 
import time
import asyncio 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs 
 
zenrows_params = {
    "js_render": "true",
    "js_instructions": "%5B%7B%22click%22%3A%22.selector%22%7D%2C%7B%22wait%22%3A500%7D%2C%7B%22fill%22%3A%5B%22.input%22%2C%22value%22%5D%7D%2C%7B%22wait_for%22%3A%22.slow_selector%22%7D%5D"
}
# Set concurrency and retries
client = ZenRowsClient("7b26afa746c5aa85d837d1440875a2c44279615a",concurrency=10, retries=1) 
 

# Create a function to parse HTML using Beautiful Soup
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Manipulate the Beautiful Soup object to extract data as needed
    return soup

async def scrap_figma(usernames): 
    urls = ["https://www.figma.com/@" + username for username in usernames]
    responses = await asyncio.gather(*[client.get_async(url,zenrows_params) for url in urls]) 

    result = []
    for idx,response in enumerate(responses): 
        original_url = parse_qs(urlparse(response.request.url).query)["url"]
        
        if response.status_code == 200:
            # print({ 
            #     "response": response, 
            #     "status_code": response.status_code, 
            #     "request_url": original_url, 
            # }) 
            soup = parse_html(response.content)
            h1_element = soup.find('h1', class_='text--_fontBaseWhyte--z-Ypd')
            name_element = h1_element.find('span')

            # Get Avatar Url
            avatar_url=""
            div_element = soup.find('div', class_='profile_header--profileHeaderAvatarContainer--7f99T')
            if div_element:
                # Get the style attribute value
                avatar_img = div_element.find('img')

                # Extract the image URL from the style attribute
                avatar_url = avatar_img['src'] if avatar_img else ""
            else:
                avatar_url=""

            span_follow = soup.find_all('span', class_='profile_resources_grid--followsDataCount--HPMnb')


            name = name_element.get_text(strip=True) if name_element else ""
            follower = span_follow[0].get_text(strip=True) if span_follow[0] else ""
            following = span_follow[1].get_text(strip=True) if span_follow[1] else ""

            print({
                "Username": usernames[idx],
                "Name": name,
                "Follower": follower,
                "Following": following,
                "Avatar-link": avatar_url,
                "Link": urls[idx]
            })
        else:
            print(f"Not available --> {usernames[idx]}")
 
if __name__ == '__main__':
    st_time = time.monotonic()
    usernames = ["henry","kevin","designer","love","akira","michael","jeny"]

    asyncio.run(scrap_figma(usernames))

    print("\033[32m"+f"Extracting Done ... [{time.monotonic() - st_time:.2f}s]." + "\033[0m")