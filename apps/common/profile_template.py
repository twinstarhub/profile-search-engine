from collections import namedtuple

# Define a named tuple structure
ProfileScrap = namedtuple('Person', ['name', 'age', 'gender'])

# This is for profile scrapping template 
class ProfileTemplate:
    def __init__(self, url, favorite, birthday, count):
        # Constructor for UserNameGenerator

        # Input variable
        self.name = fullname
        self.favorite = favorite
        self.birthday = birthday
        self.count = count