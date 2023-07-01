# pip install requests
import requests

def zenrow_scrapper(target)
    url = "https://github.com/twinstarhub"
    proxy = "http://54728ad510a6ea076aaa440a46b51a8787c027d8:@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies, verify=False)
    print(response.text)