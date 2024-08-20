import jieba
import numpy as np
import pickle
import pathlib
import re


def load_dict(file):
    """
    Sentiment内置的读取hownet自带pkl词典
    :param file:  词典pkl文件
    :return: 词语列表
    """
    pathchain = ['dic', file]
    mood_dict_filepath = pathlib.Path(__file__).parent.joinpath(*pathchain)
    dict_f = open(mood_dict_filepath, 'rb')
    words = pickle.load(dict_f)
    return words


le = load_dict('le.pkl')
e = load_dict('e.pkl')
hao = load_dict('hao.pkl')
ji = load_dict('ji.pkl')
ju = load_dict('ju.pkl')
nu = load_dict('nu.pkl')
suai = load_dict("suai.pkl")


def emo_contain_flag(origin_word):
    if origin_word in le:
        return True
    if origin_word in e:
        return True
    if origin_word in hao:
        return True
    if origin_word in ji:
        return True
    if origin_word in ju:
        return True
    if origin_word in nu:
        return True
    if origin_word in suai:
        return True
    return False
