 #!/usr/bin/env python3

import pandas as pd
from tonewriter import to_hanzi




def to_hanzi_test():
    print("TEST tw.to_hanzi:\n")
    num_errors = 0
    translations = pd.read_csv("data/translations.csv")[["hanzi","pinyin"]]
    for _, row in translations.iterrows():
        hanzz = to_hanzi(row["pinyin"]).replace(" ","")
        if hanzz != row.hanzi:
            num_errors+=1
            print(f"{hanzz} != {row.hanzi}")
    print("\nNumber of errors:",num_errors)
    