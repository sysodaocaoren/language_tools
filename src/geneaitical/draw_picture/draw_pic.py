from PIL import Image, ImageFont, ImageDraw
import os
import textwrap

def w2p(text, name, cutline=True):
    # 文字自动换行
    if cutline:
        sptext = text.split("\n")
        hlen = len(sptext)
        for i in range(hlen):
            sptext[i] = "\n".join(textwrap.wrap(sptext[i], width=35))
        text = "\n".join(sptext)

    # 获取文字列表的最大字符数量
    max_len = 0
    for item in text.split("\n"):
        if len(item) > max_len:
            max_len = len(item)

    # 转换文字为图片并保存为图片
    h = 26 * len(text.split("\n")) + 10
    w = int(max_len * 19.5 + 30)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    fpath = "D:\planself\workspace\language_tools\src\\方正楷体简体.TTF"
    font = ImageFont.truetype(fpath, 20)
    dr.text((5, 5), text, font=font, fill="#000000")

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
    w2p("你真是个好人")