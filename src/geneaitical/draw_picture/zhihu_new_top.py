import sys
import draw_pic
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\splider\\utils")
import db_mysql
import random
import datetime
from faker import Faker

def draw_zhihu_top(keyword):
    news_list = db_mysql.getTopVoteNews("zhihu",50, keyword)
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
            data = {}
        # else:
        #     comment = {}
        #     comment['content']=news_info[0]
        #     comment['user_name']=news_info[1]
        #     comment['create_time']=news_info[4]
        #     comment['location']=random_chinese_province()
        #     data['comment'] = comment
        #     draw_pic.niuComment(data)
        #     data={}
        #     printFlag = False
        count = count + 1

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
    draw_zhihu_top("一句话概括人生")