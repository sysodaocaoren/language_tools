from PIL import Image, ImageFont, ImageDraw
import os
import textwrap

word_num_line = 20
news_font_path = "D:\planself\workspace\language_tools\src\\STXINWEI.TTF"
fangzheng = "D:\planself\workspace\language_tools\src\\FZSTK.TTF"
sihei = "D:\planself\workspace\language_tools\src\\simhei.TTF"

def niuComment(news, comment, name):
    news_origin = news.replace("\n", "")
    news_origin = textwrap.wrap(news_origin, width=word_num_line)
    news_text = "\n".join(news_origin)

    comment_origin = comment.replace("\n", "")
    comment_origin = textwrap.wrap(comment_origin, width=word_num_line + 3)
    comment_text = "\n".join(comment_origin)

    # 处理正文的图片
    new_h = 26 * len(news_text.split("\n")) + 5
    all_h = 26 * len(news_text.split("\n") + comment_text.split("\n")) + 40 + 20
    w = int(word_num_line * 19.5 + 35)
    im = Image.new("RGB", (w, all_h), (230, 240, 230))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(news_font_path, 20)
    dr.text((5, 5), news_text, font=font, fill="#000000")
    # 发布时间地点
    create_time_font = ImageFont.truetype(sihei, 15)
    dr.text((8, new_h), '20分钟前 . 上海', font=create_time_font, fill="#808080")
    dr.text((w - 160, new_h), '回复(106)  点赞(22)', font=create_time_font, fill="#808080")
    # 评论发布者名称 时间 地址
    comment_time_font = ImageFont.truetype(sihei, 12)
    dr.text((8, new_h + 24), '我是一棵葱:    20分钟前 . 山东', font=comment_time_font, fill="#809080")
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

    # 插入评论头像


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