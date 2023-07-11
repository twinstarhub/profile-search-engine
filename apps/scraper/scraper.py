from apps.urlfinder.urlfinder import UrlFinder

class Scraper:
    def __init__(self, profile_list):
        self.profile_list = profile_list

    def search(self):
        for username,profile_url in self.profile_list:
            print(username,profile_url)


