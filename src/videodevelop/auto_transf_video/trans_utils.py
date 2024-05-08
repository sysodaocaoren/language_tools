
import json
import tools
from configuration import config
import urllib
import requests
import re

def save_to_json(data, file_name):
    # 打开文件的模式: 常用的有’r’（读取模式，缺省值）、‘w’（写入模式）、‘a’（追加模式）等
    with open(file_name, 'w') as f:
        # 使用json.dump()函数将序列化后的JSON格式的数据写入到文件中
        json.dump(data, f, indent=4)

def get_from_json (file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


def update_json_key(file_name, key, value):
    # 读取JSON文件
    with open(file_name, 'r') as file:
        data = json.load(file)
    # 修改值
    data[key] = value  # 将age的值改为31
    # 写回JSON文件
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def trans(text, target_language="zh", *, set_p=True,inst=None,stop=0,source_code=None):
    """
    text:
        字符串
    target_language:
        目标语言
    set_p:
        是否实时输出日志，主界面中需要
    """
    serv = tools.set_proxy()
    proxies = None
    if serv:
        proxies = {
            'http': serv,
            'https': serv
        }
    # 翻译后的文本
    target_text = []

    index = 0  # 当前循环需要开始的 i 数字,小于index的则跳过
    iter_num = 0  # 当前循环次数，如果 大于 config.settings.retries 出错
    err = ""
    google_url=tools.get_google_url()
    try:
        url = f"{google_url}/m?sl=auto&tl={urllib.parse.quote(target_language)}&hl={urllib.parse.quote(target_language)}&q={urllib.parse.quote(text)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, proxies=proxies, headers=headers, timeout=300)
        if response.status_code != 200:
            raise Exception(f'Google {response.status_code},{response.reason}')
        re_result = re.findall(
            r'(?s)class="(?:t0|result-container)">(.*?)<', response.text)
        if len(re_result) < 1:
            raise Exception('len(re_result)<1')
        if re_result[0]:
            return re_result[0]
        else:
            raise Exception(f'Google no result:{re_result}')
    except ConnectionError or Timeout as e:
        raise Exception(f'无法连接到Google，请正确填写代理地址')
    except Exception as e:
        error = str(e)
        print(str(e))