import jieba
from snownlp import SnowNLP
from cnsenti import Sentiment
def seg_sentence(sentence):
    return " ".join(jieba.cut(sentence))


# 情感分析
def sentiment_analysis(sentence):
    seg_s = seg_sentence(sentence)
    s = SnowNLP(seg_s)
    return s.sentiments

def summary(sentence):
    s = SnowNLP(sentence)
    summary = s.summary(limit=10)  # 文本概括
    for i in summary:
        print(i)


# 示例句子
sentence = "你真是个废物"

# 执行情感分析
sa = sentiment_analysis(sentence)
float_sa = float(str(sa))
print(f"情感得分:" + str(float_sa))
# summary(sentence)
senti = Sentiment()
print(senti.sentiment_calculate(sentence))