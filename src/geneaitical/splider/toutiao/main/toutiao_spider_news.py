import requests
import time
import csv
import sys
sys.path.append("G:\workspace\language_tools\src\geneaitical\splider\\utils")
import db_mysql


NEWS_API_URL = 'https://www.toutiao.com/api/search/content/'
PINGLUN_URL = 'https://www.toutiao.com/article/v2/tab_comments/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}
page = 20
total = 2001
TIMESTRF = int(time.time()) * 1000
## 根据关键词获取新闻信息，把没有评论的过滤掉
def get_news_by_keywords(keyword):
    for page_num in range(0, total, page):
        # 1.构建params数据
        params =params_news_data(keyword, page_num)
        # 2.发送请求,获取响应
        response = parse_url(NEWS_API_URL, params)
        if response.json() == None:
            return
        if response.json().get('data') == None:
            return
        # 3.提取需要的数据
        for json_str in response.json().get('data'):
            try:
                # 4.把提取出的数据放入到字典里面
                news_dict = get_news_data(json_str)
                new_id_remote = news_dict['group_id']
                if (new_id_remote is None or new_id_remote == ''):
                    continue
                if (news_dict['comment_count'] is None or news_dict['comment_count'] == 0):
                    continue
                # 获取评论
                params_pl = params_data_comment(new_id_remote)
                pl_resp = parse_url(PINGLUN_URL, params_pl)
                pl_json_str = pl_resp.json()
                if (pl_json_str.get('data') is None or len(pl_json_str.get('data')) == 0):
                    continue
                # 新闻入库
                news_data = [news_dict['news_title'], news_dict['abstract'], news_dict['user_id'], TIMESTRF, new_id_remote, "toutiao","00", "0","0"]
                newid = db_mysql.insert_news(news_data)
                # 插入搜索
                search_data = [keyword, newid, TIMESTRF]
                db_mysql.insert_search(search_data)
                # 插入评论
                for json in pl_json_str.get('data'):
                    try:
                        create_time = time.localtime(json.get('comment').get('create_time'))
                        Time = time.strftime("%Y-%m-%d %H:%M:%S", create_time)
                        content = json.get('comment').get('text')
                        if content is None or content == '':
                            continue
                        user_id = json.get('comment').get('user_id')
                        user_name = json.get('comment').get('user_name')
                        reply_count = json.get('comment').get('reply_count')
                        digg_count = json.get('comment').get('digg_count')
                        localtion_prov = json.get('comment').get('publish_loc_info')
                        comment_data = [content,newid,user_id,user_name,localtion_prov,Time,'','','','',digg_count,reply_count]
                        db_mysql.insert_comment(comment_data)
                    except Exception  as e:
                        print("捕获到comment异常：", str(e))
            except Exception as e:
                print("捕获到news异常：", str(e))




"""
构建params的方法
:return:
"""
def params_news_data(keyword, page_num):
    params = {
        "aid": "1",
        "app_name": "web_search",
        "offset": str(page_num),
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": "200",
        "en_qc": "1",
        "cur_tab": "1",
        "from": "search_tab",
        "pd": "synthesis",
        "timestamp": TIMESTRF,
    }
    return params

def parse_url(url, params):
    """
    发送请求,获取响应的方法
    :param url: self.API_URL
    :param params:
    :return:
    """
    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 200:
        return response

def get_news_data(json_str):
    """
    # 提取需要的信息的方法
    :param json_str:
    :return:
    """
    news_dict = {}
    # 提取新闻的链接
    news_dict['news_url'] = json_str.get('article_url')
    # 提取新闻的标题
    news_dict['news_title'] = json_str.get('title')
    # 提取新闻的ID
    news_dict['group_id'] = json_str.get('group_id')
    # 提取新闻的摘要
    news_dict['abstract'] = json_str.get('abstract')
    # 评论条数
    news_dict['comment_count'] = str(json_str.get('comment_count'))
    # 作者id
    news_dict['user_id'] = str(json_str.get('user_id'))
    return news_dict

def params_data_comment(newsid):
    """
    再次构建params的方法
    :param news_dict:
    :return:
    """
    params2 = {
        "aid": "1",
        "app_name": "toutiao_web",
        "offset": "0",
        "count": "1000",
        "group_id": newsid,
        "item_id": newsid,
    }
    return params2

if __name__ == '__main__':
    get_news_by_keywords("")