#!/usr/bin/env python3
 
import csv
import sys
from tonewriter import striptones,pinyinize


def search(query):
    condition = False
    found = False
    query = pinyinize(query).replace(" ","").lower()

    # :e for english, :t for tone
    option = query[:2]
    if option[0] == ":":
        query = query[2:]
    else:
        option = ""

    english_search = option == ":e"
    tone_search = query != striptones(query) or option == ":t"
    # hanzi_search = not query.isalpha()
    # translations = pd.read_csv("data/translations.csv")
    with open("data/translations.csv") as d:
        translations = csv.DictReader(d)
        for row in translations:
            if english_search:
                condition = (row["english"].lower().find(query) != -1)
            elif tone_search:
                condition = (row["pinyin"].replace(" ","").lower().find(query) != -1)
            else:
                condition = ((striptones(row["pinyin"].replace(" ","").lower()).find(query) != -1) or (row["english"].lower().find(query) != -1))
            #c3 = hanzi_search and (row["hanzi"].replace(" ","").find(query) != -1)
            if (condition):
                found = True
                #print("Match found!")
                print("    Pinyin: ",row["pinyin"], sep=" ")
                print("    Hanzi:  ",row["hanzi"], sep=" ")
                print("    English:",row["english"], sep=" ")
                print()
        if not found:
            print("Match not found\n")


if __name__ == "__main__":

    # print("1st Tone: ō (flat)",
    #    "2nd Tone: ó (rising)",
    #    "3rd Tone: ǒ (down and up)",
    #    "4th Tone: ò (falling)",
    #    "", sep="\n")
    # print("wo2 -> wó, nu:e -> nüe, ...")

    if len(sys.argv) == 1:
        response = "Q"
        print("Q TO EXIT\n")
        response = input("Enter your search term > ")
        while response.lower() != "q":
            print("-------------------------"+"-"*len(response)+"\n")
            search(response)
            response = input("Enter your search term > ")

    else:
        for word in sys.argv[1:]:
            print(" > ",word,"\n----"+"-"*len(word))
            search(word)
