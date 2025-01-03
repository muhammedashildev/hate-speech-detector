import sys
import time
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
# try:
# 	from nltk import wordpunct_tokenize
# 	from nltk.corpus import stopwords
# except ImportError:
# 	print("[!] You need to install nltk (http://nltk.org/index.html)")
# 	exit()


def calculate_languages_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)  # language "score"

    return languages_ratios


def detect_language(text):
    ratios = calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language


def load_bad_words():
    # if language.upper() in ["ENGLISH", "FRENCH", "SPANISH", "GERMAN"]:
    try:
        badwords_list = []
        lang_file = open("datasets/english.csv", "r")
        for word in lang_file:
            badwords_list.append(word.lower().strip("\n"))
        return badwords_list
    except:
        badwords_list = []
        lang_file = open("datasets/english.csv", "r")
        for word in lang_file:
            badwords_list.append(word.lower().strip("\n"))
        return badwords_list


def load_file(filename):
    file = open(filename, "rb")
    return file


def main(text="hello happy xxx"):

    # language = detect_language(text)
    print("\n")

    print("----------------------------")
    # print("Language Deteced : ", language.upper())
    print("----------------------------")
    print("\n")

    # print("Checking for bad words in " + language.upper() + " language...")
    print("**********************************************************\n")
    try:
        badwords = load_bad_words()
        badwords = set(badwords)

    except Exception as e:
        print("Error Occured in Program - Error : " + str(e))

    text_list = text.split("\n")
    for sentence in text_list:
        line_number = str(text_list.index(sentence) + 1)
        for key in [".", ",", '"', "'", "?", "!", ":", ";", "(", ")", "[", "]", "{", "}"]:
            sentence = sentence.replace(key, "")
        abuses = [i for i in sentence.lower().split() if i in badwords]
        if abuses == []:
            return "Good"
        else:
            print(
                "-- "
                + str(len(abuses))
                + " Bad Words found at line number : "
                + line_number
                + " --"
            )
            x_words = ""
            for i in abuses:
                x_words += i + ", "
            print("Bad Words : " + x_words[:-2])
            print("-----------------\n")
            return "bad"


if __name__ == "__main__":
    text = "its all rude sexy dildo"
    main(text)
