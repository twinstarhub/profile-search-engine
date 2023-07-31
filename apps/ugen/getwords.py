import os
import names
from random import randrange

class GetWords:
    def __init__(self):
        self.fullname = ""
        self.favorite = ""
    def make_username_favourite(self):
        # Input popular.txt
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, 'resources/popular.txt')
        f = open(file_path)
        contents = f.readlines()

        self.favorite = contents[randrange(0, len(contents))].strip()

        self.fullname = names.get_full_name()