
import pysrt
import mysqlutils
import os
from xpinyin import Pinyin


def is_in(full_str, sub_str):
    try:
        full_str.index(sub_str)
        return True
    except ValueError:
        return False
indexPath = {"三国演义": "t_video_sanguo", "水浒传": "t_video_shuihu", "西游记": "t_video_xiyou", "红楼梦": "t_video_honglou"}
# 创建一个索引
def addSanguo():
    data_path = "N:\\三国演义\\"
    st_names = ""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath, encoding='GBK')
                for subtitle in subtitles:
                    map_path = filePath.replace('srt', 'mp4')
                    insert_data = [(str(subtitle.text), str(subtitle.start), str(subtitle.end), map_path)]
                    mysqlutils.insert(insert_data, t_video_sanguo)

def shuihu():
    data_path = "N:\\水浒传\\"
    st_names = ""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath, encoding='GBK')
                for subtitle in subtitles:
                    map_path = filePath.replace('srt', 'mkv')
                    insert_data = [(str(subtitle.text), str(subtitle.start), str(subtitle.end), map_path)]
                    mysqlutils.insert(insert_data, "t_video_shuihu")

def xiyou():
    data_path = "N:\\西游记\\"
    st_names = ""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath)
                for subtitle in subtitles:
                    map_path = filePath.replace('srt', 'mp4')
                    insert_data = [(str(subtitle.text), str(subtitle.start), str(subtitle.end), map_path)]
                    mysqlutils.insert(insert_data, "t_video_xiyou")\

def liangjian():
    data_path = "N:\\亮剑\\"
    st_names = ""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath)
                for subtitle in subtitles:
                    map_path = filePath.replace('srt', 'mp4')
                    insert_data = [(str(subtitle.text), str(subtitle.start), str(subtitle.end), map_path)]
                    mysqlutils.insert(insert_data, "t_video_liangjian")

def honglou():
    data_path = "N:\\红楼梦\\"
    st_names = ""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath, encoding='GBK')
                for subtitle in subtitles:
                    map_path = filePath.replace('srt', 'mkv')
                    insert_data = [(str(subtitle.text), str(subtitle.start), str(subtitle.end), map_path)]
                    mysqlutils.insert(insert_data, "t_video_honglou")

def sanguonew():
    data_path = "N:\\新三国\\"
    st_names = ""
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath, encoding='UTF-8')
                for subtitle in subtitles:
                    map_path = filePath.replace('srt', 'mp4')
                    insert_data = [(str(subtitle.text), str(subtitle.start), str(subtitle.end), map_path)]
                    mysqlutils.insert(insert_data, "t_video_sanguo_new")


def update_pinyin(table_name):
    results = mysqlutils.query("", table_name)
    count = 0
    p = Pinyin()
    for hit in results:
        id = hit[0]
        pinyin_res = p.get_pinyin(hit [1], tone_marks="numbers")
        if (is_in(pinyin_res, "'")):
            continue
        if (id < 61265):
            continue
        mysqlutils.update_pinyin(str(id), pinyin_res, table_name)

# type 0:结尾 1：包含
def getByPinyinEnd(table_name, content, type = 0):
    p = Pinyin()
    pinyin = p.get_pinyin(content [-1], tone_marks="numbers")
    pinyin_end = pinyin[:-1]
    results = mysqlutils.queryBypinyin(pinyin, pinyin_end, table_name, type)
    # for hit in results:
    #     print(hit[1] + "/" + hit[5])
    return  results

if __name__ == "__main__":
    getByPinyinEnd("t_video_liangjian","日照香炉生紫烟", 0)