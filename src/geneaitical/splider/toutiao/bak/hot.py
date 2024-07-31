#!/usr/bin/env python3
# coding:utf-8
import bag
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests


def main():
    hos_list = get_hot_list()
    for dic in hos_list[:1]:
        Get_relevant_articles(dic)


def Get_relevant_articles(dic):
    url = r'https://so.toutiao.com/search?dvpf=pc&source=input&keyword={}'.format(quote(list(dic)[0], encoding='utf8'))
    headers = {
        "Referer": url,
        "Host": "so.toutiao.com"
    }
    session.headers = headers
    session.cookies[
        ''] = r'tt_webid=7349741726641210919; _ga=GA1.1.1593236486.1711245116; _tea_utm_cache_4916=undefined; _S_DPR=1.25; _S_IPAD=0; s_v_web_id=verify_lu4vah8p_O0eJgr0E_sLhQ_4Uvc_9sss_Y5GxuDq6d5ze; msToken=1-tj_F8UanP9ipxwb8AGOtlYFUBckmgeCpbsyLmWl1TLeHmtakVdRA_tar8htpfsa_3-l66NSL7j_b72_X6im2OY9auiliODwSFBFGZg; ttwid=1%7CrTMoH6_equv6Fj5KhisifcjXO0dY3yXbq3dROS5p7oQ%7C1711245342%7Ccebddba5ac70fb0ee50b6642caaa41e0e0466459e2cbbd2ea69f67ff0b2ca83d; _ga_QEHZPBE5HH=GS1.1.1711245116.1.1.1711246976.0.0.0; _S_WIN_WH=650_608; __ac_nonce=065ff9f2a00b65ed4b389; __ac_signature=_02B4Z6wo00f01JSasJgAAIDDqTOqBst0l9CUurQAAEDdb3; __ac_referer=__ac_blank'
    resp = session.get(url)
    resp.encoding = 'utf-8'
    resp.close()
    url_list = [[i[0].replace('\\u003c', '').replace('em', '').replace('\\u003e', '').replace('/', ''), i[1]] for i in
                re.findall(r'"title":"(.*?)".*?"share_url":"(.*?)"', resp.text) if i[0] != '']
    title = re.compile(r'<strong>(.*?)</strong>', re.S)
    result = []
    for ls in url_list:
        try:
            resp1 = requests.get(ls[-1])
            resp1.close()
            soup = BeautifulSoup(resp1.text, 'html.parser')
            html = soup.findAll('div', class_='a-con')
            mid = []
            for p in html:
                mid.extend(re.findall(r'<p>(.*?)</p>', str(p)))
            result.append([re.findall(title, resp1.text)[0], '\n'.join(mid)])
        except Exception as e:
            pass

    bag.Bag.save_excel(result, './头条热点文章.xlsx')  # 保存文章


def get_hot_list():
    url = r'https://api.vvhan.com/api/hotlist/toutiao'
    resp = session.get(url)
    resp.encoding = 'utf8'
    resp.close()  # 养成好习惯，请求完记得关闭连接
    result = []
    for ls in resp.json().get('data'):
        result.append({ls.get('title'): ls.get('hot')})
    return result


if __name__ == '__main__':
    session = bag.session.create_session()
    session.get('https://www.toutiao.com/')
    main()