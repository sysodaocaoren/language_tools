import requests
import time
import sys
import random
import pandas as pd
sys.path.append("D:\planself\workspace\language_tools\src\geneaitical\splider\\utils")
import db_mysql
from bs4 import BeautifulSoup


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
cookies = {
    # 填自己的z_0 cookie
    'cookie': '_zap=4315d708-dee3-44c1-a3b5-6b4727a8841d; d_c0=ATBSJ9LfjhePTgxOO4qudKmQzElLDvXZWRQ=|1697505123; _xsrf=AseKiLuWNDIt1YuS3SRlXdIpZ4d4D5wF; __zse_ck=001_j9kyoRKLbAb+2SCcA61aofhdAa5N1BW/2CCtlBLkBeWbDLLcWpjH1MKwW1pck090TT6WDILfK558JcGoBtmdmIrlR0KA=uTatYCeCIbAjNVBr9CmgRDO7M77kOoX+7XF; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1721617123,1721701264,1722562273,1722666298; HMACCOUNT=3DC3C42EDC49F678; q_c1=39924da6a31a4a50aca37d2998dafb97|1722667113000|1722667113000; SESSIONID=FzQFRn7wrX4ea6k9DGTYJc423bqj6iNwO9L69MRuAwM; JOID=VlwRBUh9bpZ006nNdX8JjtNp0GNgOxTFN4bH-gAINqITt5imTBG8PBDUqc9y39Q8Mi2YrQLbAiT28cfw31ZU0XM=; osd=Ul0RC0h5b5Z6063MdXEJitJp3mNkOhTLN4LG-g4IMqMTuZiiTRGyPBTVqcFy29U8PC2crALVAiD38cnw21dU33M=; BAIDU_SSP_lcr=https://www.baidu.com/link?url=37RmfFq_dSOwlA_NkLGP6ErTx_2OO2_cnCVX5e_8BFq&wd=&eqid=9586794e002714490000000466add065; __snaker__id=WrSHP8RZ9XKg7Ja5; gdxidpyhxdE=HCTNQDxcgYr%2FAJGckKljf49%2BJillgkq8wjVNiu7G816lJqRRcIDD3sUyTlcti0cEg99BG6OmKtB7wDkD%2B58x%5CXxM2NWoAeyYNNATn%2FSWDdYfA12GCtAe4VcZ1%2FaqrUm1SzMLSQOieGOcMQV1zetv4uoOCopul%2BJSCWU2MmoZOnAjJ8Ob%3A1722668019829; captcha_session_v2=2|1:0|10:1722667893|18:captcha_session_v2|88:UGdmWTBpK0FYb0FQMzQzKyt2bHB4NDZUSEl1ejh6ekI1Ymt3eDF3SFFiNjU3TW1FK0duRUtVSEJVdXZUWmRRWQ==|49e11fbd08a8595b4a86482a321f3c4d59ac758099bb43dff3d7c858ebf81ed2; captcha_ticket_v2=2|1:0|10:1722667906|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfMm1qMFZwU1J6WmpPTkgwNGhtNmg2MFFuV1NuVVVxcUcxWl9KQ18uODZqdkF3dUltUWp1MG04cGcuQ2FOX2lqX05MRUxhLkZJTnczRWlHRnNDVzFEM0JGZypIcVd1SzFiV01iOHphX3Uuc053NDB2d1JWQjBuRE1JWWhEVGFSaG9IT1FDZWpGWDBfNS5vclBTQ2V6U0o1MEd0cjF2Y1ZIY3U0Y1Mxak4wZ3Uxbmg0UCpCWG5QOW5GNjloKmRqbHd0eWpINUlOLlV0bE5sT19RWlNMV3FyLkZkZGtVUE1URENmaUcyT3lIb0ZJWjVPOEdpRE9zZEc5Z0EycThyYU0uSFQ4V3BZczh5UEpHV2tRZ3JMMkppTUNma1pKWTk1bnUyQUpNVDNpaXR1R0VnLkN2TW1Hc3ZwSEZfZGdJRHZJRHVXdERCUm0yZFg1RjNKV0FZZVNvejF1X216c1V4cFBRajRpWU40d0JmUmZNcUVxRFFIMUl0WUlKTGFYOVVUc28wTmluMVRWUk01TF9pRmQ4azYqc0dCT0ZBT3JRWG5PbVdHRWFSZjNwa0J0UldpMVVWUVJ0Rkh4SmZzY0hHRVIubFNVUHFrQmRvaE1iT1JxcUZXeGc4V0cqVXcuKlJEU1Y4TThDS2lZSjZyM2tzbHNLVlYwaVRURThEM2hiLjhXRktGRkdBb003N192X2lfMSJ9|be3ba338ff9e9821a0af2751d7d5ae70c3a103526da82ac89af9235720c94705; z_c0=2|1:0|10:1722667918|4:z_c0|92:Mi4xVG0tZ0F3QUFBQUFCTUZJbjB0LU9GeVlBQUFCZ0FsVk5qaUdiWndENHp6SU9xZUJDaGV3Q09YQzBpM0p1aVFnNHBB|98c442c07a2665639454b9afc28f8f2f86dd4119f4b168e769d9bbf7be555d91; tst=r; BEC=46faae78ffea44ab7c29d705bdab5c18; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1722667952'  # ?`
}

# 请求头
headers_comment = {
    'x-zse-93': '101_3_3.0',
    'x-ab-param': 'se_ffzx_jushen1=0;zr_expslotpaid=1;top_test_4_liguangyi=1;qap_question_author=0;tp_dingyue_video=0;tp_topic_style=0;tp_contents=2;qap_question_visitor= 0;pf_noti_entry_num=2;tp_zrec=1;pf_adjust=1;zr_slotpaidexp=1',
    'x-ab-pb': 'CroB1wKmBDMFdAHgBAsE4wQZBRsAaQFWBVIL5ArHAjMEEQU0DLULdQSiAwoE0QT0C58C7AqbCz8AQAG5AtgCVwTBBNoE4AsSBU8DbAThBMoCNwVRBUMA9wNFBNcLzwsqBEIEoANWDNwL9gJsAzQEBwyEAjIDFAVSBbcD6QQpBWALfQI/BY4DZAS0CvgDFQUPC1ADVwPoA9YEagGMAnIDMgU3DMwCVQUBC0cAzAQOBbQAKgI7AqED8wP0A4kMEl0AAAAAAAABAAAAAAEAAAAAAAMAAAEFAAIBAAABFQABAQEAAQAAAgAAABUBAQALAAEAAQAAAAABAAACBAABAAABAAEBAAEAAQAAAAIBAAEAAQAAAQABAAAAAQAAAAA=',
    'x-zst-81': '3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YD_ycXtucXYqK6P0E79y-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Io4cpr4w0mRPO7HoY70SfquPmz93mhDQyiqV9ebO1hwOYiiR0ELYuUrxmtDomqU7ynXtOnAoTh_PhRDSTFHOsaDH_8UYq0CN9UBFM6Hg1f_FOYrOGwBoYrgcCjBL9hvx1oCYK8CVYUBeTv6u1pgcMzwV8wwt1EbrL-UXBgvg0Z9N__vem_C3L8vCZfMS_Uhoftck1UGg0Bhw1rrXKZgcVQQeC-JLZ28eqWcOxLGo_KX3OsquLquoXxDpMUuF_ChUCCqkwe7396qOZ-Je8ADS9CqcmUuoYsq98yqLmUggYsBXfbLVL3qHMjwS_mXefOComiDSOkUOfQqX00UeBUcnXAh3mMD31bgOYSTSufuCYuDgCjqefWqHYeQSC',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'x-app-version': '6.42.0',
    'sec-ch-ua-mobile': '?0',
    'x-requested-with': 'fetch',
    'x-zse-96': '2.0_aHtyee9qUCtYHUY81LF8NgU0NqNxgUF0MHYyoHe0NG2f',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cookie': '_zap=4315d708-dee3-44c1-a3b5-6b4727a8841d; d_c0=ATBSJ9LfjhePTgxOO4qudKmQzElLDvXZWRQ=|1697505123; _xsrf=AseKiLuWNDIt1YuS3SRlXdIpZ4d4D5wF; __zse_ck=001_j9kyoRKLbAb+2SCcA61aofhdAa5N1BW/2CCtlBLkBeWbDLLcWpjH1MKwW1pck090TT6WDILfK558JcGoBtmdmIrlR0KA=uTatYCeCIbAjNVBr9CmgRDO7M77kOoX+7XF; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1721617123,1721701264,1722562273,1722666298; HMACCOUNT=3DC3C42EDC49F678; q_c1=39924da6a31a4a50aca37d2998dafb97|1722667113000|1722667113000; SESSIONID=FzQFRn7wrX4ea6k9DGTYJc423bqj6iNwO9L69MRuAwM; JOID=VlwRBUh9bpZ006nNdX8JjtNp0GNgOxTFN4bH-gAINqITt5imTBG8PBDUqc9y39Q8Mi2YrQLbAiT28cfw31ZU0XM=; osd=Ul0RC0h5b5Z6063MdXEJitJp3mNkOhTLN4LG-g4IMqMTuZiiTRGyPBTVqcFy29U8PC2crALVAiD38cnw21dU33M=; BAIDU_SSP_lcr=https://www.baidu.com/link?url=37RmfFq_dSOwlA_NkLGP6ErTx_2OO2_cnCVX5e_8BFq&wd=&eqid=9586794e002714490000000466add065; __snaker__id=WrSHP8RZ9XKg7Ja5; gdxidpyhxdE=HCTNQDxcgYr%2FAJGckKljf49%2BJillgkq8wjVNiu7G816lJqRRcIDD3sUyTlcti0cEg99BG6OmKtB7wDkD%2B58x%5CXxM2NWoAeyYNNATn%2FSWDdYfA12GCtAe4VcZ1%2FaqrUm1SzMLSQOieGOcMQV1zetv4uoOCopul%2BJSCWU2MmoZOnAjJ8Ob%3A1722668019829; captcha_session_v2=2|1:0|10:1722667893|18:captcha_session_v2|88:UGdmWTBpK0FYb0FQMzQzKyt2bHB4NDZUSEl1ejh6ekI1Ymt3eDF3SFFiNjU3TW1FK0duRUtVSEJVdXZUWmRRWQ==|49e11fbd08a8595b4a86482a321f3c4d59ac758099bb43dff3d7c858ebf81ed2; captcha_ticket_v2=2|1:0|10:1722667906|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfMm1qMFZwU1J6WmpPTkgwNGhtNmg2MFFuV1NuVVVxcUcxWl9KQ18uODZqdkF3dUltUWp1MG04cGcuQ2FOX2lqX05MRUxhLkZJTnczRWlHRnNDVzFEM0JGZypIcVd1SzFiV01iOHphX3Uuc053NDB2d1JWQjBuRE1JWWhEVGFSaG9IT1FDZWpGWDBfNS5vclBTQ2V6U0o1MEd0cjF2Y1ZIY3U0Y1Mxak4wZ3Uxbmg0UCpCWG5QOW5GNjloKmRqbHd0eWpINUlOLlV0bE5sT19RWlNMV3FyLkZkZGtVUE1URENmaUcyT3lIb0ZJWjVPOEdpRE9zZEc5Z0EycThyYU0uSFQ4V3BZczh5UEpHV2tRZ3JMMkppTUNma1pKWTk1bnUyQUpNVDNpaXR1R0VnLkN2TW1Hc3ZwSEZfZGdJRHZJRHVXdERCUm0yZFg1RjNKV0FZZVNvejF1X216c1V4cFBRajRpWU40d0JmUmZNcUVxRFFIMUl0WUlKTGFYOVVUc28wTmluMVRWUk01TF9pRmQ4azYqc0dCT0ZBT3JRWG5PbVdHRWFSZjNwa0J0UldpMVVWUVJ0Rkh4SmZzY0hHRVIubFNVUHFrQmRvaE1iT1JxcUZXeGc4V0cqVXcuKlJEU1Y4TThDS2lZSjZyM2tzbHNLVlYwaVRURThEM2hiLjhXRktGRkdBb003N192X2lfMSJ9|be3ba338ff9e9821a0af2751d7d5ae70c3a103526da82ac89af9235720c94705; z_c0=2|1:0|10:1722667918|4:z_c0|92:Mi4xVG0tZ0F3QUFBQUFCTUZJbjB0LU9GeVlBQUFCZ0FsVk5qaUdiWndENHp6SU9xZUJDaGV3Q09YQzBpM0p1aVFnNHBB|98c442c07a2665639454b9afc28f8f2f86dd4119f4b168e769d9bbf7be555d91; tst=r; BEC=46faae78ffea44ab7c29d705bdab5c18; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1722667952'  # ?`
}
printFlag = 0
TIMESTRF = int(time.time()) * 1000
def start_spilder(keyword, qusId,  path):
    global printFlag
    ans_url = 'https://www.zhihu.com/' + path
    for page in range(1, 200):
        try:
            time.sleep(random.randint(1, 3))
            ans_repo = requests.get(ans_url, headers=headers, cookies=cookies)
            if (ans_repo.json()['data'] is None or len(ans_repo.json()['data']) == 0):
                break
            for data in ans_repo.json()['data']:
                try:
                    if (printFlag == 0) :
                        print (str(data))
                        printFlag = 2
                    # resolve ans
                    answer_id = data['target']['id']
                    answer= getAnsDetail(qusId, str(answer_id))
                    vote_count = data['target']['voteup_count']
                    comment_count = data['target']['comment_count']
                    user_name=data['target']['author']['name']
                    user_id=data['target']['author']['id']
                    #保存数据库
                    news_data = [keyword, keyword, answer, user_id, TIMESTRF, qusId, answer_id, "zhihu", comment_count, vote_count, user_name]
                    print(news_data)
                    newid = db_mysql.insert_zhihu(news_data)
                    # 处理评论
                    #spilder_comment(answer_id)
                except Exception as e:
                    print("捕获到comment异常：", str(e))
        except Exception as e:
            print("捕获到comment异常：", str(e))
        ans_url = ans_repo.json()['paging']['next']

def trans_date(v_timestamp):
    """10位时间戳转换为时间字符串"""
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def tran_gender(gender_tag):
    """转换性别"""
    if gender_tag == 1:
        return '男'
    elif gender_tag == 0:
        return '女'
    else:  # -1
        return '未知'

def getAnsDetail(quetionId, ansId):
    url_ans = 'https://www.zhihu.com/question/'+quetionId+'/answer/' + ansId
    time.sleep(random.randint(1, 3))
    response = requests.get(url_ans, headers=headers_comment)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        content = soup.find('div', class_='RichContent-inner').get_text()
        return content
    else:
        print("请求失败，状态码：", response.status_code)
        return ''


def spilder_comment(answer_id):
    url0 = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset=0&status=open'.format(
        answer_id)
    r0 = requests.get(url0, headers=headers_comment)  # 发送请求
    total = r0.json()['common_counts']  # 一共多少条评论
    print('一共{}条评论'.format(total))
    if total == 0:
        return
    # 判断一共多少页（每页20条评论）
    max_page = (total + 19) // 20  # 计算总页数，确保即使评论总数小于20，也能进入循环爬取
    print('max_page:', max_page)
    # 开始循环爬取
    for i in range(max_page):
        try:

            offset = i * 20
            url = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset={}&status=open'.format(answer_id,
                str(offset))
            r = requests.get(url, headers=headers_comment)
            print('正在爬取第{}页'.format(i + 1))
            j_data = r.json()
            comments = j_data['data']
            # 如果没有评论了，就结束循环
            if not comments:
                print('无评论，退出循环')
                break
            for c in comments:  # 一级评论
                try:
                    # 评论作者
                    author = c['author']['member']['name']
                    author_id = c['author']['member']['id']
                    # 作者性别
                    gender_tag = c['author']['member']['gender']
                    # 评论时间
                    create_time = trans_date(c['created_time'])
                    # 评论内容
                    comment = c['content']
                    # 点赞数
                    vote_count = c['vote_count']
                    # IP属地
                    localtion = c['address_text'].replace('IP 属地', '')
                    comment_data = [comment, answer_id, author_id, author, localtion, create_time, '', '', '', '', vote_count,'0']
                    db_mysql.insert_comment(comment_data)
                    if c['child_comments']:  # 如果二级评论存在
                        for child in c['child_comments']:  # 二级评论
                            # 评论作者
                            author = c['author']['member']['name']
                            author_id = c['author']['member']['id']
                            # 作者性别
                            gender_tag = c['author']['member']['gender']
                            # 评论时间
                            create_time = trans_date(c['created_time'])
                            # 评论内容
                            comment = c['content']
                            # 点赞数
                            vote_count = c['vote_count']
                            # IP属地
                            localtion = c['address_text'].replace('IP 属地', '')
                            comment_data = [comment, answer_id, author_id, author, localtion, create_time, '', '', '', '',
                                            vote_count, '0']
                            db_mysql.insert_comment(comment_data)
                except Exception as e:
                    print("捕获到comment异常：", str(e))
        except Exception as e:
            print("捕获到comment异常：", str(e))

if __name__ == '__main__':
    start_spilder("从小有个扫兴的父母什么体验","640017081", "api/v4/questions/640017081/feeds/1723796953026687916")
