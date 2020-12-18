#!/usr/bin/env python3
 
import csv
import sys
from tonewriter import striptones,pinyinize
import pandas as pd
import pyperclip


# add near_search for wan in wan shang (mistyped as "wang" shang)
# Add missing vocab
# fix near_search and "No match found" [doesn't appear] for multiple words
# add ba4n (half past) and ke4j

def search(query):
    # translations = pd.read_csv("data/translations.csv")
    option = query[:2]
    if option[0] == ":":
        query = query[2:]
    else:
        option = ""
    if "," in query:
        query = query.split(",")
    else: query = [query]
    close_matches = []

    # add is_phrase to search phrases, select query options via checkboxes in pyqt gui
    english_search = option == ":e"
    tone_search = (True in [q != striptones(q, void=False) for q in query]
                   or option == ":t"
                   or option == ":p")
    clipboard = "12345"
    hanzi_search = option == ":h"
    if hanzi_search:
        clipboard = pyperclip.paste()
        query = [clipboard]

    # hanzi_search = not query.isalpha()
    for q in query:
        condition = False
        found = False
        q = pinyinize(q, void=False).replace(" ","").lower()

        if len(query) > 1: print(q+":","-"*(len(q)+1),sep="\n")
        # :e for english, :t for tone
        # with open("data/translations.csv") as d:
            #translations = csv.DictReader(d)
        translations = pd.read_csv("data/translations.csv")
        for _,row in translations.iterrows():
            if english_search:
                condition = (row["english"].lower().find(q) != -1)
            elif tone_search:
                condition = (row["pinyin"].replace(" ","").lower().find(q) != -1)
            elif hanzi_search:
                condition = (row["hanzi"].find(clipboard) != -1 or row["hanzi"].find(q) != -1)
            else:
                condition = ((striptones(row["pinyin"].replace(" ","").lower(), void=False).find(q) != -1)
                             or (row["english"].lower().find(q) != -1))
            #c3 = hanzi_search and (row["hanzi"].replace(" ","").find(query) != -1)
            if (condition):
                found = True
                #print("Match found!")
                print("    Pinyin: ",row["pinyin"], sep=" ")
                print("    Hanzi:  ",row["hanzi"], sep=" ")
                print("    English:",row["english"], sep=" ")
                print()
            elif not found:
                # Fuzzy string search implementation
                if row["category"] != "phrases" and q.isalpha():
                    condition = (not english_search) and (True in
                                                          [q_word[0] == t_word[0] and abs(len(q_word) - len(t_word)) <= 2
                                                           for q_word, t_word
                                                           in zip(q.split(" "), row["pinyin"].split(" "))])

                    condition = condition or (english_search and (q[0] in [char[0] for char in row["english"].split(";")]))

                    if condition:
                        close_matches.append(row["pinyin"])

        if not found:
            print("Match not found.")
            if len(close_matches) != 0:
                if len(close_matches) > 5:
                    for i in range(5,len(close_matches),5):
                        close_matches.insert(i,"\n")
                print("Maybe try: ", " / ".join(close_matches), "?", sep="")
            print()

        return found





if __name__ == "__main__":

    # print("1st Tone: ō (flat)",
    #    "2nd Tone: ó (rising)",
    #    "3rd Tone: ǒ (down and up)",
    #    "4th Tone: ò (falling)",
    #    "", sep="\n")
    # print("wo2 -> wó, nu:e -> nüe, ...")

    if len(sys.argv) == 1:
        response = ":q"
        hist = []
        hist_position = 0
        success = False
        print(":Q TO EXIT\n")
        response = input("Enter your search term > ")
        while response.lower() not in ["q",":q"]:
            if response != ":vh" and response[:2] != ":hs":
                print("-------------------------"+"-"*len(response)+"\n")
                success = search(response)
                if success: hist.append(response)
                response = input("Enter your search term > ")
            while response == ":vh":
                print(hist[::-1],"\n",sep="")
                response = input("Enter your search term > ")
            while response[:2] == ":hs":
                hist_position = int(response.replace("-","")[2:] if response.replace("-","")[2:] != "" else 1)
                if hist_position <= len(hist) and hist_position >= 0:
                    response = hist[0-hist_position]
                    print("History[",-hist_position,"] > ",response,"\n--------"+"-"*len(str(hist_position))+"-"*len(response)+"---\n",sep="")
                    success = search(response)
                else:
                    print("Invalid history selection (",hist_position," out of length ",len(hist),")\n",sep="")
                response = input("Enter your search term > ")

    else:
        for word in sys.argv[1:]:
            print(" > ",word,"\n----"+"-"*len(word))
            search(word)
