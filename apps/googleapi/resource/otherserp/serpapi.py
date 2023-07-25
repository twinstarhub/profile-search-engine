from serpapi import GoogleSearch
import json

start = 0
end = 20
page_size = 10

# basic search parameters
parameter = {
  "q": "site:linkedin.com Michael Bage",
  "api_key": "2491e231bd2772c6ee2fc68e93ddcfedd29ff00620a6ca81a06684c3d0adc14e",
  # optional pagination parameter
  #  the pagination method can take argument directly
  "start": start,
  "end": end,
  "num": page_size
}

# as proof of concept 
# urls collects
urls = []

# initialize a search
search = GoogleSearch(parameter)

# create a python generator using parameter
pages = search.pagination()
# or set custom parameter
pages = search.pagination(start, end, page_size)

# fetch one search result per iteration 
# using a basic python for loop 
# which invokes python iterator under the hood.
search_results_list = []
for page in pages:
    print(f"Current page: {page['serpapi_pagination']['current']}")
    if page.get("error") is not None and page.get("error") != "":
        break
    for organic_result in page["organic_results"]:
        print(f"Title: {organic_result['title']}\nLink: {organic_result['link']}\n")
        print(f"Snippet: {organic_result['snippet']}")
        urls.append(organic_result['link'])
        search_results_list.append(organic_result)
    

filename = 'searched_profile_url.json'
with open(filename, 'w') as file:
    json.dump(search_results_list, file, indent=4)

# check if the total number pages is as expected
# note: the exact number if variable depending on the search engine backend
if len(urls) == (end - start):
  print("all search results count match!")
if len(urls) == len(set(urls)):
  print("all search results are unique!")