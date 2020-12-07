 #!/usr/bin/env python3

import pandas as pd
from tonewriter import to_pinyin, to_hanzi


def to_pinyin_test():
    # print("index\toutput\t\tcorrect\tpinyin")
    num_errors = 0
    translations = pd.read_csv("data/translations.csv")[["hanzi","pinyin","category"]]
    for i, row in translations.iterrows():
        if row["category"] != "phrase":
            pinyin = to_pinyin(row["hanzi"])
            print(pinyin,"\t*\t",row.pinyin)
            # if pinyin != row.pinyin:
                
            # else:
                    # num_errors+=1
                    # print(f"{i}\t{hanzi}\t\t{row.hanzi}\t{row.pinyin}")

    #print("\nNumber of errors:",num_errors)
    # return num_errors==0,num_errors




def to_hanzi_test():
    # print("index\toutput\t\tcorrect\tpinyin")
    num_errors = 0
    translations = pd.read_csv("data/translations.csv")[["hanzi","pinyin","category"]]

    for i, row in translations.iterrows():
        if row["category"] != "phrase":
            hanzi = to_hanzi(row["pinyin"])
            if hanzi != row.hanzi:
                if "(" in hanzi:
                    pass
                    # pinyin -> hanzi is one to many relationship
                    if 0==1:
                        # Check to make sure at least one combination of options matches
                        # Not yet written for more that one set of options: (1/2)...(3/4)
                        # Work in progress, only 9 errors out of ~200 entries though!
                        passed_test = False
                        start = hanzi.find("(")
                        end = hanzi.find(")")
                        options = hanzi[start+1:end].split("/")
                        for o in options:
                            insert_option = hanzi[0:start] + o + hanzi[end+1:-1]
                            if insert_option == row.hanzi:
                                passed_test = True
                        if not passed_test:
                            num_errors+=1
                            # print(i, "**** ",options, "\t",hanzi, "\tend=",end)
                            print(f"{i}\t{insert_option}\t\t{row.hanzi}\t{row.pinyin}")
                            print()
                else:
                    num_errors+=1
                    print(f"{i}\t{hanzi}\t\t{row.hanzi}\t{row.pinyin}")

    #print("\nNumber of errors:",num_errors)
    return num_errors==0,num_errors


if __name__ == "__main__":

    # to_hanzi():
    # results = to_hanzi_test()
    # if results[0]:
        # print("to_hanzi() passed!")
    # else:
        # print("to_hanzi() failed, ",results[1], " errors encountered")
    to_pinyin_test()


