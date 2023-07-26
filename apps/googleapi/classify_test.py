import spacy
import json
import time

start = time.time()
# Load pre-trained model
nlp = spacy.load("en_core_web_md")

list = []

result_list = []


def linkedin():
    with open('linkedin.json', "r") as file:
        result = []
        data = json.load(file)
        sort_result = data[0]['organicResults']

        for item in sort_result:
            if len(item) == 0:
                continue
            else:
                result.append([item["description"], item["url"]])

        list.append(result)


def instagram():
    with open('instagram.json', "r", encoding="utf-8") as file:
        result = []
        data = json.load(file)
        sort_result = data

        for item in sort_result:
            if len(item) == 0:
                continue
            else:
                result.append([item["description"], item["url"]])

        list.append(result)


def tiktok():
    with open('tiktok.json', "r", encoding="utf-8") as file:
        result = []
        data = json.load(file)
        sort_result = data

        for item in sort_result:
            if len(item) == 0:
                continue
            else:
                result.append([item["description"],item["url"]])

        list.append(result)


def twitter():
    with open('twitter.json', "r") as file:
        result = []
        data = json.load(file)
        sort_result = data[0]['organicResults']

        for item in sort_result:
            if len(item) == 0:
                continue
            else:
                result.append([item["description"],item["url"]])

        list.append(result)


def youtube():
    with open('youtube.json', "r", encoding="utf-8") as file:
        result = []
        data = json.load(file)
        sort_result = data[0]['organicResults']

        for item in sort_result:
            if len(item) == 0:
                continue
            else:
                result.append([item["description"],item["url"]])

        list.append(result)


def calc_similar():
    for main in list[0]:
        result = []
        for group_number in range(1, len(list)):
            sen1 = nlp(main[0])
            mylist = list[group_number]
            for item in mylist:
                sen2 = nlp(item[0])
                try:
                    similarity = sen1.similarity(sen2)
                    # print(similarity)
                    if similarity > 0.7:
                        list[group_number].remove(item)
                        result.append(item[1])
                        break
                except:
                    pass

        if len(result) > 0:
            result.insert(0, main[1])
            # list[0].remove(main)
            result_list.append(result)


linkedin()
tiktok()
twitter()
youtube()
instagram()
# print(list)
calc_similar()

# input("bbb")

print(result_list)
print(len(result_list))

end = time.time()

print("running time", end - start)