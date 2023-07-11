import re
from random import randrange

from apps import db
from apps.home.models import Patterns, BirthPattern
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
# Name = Micahel bage, Kasper Andersson
# Max length = 30
# Max word = 4
split_patterns = [r'^[a-zA-Z]+[\._][a-zA-Z]+$',
                  r'^[a-zA-Z]+\s[a-zA-Z]+$',
                  r'^[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+$',
                  r'^[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+$']


class UserNameGenerator:
    def __init__(self, fullname, favorite, birthday, count):
        # Constructor for UserNameGenerator

        # Input variable
        self.name = fullname
        self.favorite = favorite
        self.birthday = birthday
        self.count = count

        # Self patterns

        # Self Define variable

        self.max_splitlength = 10
        self.splited_name = []
        self.pattern_list = []

        self.tailored_name_list = []
        self.birthday_pattern = []
        self.name_birthday_list = []
        self.name_favorite_pattern = []
        self.name_favorite_list = []
        self.favorite_common_pattern = []
        self.favorite_common_list = []
        self.favorite_birthday_list = []
        self.name_random_list = []
        self.year = ""
        self.month = ""
        self.day = ""
        self.name_wordcnt = 2

        self.tailored_name_list = []
        self.general_name_list = []
        self.name_list = []

    def translate(self):
        print(self.name)
        # if "Å" in self.name or "Ä" in self.name or "Ö" in self.name:
        #     self.name = self.name.replace("Å", "AA")
        #     self.name = self.name.replace("Ä", "AA")
        #     self.name = self.name.replace("Ö", "OO")
        # else:
        #     self.favorite = GoogleTranslator(source='auto', target='en').translate(text=self.favorite)
        #     self.name = GoogleTranslator(source='auto', target='en').translate(text=self.name)
    def get_date(self):
        self.year, self.month, self.day = self.birthday.split("-")

    # Set the max length of head letters
    def set_max_length(self, length):
        self.maxsplitlength = length

    # Fetch the general pattern list from db
    def fetch_general_pattern(self,pattern_type):
        pattern_list = Patterns.query.with_entities(Patterns.pattern).filter(
            Patterns.type == pattern_type).order_by(Patterns.rank).all()
        return [pattern[0] for pattern in pattern_list]

    # Fetch the birthday pattern list from db
    def fetch_bithday_pattern(self):
        pattern_list = Patterns.query.with_entities(BirthPattern.pattern).all()
        return [pattern[0] for pattern in pattern_list]

    # Fetch the common patterns from the db
    def fetch_common_pattern(self):
        pattern_list = Patterns.query.with_entities(Patterns.pattern).filter(
            Patterns.type == 1).all()
        self.favorite_common_pattern = [pattern[0] for pattern in pattern_list]

    # Function to set names and name word count
    def splitname(self):

        name = self.name

        # check the name is matched which pattern
        for index, pattern in enumerate(split_patterns):
            if re.match(pattern, name):
                if index == 0:
                    FirstName, LastName = re.split(r'\.|_', name)
                    self.splited_name = [FirstName, LastName, " ", " "]
                    self.name_wordcnt = 2
                    return True

                elif index == 1:
                    FirstName, LastName = name.split(" ")
                    self.splited_name = [FirstName, LastName, " ", " "]
                    self.name_wordcnt = 2
                    return True

                elif index == 2:
                    FirstName, SecondName, LastName = name.split(" ")
                    self.splited_name = [FirstName, SecondName, LastName, " "]
                    self.name_wordcnt = 3
                    return True

                elif index == 3:
                    FirstName, SecondName, MiddleName, LastName = name.split(
                        " ")
                    self.splited_name = [FirstName,
                                         SecondName, MiddleName, LastName]
                    self.name_wordcnt = 4
                    return True
        else:
            self.name_wordcnt = 0
            return False

    # **** Function to set split names to list
    def newsplitname(self):
        self.name = self.name.lower()
        sub_name_list = self.name.split(' ')
        return sub_name_list
    def newsplitfavorite(self):
        favorite_list = self.favorite.split(' ')
        return favorite_list

    # Split Name transformation by pattern
    def transformation(self, pattern, splited_name,pattern_type):
        if pattern_type >= 2 :
            pattern = pattern.replace("FN", splited_name[0])
            pattern = pattern.replace("FTN", splited_name[0][0])
            pattern = pattern.replace("SN", splited_name[1])
            pattern = pattern.replace("STN", splited_name[1][0])
        if pattern_type >= 3 :
            pattern = pattern.replace("MN", splited_name[2])
            pattern = pattern.replace("MTN", splited_name[2][0])
        if pattern_type == 4 :
            pattern = pattern.replace("LN", splited_name[3])
            pattern = pattern.replace("LTN", splited_name[3][0])
        return pattern

    # Birthday transfromation with birthday pattern
    def replace_birth_pattern(self, birth):
        year, month, day = self.birthday.split("-")
        birth = birth.replace("YYYY", year)
        birth = birth.replace("Y0", year[2:])
        birth = birth.replace("MM", month)

        if month[0] == "0":
            birth = birth.replace("M0", month[1])
        birth = birth.replace("DD", day)
        if day[0] == "0":
            birth = birth.replace("D0", day[1])
        return birth


### Generator


    # Generate tailored names with general pattern
    def tailored_generator(self,splited_name,pattern_type):
        tailored_name_list = []
        pattern_list = self.fetch_general_pattern(pattern_type)

        for pattern in pattern_list:
            transformed_name = self.transformation(pattern,splited_name,pattern_type)
            if "TX" not in transformed_name and len(transformed_name) <= 30:
                tailored_name_list.append(transformed_name)
                if len(self.name_list) > self.count :
                    return tailored_name_list
        return tailored_name_list
    # Multiplex between two string list
    def multiplex_string(self,array1,array2,str):
        temp = []
        for element1 in array1:
            for element2 in array2:
                new_str = element1.replace(str, element2)
                temp.append(new_str)
        return temp 
    # To generate name with general_generator
    def new_generator(self, transformed_name,splited_name, pattern_type):
        result = [transformed_name]
        if len(self.name_list) > self.count:
            return []
        # Parameters
        multi_patterns = ['FTX','STX','MTX','LTX']
        for idx,pattern in enumerate(multi_patterns):
            if  pattern not in transformed_name:
                continue
            if idx >= pattern_type:
                break
            next_array = []
            # Generate next array
            for i in range(1,len(splited_name[idx])):
                next_array.append(splited_name[idx][0:i])
            result = self.multiplex_string(result,next_array,pattern)
        return result
     
    # Generate general names with general pattern
    def general_generator(self,splited_name,pattern_type):
        pattern_list = self.fetch_general_pattern(pattern_type)

        for pattern in pattern_list:
            if "TX" not in pattern:
                continue
            # if len(self.general_name_list) > self.count - len(self.name_list):
            #     break
            transformed_name = self.transformation(pattern,splited_name,pattern_type)
            print(transformed_name)
            self.name_list.extend(self.new_generator(transformed_name,splited_name, pattern_type))
            if len(self.name_list) > self.count :
                return self.name_list

    # Generate name combining with favorite and common string
    def favorite_common_generator(self):

        # Read common word from files
        suffix_list = []
        with open('nouns.txt', "r", encoding='utf-8') as query_file:
            suffix_list = query_file.read().split("\n")

        for x in suffix_list:
            num = randrange(len(self.favorite_common_pattern))
            new_name = self.favorite_common_pattern[num].replace(
                "FAVO", self.favorite)+x
            if len(new_name) <= 30:
                self.favorite_common_list.append(new_name)

        self.name_list.extend(self.favorite_common_list)

    # Generate names combining birthday with birthday pattern
    def name_birthday_generator(self, tailored_name_list):
        name_birthday_list = []
        birthday_pattern = self.fetch_bithday_pattern()
        for pattern in birthday_pattern:
            birth = self.replace_birth_pattern(pattern)
            for x in tailored_name_list:
                if len(x + birth) <= 30:
                    name_birthday_list.append(x + birth)
                if len(x + birth) <= 29:
                    name_birthday_list.append(x + "_" + birth)
                if "." not in birth and len(x + birth) <= 29:
                    name_birthday_list.append(x + "." + birth)

        return name_birthday_list

    # Generate names combining favorite with birthday pattern
    def favorite_birthday_generator(self,favorite):
        favorite_list = []
        birthday_pattern = self.fetch_bithday_pattern()
        for pattern in birthday_pattern:
            birth = self.replace_birth_pattern(pattern)
            x = favorite
            if len(x + birth) <= 30:
                favorite_list.append(x + birth)
            if len(x + birth) <= 29:
                favorite_list.append(x + "_" + birth)
            if "." not in birth and len(x + birth) <= 29:
                favorite_list.append(x + "." + birth)
        return favorite_list

    # Generate names combining favorite string with common words
    def name_favorite_birthday_generator(self):
        name_favorite_bith = []
        for x in self.name_list:
            if len(x + self.favorite) <= 30:
                name_favorite_bith.append(x + self.favorite)
                name_favorite_bith.append(self.favorite + x)
                if len(x + self.favorite) <= 29:
                    name_favorite_bith.append(x + "_" + self.favorite)
                    name_favorite_bith.append(self.favorite + "_" + x)
            if "." not in x and len(x + self.favorite) <= 29:
                name_favorite_bith.append(x + "." + self.favorite)
                name_favorite_bith.append(self.favorite + "." + x)

        return name_favorite_bith

    # Generate names combining random numbers (not availale now)
    def name_random_generator(self):
        rest_count = self.count - len(self.name_list)
        randome_favorite_bith = []
        # Possible to add patten in the future
        while rest_count > 0:
            for name in self.splited_name:
                if name != " ":
                    if len(name) <= 27:
                        self.name_random_list.append(
                            name + str(randrange(1000)))
                        rest_count -= 1
                        if len(name) <= 26:
                            self.name_random_list.append(
                                name + "." + str(randrange(1000)))
                            self.name_random_list.append(
                                name + "_" + str(randrange(1000)))
                            rest_count -= 2

            new_name = ("".join(self.name)).replace(" ", "")
            if len(new_name) <= 27:
                self.name_random_list.append(new_name + str(randrange(1000)))
                rest_count -= 1
                if len(new_name) <= 26:
                    self.name_random_list.append(
                        new_name + "." + str(randrange(1000)))
                    self.name_random_list.append(
                        new_name + "_" + str(randrange(1000)))
                    rest_count -= 2

        self.name_list.extend(self.name_random_list)
    
    # ----------------------------------------------------------------
    # Main Function for Username Generator
    # ----------------------------------------------------------------
    def generate_long_username(self,splited_name,pattern_type):
        tailored_names = self.tailored_generator(splited_name,pattern_type)
        # result.extend(self.name_birthday_generator(tailored_names))
        return tailored_names

    def long_name(self,splitName):
        long_name_list= []
        total = pow(2, len(splitName))
        for i in range(1, total):
            newString = str(bin(i))[2:]
            newString = newString.zfill(len(splitName))
            newString = newString[::-1]
            newname = []
            
            if newString.count("1") < 5 and newString.count("1") > 1:
                for j in range(len(newString)):
                    if newString[j] == "1":
                        newname.append(splitName[j])
                long_name_list.append(newname)
        return long_name_list

    def updated_username_generator(self):
        self.translate()
        self.name_list = []
        # Split FullName and Favorite
        splited_name = self.newsplitname()

        splited_favorite = self.newsplitfavorite()
        pattern_type = len(splited_name)  #  word_count
    
        if pattern_type < 5:
            tailored_names = self.tailored_generator(splited_name,pattern_type)
            self.name_list.extend(tailored_names)
            if self.favorite != "" and self.birthday != "":
                for favorite in splited_favorite:
                    favorite_birthday = self.favorite_birthday_generator(favorite)
                    self.name_list.extend(favorite_birthday)
            if self.birthday !="":
                name_birthday = self.name_birthday_generator(tailored_names)
                self.name_list.extend(name_birthday)
            general_names = self.general_generator(splited_name,pattern_type)
            # self.name_list.extend(general_names)
        else:
            if self.favorite != "":
                for favorite in splited_favorite:
                    favorite_birthday = self.favorite_birthday_generator(favorite)
                    self.name_list.extend(favorite_birthday)

            name_pair_list = self.long_name(splited_name)
            for name_pair in name_pair_list:
                self.name_list.extend(self.generate_long_username(name_pair,len(name_pair)))
            
        return self.name_list
