import spacy
import json
import time

# Load pre-trained model
nlp = spacy.load("en_core_web_md")

result_dict = {}


def extract_data_from_json(filename, key):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get(key, [])


def extract_linkedin_data():
    result_dict["linkedin"] = extract_data_from_json("linkedin.json", "organicResults")


def extract_instagram_data():
    result_dict["instagram"] = extract_data_from_json("instagram.json", "")


def extract_tiktok_data():
    result_dict["tiktok"] = extract_data_from_json("tiktok.json", "")


def extract_twitter_data():
    result_dict["twitter"] = extract_data_from_json("twitter.json", "organicResults")


def extract_youtube_data():
    result_dict["youtube"] = extract_data_from_json("youtube.json", "organicResults")


def calc_similar():
    result_list = []
    websites = list(result_dict.keys())

    for main_website in websites:
        main_results = result_dict[main_website]
        result = []

        for website in websites:
            if website == main_website:
                continue

            other_results = result_dict[website]
            for item in other_results[:]:
                sen1 = nlp(main_results[0]["description"])
                sen2 = nlp(item["description"])
                try:
                    similarity = sen1.similarity(sen2)
                    if similarity > 0.7:
                        other_results.remove(item)
                        result.append(item["url"])
                        break
                except:
                    pass

        if result:
            result.insert(0, main_results[0]["url"])
            result_list.append(result)

    return result_list


def main():
    start = time.time()

    extract_linkedin_data()
    extract_tiktok_data()
    extract_twitter_data()
    extract_youtube_data()
    extract_instagram_data()

    result_list = calc_similar()

    print(result_list)
    print(len(result_list))

    end = time.time()
    print("running time", end - start)


if __name__ == "__main__":
    main()
