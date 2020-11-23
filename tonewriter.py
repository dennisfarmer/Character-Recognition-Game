#!/usr/bin/env python3

import requests
import json
import pandas as pd
# pip isntall pyperclip
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

def striptones(string):
    string
    string = string.replace("ā", "a").replace("á","a").replace("ǎ","a").replace("à","a")
    string = string.replace("ē", "e").replace("é","e").replace("ě","e").replace("è","e")
    string = string.replace("ī", "i").replace("ī","i").replace("ǐ","i").replace("ì","i")
    string = string.replace("ō", "o").replace("ó","o").replace("ǒ","o").replace("ò","o")
    string = string.replace("ū","u").replace("ú","u").replace("ǔ","u").replace("ù","u").replace("ü","u")
    return string

def to_pinyin(hanzi):
    url = "http://api.prod.mandarincantonese.com/pinyin/{}".format(characters.replace(" ",""))
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
                
        
    
if __name__ == "__main__":
    print("TEST .to_hanzi:\n")
    num_errors = 0
    translations = pd.read_csv("data/translations.csv")[["hanzi","pinyin"]]
    for _, row in translations.iterrows():
        hanzz = to_hanzi(row["pinyin"]).replace(" ","")
        if hanzz != row.hanzi:
            num_errors+=1
            print(f"{hanzz} != {row.hanzi}")
    print("\nNumber of errors:",num_errors)
    
if __name__ == "__main__g":

    # print("1st Tone: ō (flat)",
    #    "2nd Tone: ó (rising)",
    #    "3rd Tone: ǒ (down and up)",
    #    "4th Tone: ò (falling)",
    #    "", sep="\n")
    # print("wo2 -> wó, nu:e -> nüe, ...")

    
    if len(sys.argv) == 1:
        print("Q TO EXIT")
        pinyin = input("Enter text below:\n> ",sep="")
        while pinyin.lower() != "q":
            print(pinyin)
            pyperclip.copy(pinyin)
            pinyin = input("Enter text below:\n> ",sep="")
    else:
        with open(sys.argv[1], "r") as f:
            file_string = f.read()
        file_string = pinyinize(file_string)
        with open(sys.argv[1], "w") as f:
            f.write(file_string)

