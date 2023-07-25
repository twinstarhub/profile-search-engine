import requests
import json
headers = { 
  "apikey": "9db5ac00-258c-11ee-9cfd-bf5b34210be7"}

params = (
   ("q","site:linkedin.com/in/ \"Michael Bage\""),
   ("num","200"),
   ("start","100"),
)

response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
site_result = json.loads(response.text)
profile_data = []
for profile in site_result["organic"]:
    profile_data.append(profile)
    
print(response.text)

# Export search_results_list to JSON file
filename = 'search_results.json'
with open(filename, 'w') as file:
    json.dump(profile_data, file, indent=4)

print(f"Search results exported to {filename} successfully.")