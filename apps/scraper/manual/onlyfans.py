import requests
from bs4 import BeautifulSoup

def scrape_onlyfans_account(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the profile page. Please check the URL and try again.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    name_element = soup.select_one('h1.p-name')
    name = name_element.text.strip() if name_element else "N/A"
    images_element = soup.select_one('div.p-media-block[data-type="images"] span')
    images_count = images_element.text.strip() if images_element else "N/A"
    videos_element = soup.select_one('div.p-media-block[data-type="videos"] span')
    videos_count = videos_element.text.strip() if videos_element else "N/A"
    likes_element = soup.select_one('div.p-stats-block[data-type="likes"] span')
    likes_count = likes_element.text.strip() if likes_element else "N/A"
    followers_element = soup.select_one('div.p-stats-block[data-type="followers"] span')
    followers_count = followers_element.text.strip() if followers_element else "N/A"

    print("OnlyFans Account Details:")
    print("Name:", name)
    print("Images Posted:", images_count)
    print("Videos Posted:", videos_count)
    print("Likes:", likes_count)
    print("Followers:", followers_count)
    print("\n")