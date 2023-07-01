import requests
from lxml import etree

# Checked Youtube, Facebook, Linkedin Notworking

def scrape_website(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using lxml's etree
        html_content = response.content
        print(html_content)
        tree = etree.HTML(html_content)

        # Find all the article titles using XPath expression
        article_titles = tree.xpath('//h2[@class="article-title"]/text()')

        # Print the extracted titles
        for title in article_titles:
            print(title)
    else:
        print('Failed to retrieve website content.')

# Scrap function call
scrape_website('https://github.com/twinstarhub')