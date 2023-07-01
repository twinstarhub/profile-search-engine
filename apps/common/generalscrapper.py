import requests
from bs4 import BeautifulSoup

# Facebook working 
def scrape_website(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the article titles using the appropriate HTML tags and attributes
        article_titles = soup.find_all('h2', class_='article-title')

        # Extract the text from each title and print it
        for title in article_titles:
            print(title.text)
    else:
        print('Failed to retrieve website content.')

# Call the function and provide the URL of the webpage you want to scrape
scrape_website('https://github.com/twinstarhub')