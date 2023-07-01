from selenium import webdriver

def scrape_website(url):
    # Configure the Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run the browser in headless mode, without opening a visible browser window
    driver = webdriver.Chrome(options=options)

    # Load the webpage
    driver.get(url)

    # Find the article titles using the appropriate CSS selector
    article_titles = driver.find_elements_by_css_selector('h2.article-title')

    # Extract and print the text from each title
    for title in article_titles:
        print(title.text)

    # Quit the webdriver
    driver.quit()

# Call the function and provide the URL of the webpage you want to scrape
scrape_website('https://example.com')