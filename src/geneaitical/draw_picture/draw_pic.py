from PIL import Image, ImageFont, ImageDraw
import os
import textwrap

home_path = 'D:\planself\workspace\language_tools\src'
# home_path = 'G:\workspace\language_tools\src'

word_num_line = 25
news_font_path = home_path + "\\STXINWEI.TTF"
xingkai = home_path + "\\STXINGKA.TTF"
fangzheng = home_path + "\\FZSTK.TTF"
sihei = home_path + "\\simhei.TTF"
simkai = home_path + "\\simkai.ttf"
youyuan =  home_path + "\\SIMYOU.ttf"

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
    new_h = 25 * len(news_text.split("\n")) + 5
    all_h = 25 * len(news_text.split("\n")) + comment_h + 40 + 20
    w = int(word_num_line * 19.5 + 35)
    im = Image.new("RGB", (w, all_h), (230, 240, 230))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(xingkai, 20)
    dr.text((5, 5), news_text, font=font, fill="#000000")
    # 发布时间地点
    create_time_font = ImageFont.truetype(simkai, 15)
    dr.text((8, new_h), str(new_time) + " . " + new_location, font=create_time_font, fill="#808080")
    dr.text((w - 200, new_h), '回复('+str(new_comment_count)+')  点赞('+str(news_vote_count)+')', font=create_time_font, fill="#808080")
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
        save_path = save_path + "/" + name + ".png"
    else:
        os.mkdir(save_path)
        save_path = save_path + "/" + name + ".png"
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
    new_h = 25 * len(news_text.split("\n")) + 5
    all_h = 25 * len(news_text.split("\n")) + comment_h + 40 + 20
    w = int(word_num_line * 19.5 + 35)
    im = Image.new("RGB", (w, all_h), (60, 60, 60))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(youyuan, 20)
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

if __name__ == '__main__':
    niuComment("一句话评论自己的生活", "我年轻着，平凡着，忙碌着，但我对生活一往情深，愿不计算时间，尽最大努力，去做我想象中的自己。", "niu")