#!/usr/bin/env python3
import pandas as pd
import sys
from tonewriter import striptones,pinyinize


def search(query):
    c1 = False
    c2 = False
    found = False
    query = pinyinize(query).replace(" ","").lower()
    tone_search = query != striptones(query)
    #hanzi_search = not query.isalpha()
    translations = pd.read_csv("data/translations.csv")
    for _, row in translations.iterrows():
        c1 = not tone_search and ((striptones(row["pinyin"].replace(" ","").lower()).find(query) != -1) or (row["english"].lower().find(query) != -1))
        c2 = tone_search and (row["pinyin"].replace(" ","").lower().find(query) != -1)
        #c3 = hanzi_search and (row["hanzi"].replace(" ","").find(query) != -1)
        if (c1 or c2):
            found = True
            #print("Match found!")
            print("    Pinyin: ",row.pinyin, sep=" ")
            print("    Hanzi:  ",row.hanzi, sep=" ")
            print("    English:",row.english, sep=" ")
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
