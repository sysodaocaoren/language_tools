from pyspider.libs.base_handler import *
import pymysql
from urllib.parse import urlencode
import time
import re
import datetime
import pymysql
import json
import execjs
from bs4 import BeautifulSoup
import requests

#此版作为后来的完整版，开始设置为大规模爬取
class Handler(BaseHandler):
    crawl_config = {
    'headers' : {
    "proxy-Connection":"keep-alive",
    "Pragma":"no-cache",
    "Cache-Control":"no-cache",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
}

@every(minutes=2 * 60)
def on_start(self):
    connect = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456Aa?',
        db='zhousicaiji',
        charset='utf8'
    )
cursor = connect.cursor()
cursor.execute("select name from toutiao_key_xiaoyu where state = 1 limit 10000")
keywords = cursor.fetchall()
#print(keywords)
for key in keywords:
    keyword = "".join(key)
    print(keyword)
    keyword = keyword.encode('utf-8')
    print(str(keyword))
    params = {
    'offset': 1,
    'format': 'json',
    'keyword':str(keyword),
    'autoload': 'true',
    'count': '20',
    'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    #print(url)
    self.crawl(url, callback=self.index_page,validate_cert=False,exetime=time.time()+30*60)
    #print('----1------')
    #更改该关键词的状态为取出中
    cursor.execute('update toutiao_key_xiaoyu set state = 0 where name = "%s"' % keyword)
    #print('----2------')
    connect.commit()
    #关闭数据库连接
cursor.close()
connect.close()

@config(age=1 * 6 * 60 * 60)
def index_page(self, response):
    print(response.url)
    print(response.text)
    result = response.text
    #正则匹配网址
    pattern = re.compile('"article_url": "(http://toutiao.com/group/\d+/)"')
    article_urls = pattern.findall(result)
    #print(article_urls)
    for article_url in article_urls:
        print(article_url)
        self.crawl(article_url, callback=self.detail_page,validate_cert=False,exetime=time.time()+30)

@config(priority=2)
def detail_page(self, response):
    #print('----11------')
    title = response.doc('title').text()
    #print(response.url)
    print(response.text)
    article_content = re.findall(r'articleInfo:(.*?\{[\s\S]*?),[\\n\s]*commentInfo', response.text)
    #print(article_content)
    for content_o in article_content:
        print('----12------')
        a = execjs.eval(content_o)
        print(a['content'])
        content = a['content']
        #提取内容
        content = content.replace('&lt;','<')
        content = content.replace('&gt;','>')
        content = content.replace('&#x3D;','=')
        content = content.replace('&quot;','"')
        #print('alt="%s"'%title)
        content = content.replace('alt="%s"'%title,'')
        print(content)
        name = u'今日头条 关键字'
        link = response.url
        print(link)
        now_time = datetime.date.today()
        catid = "2"
        # 连接mysql
        connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456Aa?',
            db='splider',
            charset='utf8'
        )
        cursor = connect.cursor()
        try:
            cursor.execute("insert into touTiaoxiao(catid,from_url,title,content,inputtime,name) values ('%s','%s','%s','%s','%s','%s')"%(catid,response.url,title,content,now_time,name))
            connect.commit()
        except pymysql.err.IntegrityError:
            print('该文章已存在！')
            print('-----1-----')
        cursor.close()
        connect.close()
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "content":content,
        }