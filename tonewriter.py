#!/usr/bin/env python3

import requests
import json
import pandas as pd
# pip install pyperclip
import pyperclip
import sys

#https://github.com/pepebecker/pinyin-rest

# https://github.com/lxyu/pinyin
# pip install pinyin
# import pinyin

def pinyinize(string):
    string = string.replace("a1","ā").replace("a2","á").replace("a3","ǎ").replace("a4","à")
    string = string.replace("e1","ē").replace("e2","é").replace("e3","ě").replace("e4","è")
    string = string.replace("i1","ī").replace("i2","ī").replace("i3","ǐ").replace("i4","ì")
    string = string.replace("o1","ō").replace("o2","ó").replace("o3","ǒ").replace("o4","ò")
    string = string.replace("u1","ū").replace("u2","ú").replace("u3","ǔ").replace("u4","ù").replace("u:","ü")
    return string

def numericize(string):
    string = string.replace("ā","a1").replace("á","a2").replace("ǎ","a3").replace("à","a4")
    string = string.replace("ē","e1").replace("é","e2").replace("ě","e3").replace("è","e4")
    string = string.replace("ī","i1").replace("ī","i2").replace("ǐ","i3").replace("ì","i4")
    string = string.replace("ō","o1").replace("ó","o2").replace("ǒ","o3").replace("ò","o4")
    string = string.replace("ū","u1").replace("ú","u2").replace("ǔ","u3").replace("ù","u4").replace("ü","u:")
    return string

def striptones(string):
    string = pinyinize(string)
    string = string.replace("ā", "a").replace("á","a").replace("ǎ","a").replace("à","a")
    string = string.replace("ē", "e").replace("é","e").replace("ě","e").replace("è","e")
    string = string.replace("ī", "i").replace("ī","i").replace("ǐ","i").replace("ì","i")
    string = string.replace("ō", "o").replace("ó","o").replace("ǒ","o").replace("ò","o")
    string = string.replace("ū","u").replace("ú","u").replace("ǔ","u").replace("ù","u").replace("ü","u")
    return string

def to_pinyin(hanzi):
    url = "http://api.prod.mandarincantonese.com/pinyin/{}".format(hanzi.replace(" ",""))
    response = requests.get(url)
    return json.loads(response.content)["pinyin"]

def to_hanzi(pinyin="nǐ hǎo", clip=False):
    pinyin = pinyin.lower()
    pinyin_split = pinyin.split(" ")
    translations = pd.read_csv("data/translations.csv")[["hanzi","pinyin"]]
    
    translations["hanzi_length"] = translations["hanzi"].str.len()
    for length in range(translations["hanzi_length"].max(), 0, -1):
        subset = translations[translations["hanzi_length"] == length]
        for _, row in subset.iterrows():
            if pinyin.find(row["pinyin"].lower()) != -1:
                for i, p in enumerate(pinyin_split):
                    if row["pinyin"].lower() in p:
                        pinyin_split[i] = row["hanzi"]
                        
    pinyin = " ".join(pinyin_split)
    if clip:
       pyperclip.copy(pinyin)
    return pinyin

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
            print("    Pinyin:",row.pinyin, sep=" ")
            print("    Hanzi:",row.hanzi, sep=" ")
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
        print("Q TO EXIT")
        print("[S]earch or [T]onewriter?")
        response = input("> ")
        while response.lower() != "q":
            if response.lower() == "s":
                response = input("Enter your search term > ")
                while response.lower() != "q":
                    print("-------------------------"+"-"*len(response)+"\n")
                    search(response)
                    response = input("Enter your search term > ")

            elif response.lower() == "t":
                response = input("[1] numeric -> pinyin\n[2] pinyin -> numeric\n> ")
                if response == "1":
                    response = input("Enter numeric (ni3 ha3o) > ")
                    while response.lower() != "q":
                        pinyin = pinyinize(response)
                        pyperclip.copy(pinyin)
                        print(pinyin, " copied to clipboard", sep = "")
                        response = input("Enter numeric (ni3 ha3o) > ")
                elif response == "2":
                    response = input("Enter pinyin (nǐ hǎo) > ")
                    while response.lower() != "q":
                        numeric = numericize(response)
                        pyperclip.copy(numeric)
                        print(numeric, " copied to clipboard", sep = "")
                        response = input("Enter pinyin (nǐ hǎo) > ")

            print("\nQ TO EXIT")
            print("[S]earch or [T]onewriter?")
            response = input("> ")

    else:
        with open(sys.argv[1], "r") as f:
            file_string = f.read()
        file_string = pinyinize(file_string)
        with open(sys.argv[1], "w") as f:
            f.write(file_string)

