
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from matplotlib import colors
from collections import Counter
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
# 直线图
# x: [1,2,3,4]  y:[2,3,6,8]  title: text  x_title: ceshi   y_title: ceshi
def drawlinePic(lineData):
    # 绘制线图
    plt.plot(lineData['x'], lineData['y'])
    plt.title(lineData['title'])
    plt.xlabel(lineData['x_title'])
    plt.ylabel(lineData['y_title'])
    plt.grid(False)
    # plt.show()
    plt.savefig(lineData['title']+"line_chart.png")


# 散点图
def drawScatterPic(ScatterData):
    # 绘制线图
    plt.scatter(ScatterData['x'], ScatterData['y'])
    plt.title(ScatterData['title'])
    plt.xlabel(ScatterData['x_title'])
    plt.ylabel(ScatterData['y_title'])
    plt.grid(False)
    plt.show()
    # plt.savefig(ScatterData['title']+"ScatterData_chart.png")


# 条形图
def drawBarPic(barparams):
    categories = barparams['categories']
    values = barparams['values']
    # 设置字体为支持中文的字体，比如'SimHei'（黑体），确保你的系统中安装了该字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 绘制条形图
    plt.bar(categories, values, label='测试图例')
    plt.title(barparams['title'])
    plt.xlabel(barparams['x_title'])
    plt.ylabel(barparams['y_title'])
    plt.legend()
    plt.show()


# 饼图
def drawPiePic(pieParams):
    labels = pieParams['lables']
    sizes = pieParams['sizes']
    plt.pie(sizes, labels=labels)
    plt.title(pieParams['title'])
    plt.show()

def draw3DPie(pie3dParams):
    labels = pieParams['lables']
    sizes = pieParams['sizes']
    plt.pie(sizes, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(pieParams['title'])
    plt.show()

# 词云图
def drawCloudPic(report_words):
    # 建立颜色数组，可更改颜色
    color_list = ['#FF0000', '#5959AB', '#00FFFF', '#FF00FF', '#3232CD', '#3299CC', '#FF6EC7' , '#4F2F4F' , '#FFFF00' , '#00FF00' ]
    # 调用颜色数组
    colormap = colors.ListedColormap(color_list)
    stopwords = set(STOPWORDS)
    stopwords.update(["的", "感谢", "我代表", "以上", "报告", "表示诚挚感谢", "战略", "，", "我", "的","游戏"])
    # 设置字体大小
    max_font_size = 200
    min_font_size = 10
    # 统计高频词汇
    result = Counter(report_words).most_common(300)  # 词的个数
    # 建立词汇字典
    content = dict(result)
    wordcloud = WordCloud(scale=4,  # 输出清晰度
                          font_path='D:\planself\workspace\language_tools\src\\simkai.ttf',  # 输出路径
                          colormap=colormap,  # 字体颜色
                          width=1600,  # 输出图片宽度
                          height=900,  # 输出图片高度
                          background_color='white',  # 图片背景颜色
                          stopwords=stopwords,  # 停用词
                          # mask=mask,  # 掩膜
                          max_font_size=max_font_size,  # 最大字体大小
                          min_font_size=min_font_size)  # 最小字体大小
    wordcloud.generate_from_frequencies(content)
    # 使用 matplotlib 显示词云
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('on')
    plt.show()
    # 保存词云图
    wordcloud.to_file("wordcloud.png")

if __name__ == '__main__':
    # 线图
    lineData = {}
    lineData['x'] = [1,2,3,4]
    lineData['y'] = [2,3,6,8]
    lineData['title'] = 'test'
    lineData['x_title'] = 'X'
    lineData['y_title'] = 'Y'
    #drawlinePic(lineData)

    # 散点图
    ScatterData = {}
    ScatterData['x'] = [1, 2, 3, 4, 7, 9, 7, 5, 3, 2]
    ScatterData['y'] = [2, 3, 6, 8, 4, 6, 3, 2, 1, 5]
    ScatterData['title'] = 'test'
    ScatterData['x_title'] = 'X'
    ScatterData['y_title'] = 'Y'
    # drawScatterPic(ScatterData)

    # 柱状图图
    barparams = {}
    barparams['categories'] = ['男', '女', '不男不女']
    barparams['values'] = [2, 3, 6]
    barparams['title'] = '性别统计'
    barparams['x_title'] = '性别'
    barparams['y_title'] = '人数'
    # drawBarPic(barparams)

    #饼图
    pieParams = {}
    pieParams['lables'] = ['男', '女', '不男不女']
    pieParams['sizes'] = [20, 30, 50]
    pieParams['title'] = '性别统计'
    # drawPiePic(pieParams)

    #3D 饼图
    pie3dParams = {}
    pie3dParams['lables'] = ['男', '女', '不男不女']
    pie3dParams['sizes'] = [20, 30, 50]
    pie3dParams['title'] = '性别统计'
    #draw3DPie(pie3dParams)

    # 词云图
    report_words = ['男', '女', '不男不女','1','哈哈','男','哈哈','哈哈','哈哈','哈哈','哈哈','哈哈','哈哈','哈哈','哈哈', '1', '1']
    # drawCloudPic(report_words)


