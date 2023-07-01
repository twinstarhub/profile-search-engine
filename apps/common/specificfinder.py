import requests

# Linkedin URL finder
def check_linkedin_profile(username):
    # Replace with your own values
    access_token = 'Bearer token'

    # Construct the API request URL
    url = f'https://api.linkedin.com/v2/people?q=username:{username}'

    # Set the request headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Send the HTTP GET request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get('total', 0) > 0:
            print("Profile exists.")
        else:
            print("Profile does not exist.")
    else:
        print("An error occurred:", response.text)


# Usage
username = 'example_username'
check_linkedin_profile(username)
