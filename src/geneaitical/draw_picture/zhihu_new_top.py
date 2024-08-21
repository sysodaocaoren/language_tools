import sys
import draw_pic
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\chart")
import draw_chart
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\splider\\utils")
import db_mysql
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\emo")
import emo_utils
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\word")
import generate_word
import random
import datetime
from faker import Faker
import jieba

def draw_zhihu_cloud_pic(keyword):
    news_list = db_mysql.getTopZhihu("zhihu", 1000, keyword)
    count = 0
    printFlag = False
    data = {}
    answerArray = []
    for news_info in news_list:
        print('[' + str(count) + ']' + news_info[0])
        if printFlag == False:
            data['news'] = news_info[0]
            data['name'] = keyword + '_' + str(count + 40)
            data['new_time'] = random_datetime()
            data['new_location'] = random_chinese_province()
            data['vote_count'] = str(news_info[2])
            data['comment_flag'] = False
            if int(news_info[3]) == 0:
                data['comment_count'] = str(news_info[3])
            else:
                data['comment_count'] = int(random.random() * 250)
            answer_split = jieba.cut(news_info[0])
            ans_temp = ",".join(answer_split)
            for str22 in ans_temp.split(","):
                if emo_utils.emo_contain_flag(str22):
                    answerArray.append(str22)
        count = count + 1
    draw_chart.drawCloudPic(answerArray)

def draw_zhihu_top(keyword):
    news_list = db_mysql.getTopZhihu("zhihu",10, keyword)
    count = 0
    printFlag = False
    data = {}
    for news_info in news_list:
        print('[' + str(count) + ']' + news_info[0])
        if printFlag == False:
            data['news'] = news_info[0]
            data['name'] = keyword +'_' + str(count + 40)
            data['new_time'] = random_datetime()
            data['new_location'] = random_chinese_province()
            data['vote_count'] = str(news_info[2])
            data['comment_flag'] = False
            if int(news_info[3]) == 0:
                data['comment_count'] = str(news_info[3])
            else:
                data['comment_count'] = int(random.random() * 250)
            draw_pic.niuComment(data)
        count = count + 1

def get_keywords_docx(keyword):
    comments = ''
    start_word = ''
    end_word = ''
    comments_array = comments.split("*")
    news_list = db_mysql.getTopZhihu("zhihu", 10, keyword)
    pic_path_array = []
    for i in range(len(news_list)):
        pic_path_array.append("D:\planself\workspace\language_tools\src\geneaitical\draw_picture\picture\\"+keyword+"_"+str(i)+".png")
    generate_word.generate_word(keyword, start_word, comments_array, pic_path_array, end_word)

def random_chinese_province():
    provinces = [
        '广东', '北京', '上海', '天津', '江苏', '浙江', '四川', '湖北', '湖南', '江西',
        '安徽', '浙江', '山东', '河南', '河北', '湖南', '吉林', '江西', '山西', '内蒙古',
        '广西', '甘肃', '西藏', '陕西', '甘肃', '云南', '甘肃', '甘肃', '甘肃', '甘肃',
        '青海', '宁夏', '新疆', '香港', '澳门', '台湾'
    ]
    return random.choice(provinces)

def transf_date(longtime):
    print(longtime)
    date = datetime.datetime.fromtimestamp(longtime)
    return date.strftime('%Y-%m-%d')

def random_datetime():
    fake = Faker()
    random_date = fake.date_time_between(start_date="-3y", end_date="now")
    time_str = random_date.strftime("%Y-%m-%d")
    return time_str

if __name__ == '__main__':
    draw_zhihu_top("如何看待黑神话悟空")