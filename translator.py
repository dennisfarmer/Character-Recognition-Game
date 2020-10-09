#!/usr/bin/env python3
import time
import pandas as pd
import numpy as np

def main():
    translations = pd.read_csv("translations.csv")
    translations["english"] = translations["english"].str.lower()
    translations["pinyin"] = translations["pinyin"].str.lower()

    number_correct = 0
    iterations = 10
    give_character = True
    # Direction of translation
    direction = ["pinyin", "character"]
    if give_character:
        direction = direction[::-1]

    for _ in range(iterations):
        random_indexes = np.random.randint(0,translations.shape[0], size=3)
        correct_answer = translations.loc[random_indexes[0],direction[0]]
        print("\n", translations.loc[random_indexes[0],direction[1]],sep="")
        np.random.shuffle(random_indexes)
        for number, i in enumerate(random_indexes):
            print(number+1,": ", translations.loc[i,direction[0]],sep="")
        user_selection = int(input("\nSelect an answer: ")) - 1
        user_answer = translations.loc[random_indexes[user_selection],direction[0]]
        if correct_answer == user_answer:
            print("That is correct! + 1 point!")
            number_correct += 1
        else:
            print("Sorry, that's not quite right. The correct answer was ", correct_answer, sep="")
        time.sleep(0.5)
        
    score = round(100*(number_correct/iterations), None)
    print("You achieved a score of ", score, "%, with ", number_correct, "/", iterations," of the questions answered correctly.", sep="")
    if score < 75:
        print("Try studying a bit more!")
    else:
        print("Good job!")

    #TODO: write webscraper https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project

if __name__ == "__main__":
    main()