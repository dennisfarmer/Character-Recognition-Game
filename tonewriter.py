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

def pinyinize(string, clip=False, mute=False, void=True):
    string = string.replace("a1","ā").replace("a2","á").replace("a3","ǎ").replace("a4","à")
    string = string.replace("e1","ē").replace("e2","é").replace("e3","ě").replace("e4","è")
    string = string.replace("i1","ī").replace("i2","í").replace("i3","ǐ").replace("i4","ì")
    string = string.replace("o1","ō").replace("o2","ó").replace("o3","ǒ").replace("o4","ò")
    string = string.replace("u1","ū").replace("u2","ú").replace("u3","ǔ").replace("u4","ù").replace("u:","ü")
    if clip:
        pyperclip.copy(string)
        if not mute: print(pinyin, " copied to clipboard\n", sep = "")
    if not void: return string

def numericize(string, clip=False, mute=False, void=True):
    string = string.replace("ā","a1").replace("á","a2").replace("ǎ","a3").replace("à","a4")
    string = string.replace("ē","e1").replace("é","e2").replace("ě","e3").replace("è","e4")
    string = string.replace("ī","i1").replace("í","i2").replace("ǐ","i3").replace("ì","i4")
    string = string.replace("ō","o1").replace("ó","o2").replace("ǒ","o3").replace("ò","o4")
    string = string.replace("ū","u1").replace("ú","u2").replace("ǔ","u3").replace("ù","u4").replace("ü","u:")
    if clip:
        pyperclip.copy(string)
        if not mute: print(string, " copied to clipboard\n", sep = "")
    if not void: return string

def striptones(string, clip=False, mute=False, void=True):
    string = pinyinize(string, void=False)
    string = string.replace("ā", "a").replace("á","a").replace("ǎ","a").replace("à","a")
    string = string.replace("ē", "e").replace("é","e").replace("ě","e").replace("è","e")
    string = string.replace("ī", "i").replace("í","i").replace("ǐ","i").replace("ì","i")
    string = string.replace("ō", "o").replace("ó","o").replace("ǒ","o").replace("ò","o")
    string = string.replace("ū","u").replace("ú","u").replace("ǔ","u").replace("ù","u").replace("ü","u")
    if clip:
        pyperclip.copy(string)
        if not mute: print(string, " copied to clipboard\n", sep = "")
    if not void: return string

# key = "hanzi" or "pinyin"
def generate_translation_dict(key=None, csv_path="data/translations.csv"):

    if key == "pinyin":
        translations = pd.read_csv(csv_path)[["hanzi","pinyin","category"]]
        translations = translations[translations["category"]!="phrases"]
        pinyin_to_hanzi = {}
        for _, row in translations.iterrows():
            for i,j in zip(row["pinyin"].lower().split(" "),[character for character in row["hanzi"]]):
                if i in pinyin_to_hanzi:
                    if pinyin_to_hanzi[i] != j:
                        updated = pinyin_to_hanzi[i].replace("(","").replace(")","").replace(f"/{j}","").replace(f"{j}/","").replace(f"{j}","")
                        new_value = f"({updated}/{j})"
                        pinyin_to_hanzi[i] = new_value
                else:
                    pinyin_to_hanzi[i] = j
        return pinyin_to_hanzi

    elif key == "hanzi":
        translations = pd.read_csv(csv_path)[["hanzi","pinyin"]]
        hanzi_to_pinyin = {}
        for _, row in translations.iterrows():
            for i,j in zip([character for character in row["hanzi"]], row["pinyin"].lower().split(" ")):
                if i in hanzi_to_pinyin:
                    if j not in hanzi_to_pinyin[i]:
                        hanzi_to_pinyin[i].append(j)
                else:
                    hanzi_to_pinyin[i] = [j]
        return hanzi_to_pinyin
    else: return {"ERROR":"No key given, or key is invalid. Use \"pinyin\" or \"hanzi\" as key."}


def to_pinyin(hanzi=None, hanzi_to_pinyin=None, txt_path="data/type_hanzi_here.txt", clip=False, mute=False, void=True):
    if not hanzi:
        with open(txt_path) as f:
            hanzi = f.read()
            if not mute: print(f"Reading {txt_path}:\n\n", hanzi.replace("\n","\\n\n"))
    if not hanzi_to_pinyin: hanzi_to_pinyin = generate_translation_dict(key = "hanzi")
    list_pinyin = []
    for character in hanzi:
        list_pinyin.append(hanzi_to_pinyin[character] if character in hanzi_to_pinyin else character)

    pinyin = "".join(list_pinyin)
    if clip:
        pyperclip.copy(pinyin)
        if not mute: print(string, " copied to clipboard\n", sep = "")
    if not mute: print("Result:\n\n", pinyin)
    if not void: return pinyin
    #url = "http://api.prod.mandarincantonese.com/pinyin/{}".format(hanzi.replace(" ",""))
    #response = requests.get(url)
    #return json.loads(response.content)["pinyin"]


def to_hanzi(pinyin, pinyin_to_hanzi=None, clip=False, mute=False, void=True):

    pinyin = pinyin.lower()
    pinyin_split = pinyin.split(" ")
    if not pinyin_to_hanzi: pinyin_to_hanzi = generate_translation_dict(key = "pinyin")
    list_hanzi = []
    for word in pinyin.split(" "):
        list_hanzi.append(pinyin_to_hanzi[word] if word in pinyin_to_hanzi else f"({word})")

    hanzi = "".join(list_hanzi)
    if clip:
        pyperclip.copy(hanzi)
        if not mute: print(hanzi, " copied to clipboard\n", sep = "")
    if not void: return hanzi

def main():
    if len(sys.argv) == 1:
        response = "Q"
        pinyin_to_hanzi = None
        print("Q TO EXIT\n")
        response = input("[1] numeric to pinyin\n[2] pinyin to numeric\n[3] pinyin to hanzi\n> ")
        print()
        while response.lower() != "q":

            if response == "1":
                response = input("Enter numeric (ni3 ha3o) > ")
                while response.lower() != "q":
                    pinyinize(response, clip=True)
                    response = input("Enter numeric (ni3 ha3o) > ")

            elif response == "2":
                response = input("Enter pinyin (nǐ hǎo) > ")
                while response.lower() != "q":
                    numericize(response, clip=True)
                    response = input("Enter pinyin (nǐ hǎo) > ")

            elif response == "3":
                response = input("Enter pinyin (n3 or nǐ) > ")
                while response.lower() != "q":
                    if not pinyin_to_hanzi: pinyin_to_hanzi = generate_translation_dict(key="pinyin")
                    pinyin = pinyinize(response, void=False)
                    to_hanzi(pinyin, pinyin_to_hanzi, clip=True)
                    response = input("Enter pinyin (n3 or nǐ) > ")

            response = input("[1] numeric to pinyin\n[2] pinyin to numeric\n[3] pinyin to hanzi\n> ")
            print()
            
    else:
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            file_string = f.read()
        file_string = pinyinize(file_string, void=False)
        with open(file_path, "w") as f:
            f.write(file_string)

if __name__ == "__main__": main()
