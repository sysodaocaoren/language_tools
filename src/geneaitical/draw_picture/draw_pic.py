from PIL import Image, ImageFont, ImageDraw
import os
import textwrap
import re

home_path = 'D:\planself\workspace\language_tools\src'
# home_path = 'G:\workspace\language_tools\src'

word_num_line = 20
news_font_path = home_path + "\\方正楷体简体.TTF"
xingkai = home_path + "\\STXINGKA.TTF"
fangzheng = home_path + "\\FZSTK.TTF"
sihei = home_path + "\\simhei.TTF"
simkai = home_path + "\\simkai.ttf"
youyuan =  home_path + "\\SIMYOU.ttf"

split_mark = ['.', '?','!','。','？','！']

def niuComment(data):
    news = data["news"]
    comment = {}
    name = data["name"]
    new_time = data['new_time']
    new_location = data['new_location']
    news_vote_count = data['vote_count']
    new_comment_count = data['comment_count']
    comment_flag = data['comment_flag']

    news_origin = news.replace("\n", "")
    # news_origin = textwrap.wrap(news_origin, width=word_num_line)
    news_text = format_string(news_origin)
    print(news_text)

    if (comment_flag == True):
        comment = data["comment"]
        comment_origin = comment['content'].replace("\n", "")
        comment_origin = textwrap.wrap(comment_origin, width=word_num_line + 3)
        comment_text = "\n".join(comment_origin)
        comment['comment_text'] = comment_text
        comment_h = len(comment_text.split("\n")) + 5
    else:
        comment_h = -20

    # 处理正文的图片
    new_h = 42 * len(news_text.split("\n")) + 15
    all_h = 42 * len(news_text.split("\n")) + comment_h + 40 + 30
    w = int(word_num_line * 42+ 95)
    im = Image.new("RGB", (w, all_h), (230, 240, 230))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(news_font_path, 43)
    dr.text((20, 5), news_text, font=font, fill="#000000")
    # 发布时间地点
    create_time_font = ImageFont.truetype(sihei, 18)
    dr.text((15, new_h), str(new_time) + " . " + new_location, font=create_time_font, fill="#808080")
    dr.text((w - 190, new_h), '回复('+str(new_comment_count)+')  点赞('+str(news_vote_count)+')', font=create_time_font, fill="#808080")
    if (comment_flag == True):
        # 评论发布者名称 时间 地址
        c_h = 0
        comment_time_font = ImageFont.truetype(sihei, 12)
        dr.text((8, new_h + 24), comment['user_name'] + ':    '+str(comment['create_time']) + ' . ' + str(comment['location']), font=comment_time_font, fill="#809080")
        # 评论字体
        comment_font = ImageFont.truetype(news_font_path, 17)
        dr.text((20, new_h + 44), comment_text, font=comment_font, fill="#000000")    # 存储图片到本地路径/w2p.png
    save_path = os.getcwd()
    if (os.path.exists(save_path)):
        save_path = save_path + "/picture/" + name + ".png"
    else:
        os.mkdir(save_path)
        save_path = save_path + "/picture/" + name + ".png"
    im.save(save_path)


def draw_new(data):
    news = data["news"]
    name = data["name"]
    new_time = data['new_time']
    new_location = data['new_location']
    news_vote_count = data['vote_count']
    new_comment_count = data['comment_count']

    news_origin = news.replace("\n", "")
    news_text = format_string(news_origin)
    # 循环每一段的新闻
    new_h = 15
    news_draw_infos = []
    w = int(word_num_line * 42 + 115)
    for news_para in news_text:
        if len(news_para) == 0:
            continue
        news_lines = news_para.split("\n")
        news_line_infos = []
        news_line_h = 0
        for news_line in news_lines:
            news_line_info = {"text": news_line, 'y': new_h + news_line_h}
            news_line_infos.append(news_line_info)
            news_line_h = news_line_h + 42 + 11
        news_draw_info = {'line_infos': news_line_infos}
        new_h = new_h + news_line_h + 22
        news_draw_infos.append(news_draw_info)
    all_h = new_h + 60
    im = Image.new("RGB", (w, all_h), (230, 240, 230))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(news_font_path, 43)
    for news_draw_info in news_draw_infos:
        for news_line in news_draw_info['line_infos']:
            dr.text((20, news_line['y']), news_line['text'], font=font, fill="#000000")
    # 发布时间地点
    create_time_font = ImageFont.truetype(sihei, 27)
    dr.text((15, all_h - 50), str(new_time) + " . " + new_location, font=create_time_font, fill="#808080")
    dr.text((w - 280, all_h - 50), '回复('+str(new_comment_count)+')  点赞('+str(news_vote_count)+')', font=create_time_font, fill="#808080")
    save_path = os.getcwd()
    if (os.path.exists(save_path)):
        save_path = save_path + "/picture/" + name + ".png"
    else:
        os.mkdir(save_path)
        save_path = save_path + "/picture/" + name + ".png"
    im.save(save_path)


def niuComment2(data):
    news = data["news"]
    comment = {}
    name = data["name"]
    new_time = data['new_time']
    new_location = data['new_location']
    news_vote_count = data['vote_count']
    new_comment_count = data['comment_count']
    comment_flag = data['comment_flag']

    news_origin = news.replace("\n", "")
    news_origin = textwrap.wrap(news_origin, width=word_num_line)
    news_text = "\n".join(news_origin)

    if (comment_flag == True):
        comment = data["comment"]
        comment_origin = comment['content'].replace("\n", "")
        comment_origin = textwrap.wrap(comment_origin, width=word_num_line + 3)
        comment_text = "\n".join(comment_origin)
        comment['comment_text'] = comment_text
        comment_h = len(comment_text.split("\n")) + 5
    else:
        comment_h = -20

    # 处理正文的图片
    new_h = 27 * len(news_text.split("\n")) + 5
    all_h = 27 * len(news_text.split("\n")) + comment_h + 40 + 20
    w = int(word_num_line * 19.5 + 35)
    im = Image.new("RGB", (w, all_h), (60, 60, 60))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(news_font_path, 25)
    dr.text((5, 5), news_text, font=font, fill="#ffffff")
    # 发布时间地点
    create_time_font = ImageFont.truetype(simkai, 15)
    dr.text((8, new_h), str(new_time), font=create_time_font, fill="#ffffff")
    dr.text((w - 200, new_h), '赞同('+str(news_vote_count)+')  ' + new_location , font=create_time_font, fill="#ffffff")
    if (comment_flag == True):
        # 评论发布者名称 时间 地址
        c_h = 0
        comment_time_font = ImageFont.truetype(simkai, 12)
        dr.text((8, new_h + 24), comment['user_name'] + ':    '+str(comment['create_time']) + ' . ' + str(comment['location']), font=comment_time_font, fill="#809080")
        # 评论字体
        comment_font = ImageFont.truetype(news_font_path, 17)
        dr.text((20, new_h + 44), comment_text, font=comment_font, fill="#000000")    # 存储图片到本地路径/w2p.png
    save_path = os.getcwd()
    if (os.path.exists(save_path)):
        save_path = save_path + "/" + name + ".png"
    else:
        os.mkdir(save_path)
        save_path = save_path + "/" + name + ".png"
    im.save(save_path)


def w2p(text, name, cutline=True):
    # 文字自动换行
    if cutline:
        sptext = text.replace("\n", "")
        sptext = textwrap.wrap(sptext, width=word_num_line)
        text = "\n".join(sptext)
    # 转换文字为图片并保存为图片
    h = 26 * len(text.split("\n")) + 25
    w = int(word_num_line * 19.5 + 45)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(news_font, 20)
    dr.text((20, 30), text, font=font, fill="#000000")
    # 存储图片到本地路径/w2p.png
    save_path = os.getcwd()
    if (os.path.exists(save_path)):
        save_path = save_path + "/" + name +".png"
    else:
        os.mkdir(save_path)
        save_path = save_path + "/" + name +".png"
    im.save(save_path)
    return save_path

def segment_txt(txt):
    segments = []
    start_idx = 0
    for i in range(len(txt)):
        if txt[i] in ['。', '？', '；', '！'] and (len(txt) > i+1 and txt[i+1] != "”"):
            segments.append(txt[start_idx:i+1])
            start_idx = i + 1
    segments.append(txt[start_idx:])
    return segments

def format_string(s, indent_spaces=4, max_line_length=20, paragraph_spacing=1):
    """
    重新排版字符串，按句号分段落，并添加每行字符数限制的优化。

    :param s: 输入的字符串
    :param indent_spaces: 每个段落前的缩进空格数
    :param max_line_length: 每行的最大字符数（包括空格和缩进）
    :param paragraph_spacing: 段落之间的空行数
    :return: 格式化后的字符串
    """
    # 首先将字符串分割
    paragraphs = segment_txt(s)
    # 格式化后的段落列表
    formatted_paragraphs = []

    for paragraph in paragraphs:
        # 去除段落前后的空格
        clean_paragraph = paragraph.strip()
        news_origin = textwrap.wrap(clean_paragraph, width=max_line_length)
        news_array_oaragraph = []
        parag_num = 0
        for news_line in news_origin:
            start_split = ""
            if (len(news_array_oaragraph) == 0):
                start_split = ''
            # 小于3不分行
            if (len(news_line) < 3 and parag_num > 0):
                news_array_oaragraph[parag_num-1] = news_array_oaragraph[parag_num - 1] + news_line
            else:
                news_array_oaragraph.append(start_split + news_line)
            parag_num = parag_num + 1
        formatted_paragraphs.append("\n".join(news_array_oaragraph))
    return formatted_paragraphs

if __name__ == '__main__':
    niuComment("一句话评论自己的生活", "我年轻着，平凡着，忙碌着。但我对生活一往情深，愿不计算时间。尽最大努力，去做我想象中的自己。", "niu")