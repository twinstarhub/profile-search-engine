import time
import asyncio 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs 
import requests
from bs4 import BeautifulSoup

# Create a function to parse HTML using Beautiful Soup
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Manipulate the Beautiful Soup object to extract data as needed
    return soup


def scrape_okcupid(name):
    profile_url = f"https://www.okcupid.com/profile/{name}"
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    username = soup.find('span', class_='name').get_text(strip=True)
    age = soup.find('span', class_='age').get_text(strip=True)
    location = soup.find('span', class_='location').get_text(strip=True)
    about = soup.find('div', class_='essay').get_text(strip=True)
    print("Username:", username)
    print("Age:", age)
    print("Location:", location)
    print("About:", about)

names = ["Akira Taro", "twinstar", "Michael"]

for name in names:
    print(f"{name}'s all information")
    print("\n")
    scrape_okcupid(name)
    print("\n")