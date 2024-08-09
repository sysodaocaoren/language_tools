import sys
import draw_pic
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\splider\\utils")
import db_mysql


def draw_zhihu_top(keyword):
    comment_list = db_mysql.getTopVoteNews("zhihu",20, keyword)
    count = 0
    for news_info in comment_list:
        print(news_info)
        #draw_pic.w2p(news_info[0], "zhihu_top" + str(count))
        count = count + 1

if __name__ == '__main__':
    draw_zhihu_top("一句话生活")