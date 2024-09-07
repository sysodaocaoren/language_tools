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
    news_list = db_mysql.getRandomZhihu("zhihu", 500, keyword)
    answerArray = []
    for news_info in news_list:
        answer_split = jieba.cut(news_info[0])
        ans_temp = ",".join(answer_split)
        for str22 in ans_temp.split(","):
            if emo_utils.emo_contain_flag(str22):
                answerArray.append(str22)
    out_path = "D:\planself\workspace\language_tools\src\geneaitical\picture\\" + keyword + ".png"
    draw_chart.drawCloudPic(answerArray, out_path)

def draw_zhihu_top(keyword):
    news_list = db_mysql.getTopZhihu("zhihu",10, keyword)
    count = 0
    printFlag = False
    data = {}
    for news_info in news_list:
        print('[' + str(count) + ']' + news_info[0])
        if printFlag == False:
            data['news'] = news_info[0]
            data['name'] = keyword +'_' + str(count)
            data['new_time'] = random_datetime()
            data['new_location'] = random_chinese_province()
            data['vote_count'] = str(news_info[2])
            data['comment_flag'] = False
            if int(news_info[3]) == 0:
                data['comment_count'] = str(news_info[3])
            else:
                data['comment_count'] = int(random.random() * 250)
            draw_pic.draw_new(data)
        count = count + 1

def get_keywords_docx(keyword):
    comments = '那些年，我与扑克牌的不解之缘，父爱如山，重得我差点没站稳！*留守儿童的逆袭？自己拿主意，人生剧本自己写！*娃，你的孝心我收到了，但这粉色小天才，爸爸真的hold不住啊！*扫兴父母大揭秘，原来我们都是“不够好”的受害者！*父爱如“狮吼”，我学会了“忍”字诀，还附赠“左耳进右耳出”技能！*回家过年变“过劫”，高铁票都换不来老妈一笑，我太难了！*报喜不报忧，我的情绪管理秘籍，爸妈不懂我，我懂自己就好！*沟通是桥，理解是梁，跨过扫兴父母的“河”，拥抱自我成长！*佛系应对扫兴父母，修炼内心平和，让他们的“剑”无处可刺！*自给自足，乐在其中，扫兴？不存在的，我的世界我主宰！'
    start_word = '  你是否曾偷偷在心底嘀咕，为啥爸妈总爱在你兴头上浇盆冷水？是基因自带“扫兴”属性，还是爱的另一种深沉表达？今天，咱们就来聊聊“从小有个扫兴父母”的那些事儿，看看你是不是也中了这条“甜蜜又苦涩”的亲情魔咒。准备好了吗？让我们一起揭开那些让人哭笑不得的家庭日常吧！'
    end_word = '  在这个充满爱与挑战的家庭舞台上，我们或许都曾是那个被“扫兴”包围的孩子。但正是这些经历，让我们学会了独立、坚强，更懂得了如何爱自己。记住，无论父母的言行如何，他们的出发点总是爱。而我们，也要学会在爱中成长，在成长中释怀，最终找到属于自己的幸福之路。毕竟，生活是自己的，精彩与否，全由我们说了算！'
    comments_array = comments.split("*")
    news_list = db_mysql.getTopZhihu("zhihu", 10, keyword)
    pic_path_array = []
    for i in range(len(news_list)):
        pic_path_array.append("D:\planself\workspace\language_tools\src\geneaitical\draw_picture\picture\\"+keyword+"_"+str(i)+".png")
    cloud_pic_path = "D:\planself\workspace\language_tools\src\geneaitical\picture\\" + keyword + ".png"
    generate_word.generate_word(keyword, start_word, comments_array, pic_path_array, end_word, cloud_pic_path)

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
    draw_zhihu_top("中国足球不行是为什么")
    #get_keywords_docx("从小有个扫兴的父母什么体验")