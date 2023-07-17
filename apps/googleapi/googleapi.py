from serpapi import GoogleSearch
import json, re

API_KEY = "4d0c5dcf12f23b0f76585c56fda833046a9b4d5b80a67b94e2f230fea10cd291"

def search_profile(search_query):
    queries = [
        search_query+' twitter profile',
        search_query+' youtube profile',
        search_query+' facebook profile',
        search_query+' instagram profile',
        search_query+' linkedin profile',
    ]

    data = []

    twitter_urls = []
    youtube_urls = []
    facebook_urls = []
    instagram_urls = []
    linkedin_urls = []

    for query in queries:
        params = {
            'api_key':API_KEY,
            'engine':"duckduckgo",
            "kl": "uk-en",
            'device': 'desktop', 
            'q': query,
        }
        search = GoogleSearch(params) 
        results = search.get_dict() 

        if 'error' in results:
            print(results['error'])
            break

        for result in results.get('organic_results', []):
            url = result.get('link')

            # Add Twitter Profile
            match = re.search(r"https://twitter\.com/([A-Za-z0-9_]+)", url)
            if match:
                username = match.group(1)
                twitter_url = f"https://twitter.com/{username}"
                twitter_urls.append(twitter_url)
                data.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })

            # Add Youtube Profile

            match = re.search(r"https://www.youtube\.com/@([A-Za-z0-9_]+)", url)
            if match:
                username = match.group(1)
                youtube_url = f"https://www.youtube.com/{username}"
                youtube_urls.append(youtube_url)
                data.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })

            # Add Youtube Profile
            
            match = re.search(r"https://www.instagram\.com/([A-Za-z0-9_]+)", url)
            if match:
                username = match.group(1)
                instagram_url = f"https://www.instagram.com/{username}"
                instagram_urls.append(instagram_url)
                data.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })

        
            match = re.search(r"https://www.linkedin\.com/in/([A-Za-z0-9_]+)", url)
            if match:
                username = match.group(1)
                linkedin_url = f"https://www.linkedin.com/in/{username}"
                linkedin_urls.append(linkedin_url)

                data.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })

            match = re.search(r"https://www.facebook\.com/public/([A-Za-z0-9_]+)", url)
            if match:
                username = match.group(1)
                facebook_url = f"https://www.facebook.com/public/{username}"
                facebook_urls.append(facebook_url)

                data.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })
                
    return data
    # return (data, indent=2, ensure_ascii=False)



