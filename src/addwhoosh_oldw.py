from whoosh import index
from whoosh.fields import TEXT, ID
from whoosh.qparser import QueryParser
import pysrt
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.fields import TEXT, SchemaClass
from jieba.analyse import ChineseAnalyzer
import os


analyzer = ChineseAnalyzer()
class ArticleSchema(SchemaClass):
    content = TEXT(stored=True, analyzer=analyzer)
    starttime = TEXT(stored=True)
    endtime = TEXT(stored=True)
    path = TEXT(stored=True)


def is_in(full_str, sub_str):
    try:
        full_str.index(sub_str)
        return True
    except ValueError:
        return False

# 创建一个索引
def addSanguo():
    schema = ArticleSchema()
    ix = create_in("N:\\三国演义\\indexdir", schema, indexname='article_index')
    writer = ix.writer()
    data_path = "N:\\三国演义\\"
    st_names = "72司马取印.ts,64安居平五路.ts,69收姜维.ts,74诸葛妆神.ts,52夺占西川.ts,79吴宫干戈.ts"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                filePath = os.path.join(root, file)
                print("resolve" + filePath)
                subtitles = pysrt.open(filePath, encoding='GBK')
                for subtitle in subtitles:
                    map_path = ''
                    if (is_in(st_names, file)):
                        map_path = filePath.replace('srt', '.ts')
                    else:
                        map_path = filePath.replace('srt', 'mp4')
                    print(map_path)
                    writer.add_document(content=str(subtitle.text), starttime=str(subtitle.start), endtime=str(subtitle.end), path=map_path)
    writer.commit()

if __name__ == "__main__":
    addSanguo()