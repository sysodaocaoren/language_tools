# 浏览器自动化工具
from selenium import webdriver
from selenium.webdriver.common.by import By
# 网络请求工具
import requests

# JSON解析工具
import json

# 创建一个浏览器实例
browser = webdriver.Firefox()

# 获取请求地址 G:/workspace/language_tools/src/geneaitical/splider/toutiao/html/toutiao.html
browser.get("G:/workspace/language_tools/src/geneaitical/splider/toutiao/html/toutiao.html")

# 自动化获取js代码计算的sig数据值
sigTag = browser.find_element(By.ID, "sigUrl")
url = sigTag.text

headers = {
    # 设置User-Agent，模拟浏览器发送请求
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    # 设置Cookie，用于身份验证或其他需要的信息
    'Cookie': '__ac_signature=_02B4Z6wo00f01Lz3yHgAAIDB3.0IExdN.9i818zAAEpR33;tt_webid=7309719685489198604;ttcid=fb73866ceb7a44cdb848344abfc11b6364;s_v_web_id=verify_lpur8vrr_aKDsfWBn_AThk_4UlU_8RpK_Ci9lGCzIBKbb; _ga=GA1.1.1051493470.1701926754; local_city_cache=%E4%B8%B4%E6%B2%82; csrftoken=4561fa578aa7c7bc7d3ac8f87ac7fad1; __feed_out_channel_key=entertainment; passport_csrf_token=a296ea89de4f632e00534cd16812d593; passport_csrf_token_default=a296ea89de4f632e00534cd16812d593; msToken=Lhx7DAYTtQJiiCVIVmYNqtpQkUVKq8RzEzhUZAslgKw_w5gJ_vSlmCJKsQoQUyXXoJzHhluRQFpfceUoT2n2IoACypVJ-aD7RCuXC7iI; tt_scid=0lfkb7lPohYDsWmjDuFAe7L3oLDo0KsbKzlhKzl1CQ2im2TQypCzPCKr.jkBHxexd641; ttwid=1%7CVPO9aK7JwsvyYUFWA3MR5i_pw1b4nic0TD5-jp-zjVc%7C1702450449%7C067c9bd8be4c0a21dc4e60bc225ee29072184eeb24503d5d6cc26b9554d20d26; _ga_QEHZPBE5HH=GS1.1.1702455638.13.0.1702455638.0.0.0.0.0'
}

# 请求接口获取json数据
res = requests.get(url, headers=headers)
print(res.text)
json_obj = json.loads(res.text)

# 通过遍历每条数据，过滤热门文章
for item in json_obj['data']:
    # 判断文章路径是否是站内文章路径
    if re.match(matchTemplate, item['article_url']):
        # 多条件判断是否是较新的热门文章
        print(item['title'])
