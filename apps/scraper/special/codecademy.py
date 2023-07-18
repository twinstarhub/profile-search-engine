import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import concurrent.futures

from apps.scraper.base_model import Platform

ZENROW_API_KEY = os.getenv("ZENROW_API_KEY", "7b26afa746c5aa85d837d1440875a2c44279615a")


class CodeAcademy(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Codecademy", *args, **kwargs)
        self.proxies = [f'http://{ZENROW_API_KEY}:@proxy.zenrows.com:8001']

    def parse_response(self, username, response):
        """Parse the response from Codecademy."""
        try:
            soup = BeautifulSoup(response, 'html.parser')
            # Find the element containing the username
            username_element = soup.find("span", class_="_3LM4tRaExed4x1wBfK1pmg")
            if username_element is not None:
                username_text = username_element.text.strip()
                print(f"[{self.name}] User name: {username_text}")
            else:
                print(f"[{self.name}] Username not found on the profile page.")
            # Find the element containing the fullname
            fullname_element = soup.find("p", class_="gamut-10adrv7-Text e1xvzpfm0")
            if fullname_element is not None:
                karma_text = fullname_element.text.strip()
                print(f"[{self.name}] Full Name: {karma_text}")
            else:
                print(f"[{self.name}] Full Name not found on the profile page.")
            # Find the element containing the joined day
            parent_div = soup.find('div', attrs={'data-testid': 'date-section'})
            join_day_element = None  # Assign a default value
            if parent_div is not None:
                join_day_element = parent_div.find("p", class_="gamut-10adrv7-Text e1xvzpfm0")
            if join_day_element is not None:
                join_day_text = join_day_element.text.strip()
                print(f"[{self.name}] Join Day: {join_day_text}")
                # Calculate the age of the account
                current_year = datetime.now().year
                print(join_day_text)
                date_string = join_day_text.replace("Joined ", "")
                join_day = datetime.strptime(date_string, "%b %d, %Y")
                account_age = current_year - join_day.year
                print(f"[{self.name}] Age of Account: {account_age} years")
            else:
                print(f"[{self.name}] Join Day not found on the profile page.")
            return {
                "username": username_text,
                "fullname": karma_text,
                "join_day": join_day_text,
                "account_age": account_age
            }
        except AttributeError:
            print(f'[{self.name}] Error: Some elements not found for user "{username}"')
            return None


# def scrape_user_data(username):
#     # URL with the username as a placeholder
#     url = f"https://www.codecademy.com/profiles/{username}"
#     # Proxies list
#     proxies = [
#         'http://{ZENROW_API_KEY}:@proxy.zenrows.com:8001',
#         # 'http://proxy2.example.com:5678',
#         # Add more proxies here
#     ]
#     print(username)
#     # Headers to mimic a browser visit
#     headers = {'User-Agent': 'Mozilla/5.0'}

#     max_retries = 3
#     retry_delay = 0.01

#     for retry in range(max_retries):
#         try:
#             # Select a random proxy from the list
#             proxy = {'http': proxies[retry % len(proxies)]}
#             # Returns a requests.models.Response object
#             page = requests.get(url, headers=headers, proxies=proxy)
#             page.raise_for_status()
#             break  # Successful request, exit the loop
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed. Retrying ({retry+1}/{max_retries})...")
#             time.sleep(retry_delay)

#     soup = BeautifulSoup(page.text, 'html.parser')

#     # Find the element containing the username
#     username_element = soup.find("span", class_="_3LM4tRaExed4x1wBfK1pmg")

#     if username_element is not None:
#         username_text = username_element.text.strip()
#         print(f"User name: {username_text}")
#     else:
#         print("Username not found on the profile page.")

#     # Find the element containing the fullname
#     fullname_element = soup.find("p", class_="gamut-10adrv7-Text e1xvzpfm0")

#     if fullname_element is not None:
#         karma_text = fullname_element.text.strip()
#         print(f"Full Name: {karma_text}")
#     else:
#         print("Full Name not found on the profile page.")

#     # Find the element containing the joined day
#     parent_div = soup.find('div', attrs={'data-testid': 'date-section'})
#     join_day_element = None  # Assign a default value
#     if parent_div is not None:
#         join_day_element = parent_div.find("p", class_="gamut-10adrv7-Text e1xvzpfm0")

#     if join_day_element is not None:
#         join_day_text = join_day_element.text.strip()
#         print(f"Join Day: {join_day_text}")
#         # Calculate the age of the account
#         current_year = datetime.now().year
#         print(join_day_text)
#         date_string = join_day_text.replace("Joined ", "")
#         join_day = datetime.strptime(date_string, "%b %d, %Y")
#         account_age = current_year - join_day.year
#         print(f"Age of Account: {account_age} years")
#     else:
#         print("Join Day not found on the profile page.")

# # Function to process a single username
# def process_username(username):
#     print(f"Processing username: {username}")
#     scrape_user_data(username)
#     print("-----------------------")

# # Usage with multiple usernames
# usernames = ["boss", "love", "kill","jeny","python","tong"]

# for username in usernames:
#     scrape_user_data(username)
#     print("-----------------------")
#     time.sleep(0.01)  # Delay between requests to avoid overwhelming the server


# # Maximum number of parallel workers
# max_workers = 20  # Adjust this value as per your requirements

# # Create a ThreadPoolExecutor with the specified maximum workers
# with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#     # Submit each username to the executor as a separate task
#     # The executor will automatically schedule and run the tasks in parallel
#     futures = [executor.submit(process_username, username) for username in usernames]

#     # Wait for all tasks to complete
#     concurrent.futures.wait(futures)
