import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import concurrent.futures

from apps.scraper.base_model import Platform

ZENROW_API_KEY = os.getenv("ZENROW_API_KEY", "7b26afa746c5aa85d837d1440875a2c44279615a")
USERNAME_PATT = re.compile(r'u/.+')

class Reddit(Platform):
    def __init__(self, *args, **kwargs):
        super().__init__("Reddit", *args, **kwargs)
        # self.proxies = [f'http://{ZENROW_API_KEY}:@proxy.zenrows.com:8001']

    def parse_response(self, username, response):
        """Parse the response from Reddit."""
        try:
            soup = BeautifulSoup(response, 'html.parser')
            # Find the element containing the username
            username_element = soup.find("a", text=USERNAME_PATT)
            username_text = None  # Assign a default value
            if username_element is not None:
                username_text = username_element.text.strip()
                print(f"[{self.name}][{username}] Full Name: {username_text}")
            else:
                print(f"[{self.name}][{username}] Username not found on the profile page.")
            # Find the element containing the karma
            karma_element = soup.find("span", id="profile--id-card--highlight-tooltip--karma")
            karma_text = None  # Assign a default value
            if karma_element is not None:
                karma_text = karma_element.text.strip()
                print(f"[{self.name}][{username}] Karma: {karma_text}")
            else:
                print(f"[{self.name}][{username}] Karma not found on the profile page.")
            # Find the element containing the cake day
            cake_day_element = soup.find("span", id="profile--id-card--highlight-tooltip--cakeday")
            cake_day_text = None  # Assign a default value
            account_age = None  # Assign a default value
            if cake_day_element is not None:
                cake_day_text = cake_day_element.text.strip()
                print(f"[{self.name}][{username}] Cake Day: {cake_day_text}")
                # Calculate the age of the account
                current_year = datetime.now().year
                cake_day = datetime.strptime(cake_day_text, "%B %d, %Y")
                account_age = current_year - cake_day.year
                print(f"[{self.name}][{username}] Age of Account: {account_age} years")
            else:
                print(f"[{self.name}][{username}] Cake Day not found on the profile page.")
            avatar = None  # Assign a default value
            avatar_element = soup.find("img", alt="User avatar")
            if avatar_element is not None:
                avatar = avatar_element.get('src')
                print(f"[{self.name}][{username}] Avatar: {avatar}")
            else:
                print(f"[{self.name}][{username}] Avatar not found on the profile page.")
            return {
                "username": username_text,
                "avatar": avatar,
                "karma": karma_text,
                "cake_day": cake_day_text,
                "account_age": account_age
            }
        except AttributeError:
            print(f'[{self.name}][{username}] Error: Some elements not found for user.')
            return None

# def scrape_user_data(username):
#     # URL with the username as a placeholder
#     url = f"https://www.reddit.com/user/{username}"
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
#     username_element = soup.find("h1", class_="_3LM4tRaExed4x1wBfK1pmg")

#     if username_element is not None:
#         username_text = username_element.text.strip()
#         print(f"Full Name: {username_text}")
#     else:
#         print("Username not found on the profile page.")

#     # Find the element containing the karma
#     karma_element = soup.find("span", id="profile--id-card--highlight-tooltip--karma")

#     if karma_element is not None:
#         karma_text = karma_element.text.strip()
#         print(f"Karma: {karma_text}")
#     else:
#         print("Karma not found on the profile page.")

#     # Find the element containing the cake day
#     cake_day_element = soup.find("span", id="profile--id-card--highlight-tooltip--cakeday")

#     if cake_day_element is not None:
#         cake_day_text = cake_day_element.text.strip()
#         print(f"Cake Day: {cake_day_text}")
#         # Calculate the age of the account
#         current_year = datetime.now().year
#         cake_day = datetime.strptime(cake_day_text, "%B %d, %Y")
#         account_age = current_year - cake_day.year
#         print(f"Age of Account: {account_age} years")
#     else:
#         print("Cake Day not found on the profile page.")

# # Function to process a single username
# def process_username(username):
#     print(f"Processing username: {username}")
#     scrape_user_data(username)
#     print("-----------------------")

# # Usage with multiple usernames
# usernames = ["L_Industries", "kasper1995", "kasper_1995","andersson","twinstar","kasper_a","a_kasper","kasper09","kasper_09","kasper97","kasper_a","a_kasper","a_k","an_k","and_k","ande_k","an_ka","a_kas","an_kas","k_a","k_ande","k_ander","k_anders","ka_and","kas_an","kasp_a"]

# # for username in usernames:
# #     scrape_user_data(username)
# #     print("-----------------------")
# #     time.sleep(0.01)  # Delay between requests to avoid overwhelming the server


# # Maximum number of parallel workers
# max_workers = 20  # Adjust this value as per your requirements

# # Create a ThreadPoolExecutor with the specified maximum workers
# with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#     # Submit each username to the executor as a separate task
#     # The executor will automatically schedule and run the tasks in parallel
#     futures = [executor.submit(process_username, username) for username in usernames]

#     # Wait for all tasks to complete
#     concurrent.futures.wait(futures)
