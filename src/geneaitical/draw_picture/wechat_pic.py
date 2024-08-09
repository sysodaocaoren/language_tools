from PIL import Image, ImageDraw, ImageFont
sihei = "D:\planself\workspace\language_tools\src\\simhei.TTF"
def get_font_render_size(text, font_path, font_size):
    """
    :param text: 文字
    :param font_path: 字体路径
    :param font_size: 字体大小
    :return: tuple 宽高
    """
    canvas = Image.new('RGB', (2048, 2048))
    ImageDraw.Draw(canvas).text((0, 0),
                                text, font=ImageFont.truetype(font_path, font_size))
    bbox = canvas.getbbox()
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def main(text="Hello World", logo_path="002.jpg", save_path="003.jpg",
         font_path=sihei, font_size=25, space_length=20,
         bg_height=64):
    # 计算文字渲染后的长度
    text_width, text_height = get_font_render_size(text, font_path, font_size)
    # 定义背景宽度
    bg_width = text_width + space_length
    # 生成背景
    bg_img = Image.new(mode='RGB', size=(bg_width + 120, bg_height), color="#F5F5F5")

    # 读取头像文件，并绘制头像到背景图片
    logo = Image.open(logo_path, mode="r")
    logo = logo.resize((bg_height, bg_height))
    bg_img.paste(logo, (0, 0))

    # 绘制气泡
    ## 1. 绘制圆角矩形
    x, y, w, h, r = bg_height + space_length, 0, text_width + space_length * 1.5, bg_height, space_length
    fill_color = "#FFFFFF"
    draw_object = ImageDraw.Draw(bg_img)

    draw_object.ellipse((x, y, x + r, y + r), fill=fill_color)
    draw_object.ellipse((x + w - r, y, x + w, y + r), fill=fill_color)
    draw_object.ellipse((x, y + h - r, x + r, y + h), fill=fill_color)
    draw_object.ellipse((x + w - r, y + h - r, x + w, y + h), fill=fill_color)

    draw_object.rectangle((x + r / 2, y, x + w - (r / 2), y + h), fill=fill_color)
    draw_object.rectangle((x, y + r / 2, x + w, y + h - (r / 2)), fill=fill_color)

    ## 2. 绘制三角形 （对话的哪个尖尖）
    draw_object.polygon([
        (bg_height + space_length / 2, bg_height / 2),
        (bg_height + space_length, bg_height / 2 - space_length / 2),
        (bg_height + space_length, bg_height / 2 + space_length / 2),
    ], fill="#FFFFFF")

    ## 3. 绘制字体
    draw_object.text((bg_height + space_length + 15, (bg_height - 25) / 2 - 5 - 1),
                     text, fill=0, font=ImageFont.truetype(font_path, font_size))

    bg_img.save(save_path)


if __name__=="__main__":
    main("我不敢下苦功琢磨自己，怕终于知道自己并非珠玉；\n 然而心中又存着一丝希冀，便又不肯甘心与瓦砾为伍。") # 更改此处文字即可。

