# 导入需要的模块
import requests
import time
import csv


class JrttSpider:
    """爬取今日头条新闻评论"""

    def __init__(self, search_name, page):
        self.API_URL = 'https://www.toutiao.com/api/search/content/'
        self.PINGLUN_URL = 'https://www.toutiao.com/article/v2/tab_comments/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        self.search_name = search_name
        self.PAGE = page
        self.TIMESTRF = int(time.time()) * 1000

    def paramsData(self):
        """
        构建params的方法
        :return:
        """
        params = {
            "aid": "1",
            "app_name": "web_search",
            "offset": str(self.PAGE),
            "format": "json",
            "keyword": self.search_name,
            "autoload": "true",
            "count": "200",
            "en_qc": "1",
            "cur_tab": "1",
            "from": "search_tab",
            "pd": "synthesis",
            "timestamp": self.TIMESTRF,
        }
        return params

    def parse_url(self, url, params):
        """
        发送请求,获取响应的方法
        :param url: self.API_URL
        :param params:
        :return:
        """
        response = requests.get(url=url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response

    # 提取需要的信息的方法
    def get_news_data(self, json_str):
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
        return news_dict

    def paramsData2(self, news_dict):
        """
        再次构建params的方法
        :param news_dict:
        :return:
        """
        params2 = {
            "aid": "1",
            "app_name": "toutiao_web",
            "offset": "0",
            "count": "10000",
            "group_id": news_dict.get('group_id'),
            "item_id": news_dict.get('group_id'),
        }
        return params2

    def get_pinglun_data(self, resp):
        """
        提取需要的评论信息的方法
        :param resp:
        :return:
        """
        json_str = resp.json()
        for json in json_str.get('data'):
            create_time = time.localtime(json.get('comment').get('create_time'))
            Time = time.strftime("%Y-%m-%d %H:%M:%S", create_time)
            yield {
                # 提取评论者id
                'user_id': json.get('comment').get('user_id'),
                # 提取评论者名字
                'user_name': json.get('comment').get('user_name'),
                # 提取评论内容
                'pl_content': json.get('comment').get('text'),
                # 提取评论时间
                'pl_time': Time
            }

    def run(self):
        """
        # 实现主要逻辑思路
        :return:
        """
        with open('news_pl.csv', 'a', encoding='utf-8-sig', newline="") as csvfile:
            fieldnames = ['news_title', 'user_id', 'user_name', 'pl_content', "pl_time"]
            write_dict = csv.DictWriter(csvfile, fieldnames=fieldnames)
            write_dict.writeheader()
            # 1.构建params数据
            params = self.paramsData()
            print(params)
            # 2.发送请求,获取响应
            response = self.parse_url(self.API_URL, params)
            if response.json() == None:
                return
            if response.json().get('data') == None:
                return
            # 3.提取需要的数据
            for json_str in response.json().get('data'):
                # 4.把提取出的数据放入到字典里面
                news_dict = self.get_news_data(json_str)
                # 5.再次构建params数据
                params2 = self.paramsData2(news_dict)
                # 6.再次发送请求,获取响应
                resp = self.parse_url(self.PINGLUN_URL, params2)
                # 7.提取需要的数据
                pinglun_list = self.get_pinglun_data(resp)
                news_pl_dict = {'news_title': news_dict.get('title')}
                for pinglun_dict in pinglun_list:
                    news_pl_dict.update(pinglun_dict)
                    # 8.保存数据
                    write_dict.writerow(news_pl_dict)


if __name__ == '__main__':
    serch_name = input('请输入你需要搜索的新闻关键字:')
    for page in range(0, 201, 20):
        jrtt_data = JrttSpider(serch_name, page)
        jrtt_data.run()