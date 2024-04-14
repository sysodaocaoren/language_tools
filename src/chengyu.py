import random

import pandas as pd
import numpy as np
import mysqlutils

chengyu = pd.read_json("xinhua/idiom.json")
t = chengyu.pinyin.str.split()
chengyu["shoupin"] = t.str[0]
chengyu["weipin"] = t.str[-1]
chengyu = chengyu.set_index("word")[["shoupin", "weipin"]]



def get_chengyu_list(word):
    result_array = []
    if word not in chengyu.index:
       print("你输入的不是一个成语，程序结束！")
       return result_array
    words = chengyu.index[chengyu.shoupin == chengyu.loc[word, "weipin"]]
    if words.shape[0] == 0:
       print("没有找到可以接龙的成语，程序结束")
       flag = result_array
    for word_temp in words:
        result_array.append(word_temp)
    return result_array

chengyu_result = []
def generate_chengyu_video(first_chengyu, index = "0", path = []):
    next_chengyu_ayyay = get_chengyu_list(first_chengyu)
    if (len(next_chengyu_ayyay) == 0):
        return
    count = 0
    for chengyu_now in next_chengyu_ayyay:
        results = mysqlutils.queryall(chengyu_now)
        if len(results) == 0:
            continue
        video_info = {}
        id = random.randint(0, 100000000) + random.randint(1, 10000)
        video_info["id"] = id
        video_info["info"] = results[0]
        video_info["pre"] = index
        chengyu_result.append(video_info)
        print(str(chengyu_result))
        generate_chengyu_video(chengyu_now, id, path)
    print("not found , end")


# generate_chengyu_video("门当户对", 1)
# print(str(chengyu_result))


# word = input("请输入一个成语：")
# flag = True
# if word not in chengyu.index:
#     print("你输入的不是一个成语，程序结束！")
#     flag = False
# while flag:
#     n = input("接龙的次数(1-100次的整数，输入任意字母表示结束程序)")
#     if not n.isdigit():
#         print("程序结束")
#         break
#     n = int(n)
#     if not (0 < n <= 100):
#         print("非法数字，程序结束")
#         break
#     for _ in range(n):
#         words = chengyu.index[chengyu.shoupin == chengyu.loc[word, "weipin"]]
#         if words.shape[0] == 0:
#             print("没有找到可以接龙的成语，程序结束")
#             flag = False
#             break
#         for word_temp in words:
#             print(word_temp)
#         #word = np.random.choice(words)
#         #print(word)