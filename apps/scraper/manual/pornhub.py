import requests
from bs4 import BeautifulSoup

def scrape_pornhub_account(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the profile page. Please check the URL and try again.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    name_element = soup.select_one('div.usernameWrap')
    name = name_element.text.strip() if name_element else "N/A"
    location_element = soup.select_one('div.userDetails dd.location')
    location = location_element.text.strip() if location_element else "N/A"
    views_element = soup.select_one('div.userDetails dd.views')
    views_count = views_element.text.strip() if views_element else "N/A"
    career_element = soup.select_one('div.userDetails dd.careerStatus')
    career_status = career_element.text.strip() if career_element else "N/A"
    gender_element = soup.select_one('div.userDetails dd.gender')
    gender = gender_element.text.strip() if gender_element else "N/A"
    birth_element = soup.select_one('div.userDetails dd.birthplace')
    birth_place = birth_element.text.strip() if birth_element else "N/A"

    print("Pornhub Account Details:")
    print("Name:", name)
    print("City and Country:", location)
    print("Profile Views:", views_count)
    print("Career Status:", career_status)
    print("Gender:", gender)
    print("Birth Place:", birth_place)
    print("\n")