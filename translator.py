#!/usr/bin/env python3
import time
import pandas as pd
import numpy as np

def main():
    translations = pd.read_csv("data/translations.csv")
    translations["english"] = translations["english"].str.lower()
    translations["pinyin"] = translations["pinyin"].str.lower()
    translations["hanzi_length"] = translations["hanzi"].str.len()
    # translations["hanzi_length"] = translations["hanzi"].apply(lambda x: len(x))
    # translations = translations[translations["character_length"] == 1]
    translations = translations[translations["category"] == "Family Members"]
    translations.reset_index(inplace=True)

    number_correct = 0
    iterations = 10
    number_of_answers = 3
    give_character = False
    # Direction of translation
    direction = ["pinyin", "hanzi"]
    if give_character:
        direction = direction[::-1]

    for _ in range(iterations):
        rng = np.random.default_rng()
        random_indexes = rng.choice(translations.shape[0], size=number_of_answers, replace=False)
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
    print("\nYou achieved a score of ", score, "%", sep="")
    if score < 75:
        print("Try studying a bit more!")
    else:
        print("Good job!")

    # TODO:
    # When gui is made, make sure number of answers isnt greater than size of df
    # also avoid repeat questions and keep track of specific works between sessions
    # "you should work on x, y, and z", etc.

    #TODO: write webscraper https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project

if __name__ == "__main__":
    main()
