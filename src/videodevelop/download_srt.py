import requests
from bs4 import BeautifulSoup

# 视频 ID
video_id = 'YWh0c5Kj7mM'
# 字幕语言
language_code = 'en'
# YouTube 页面 URL
youtube_url = f'https://www.youtube.com/watch?v={video_id}'

# 获取页面 HTML
response = requests.get(youtube_url)
print(response.text)
soup = BeautifulSoup(response.text, 'lxml')

# 找到字幕的 <a> 元素
subtitle_link = soup.select_one(f'a[href*="{video_id}"][href*="tlang={language_code}"]')
print(subtitle_link)
if subtitle_link:
    # 下载字幕文件
    subtitle_url = subtitle_link['href']
    response = requests.get(subtitle_url)
    with open(f'{video_id}.{language_code}.srt', 'wb') as f:
        f.write(response.content)