# Character-Recognition-Game

```zsh
# Requirements
pip install pyperclip
pip install pandas
```

Chinese is a pretty dope language, without nasty conjugation and plural forms like Spanish or English (gross). However, it does take a lot of practice as a native of a latin based language to be able to read and write it. These Python scripts are a set of tools that make it a tad bit easier to make progress on learning Chinese. Although taking Spanish would be much easier for a foreign language university requirement, I became interested in Chinese when I took it in early grade school and decided to dive into learning it. Enjoy!


### `tonewriter.py`
This program is used to convert between numerized pinyin and proper pinyin with tone characters (ni3 ha3o to nǐ hǎo). You can give `tonewriter.py` a line of text to copy right to your clipboard automatically, or give it an entire file to convert. Currently only numerized to pinyin is supported , but eventually pinyin to hanzi will also be implimented.

### `dictionary.py`
This program can be used to quickly look through a vocabulary list in the form of a csv file to help with chinese vocab. Search can be performed with untoned pinyin, numeric pinyin, or english. Hanzi will later be supported, but it is hard to type hanzi without copying from google translate so this feature sits low on my priority list.

### `interface.py`
WIP gui using PyQt that will be used to tie all of my programs together in a universal executable. Will support adding vocab to `data/translations.csv` and other nifty functionality. Tkinter looks like dog shit wrapped in cat shit so I'm not going to take the time to learn it lmao.

### `tests.py`
Basic unit test program to make sure my scripts still work as I add new vocabulary to my vocab sheet. Currently only tests the `to_hanzi(pinyin)` function from `tonewriter.py`, but will be expanded upon as more stuff gets written.

### `flashcard.py`
I likely won't work on this part until everythin else is done, but `flashcard.py` is a rudimentary memory game designed to help with Chinese words that you might struggle with. Vocabulary can be sorted based on length, lesson number, and category. Eventually I would like to be able to incorporate a sort of progress system akin to other memory games where the game keeps track of what your strengths and weaknesses are. I might even use some machine learning to design it, I'm not sure lol.
