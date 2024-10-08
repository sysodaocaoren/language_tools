import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
def resize_photo(photo,choice):
    if choice == 1:
        resized_photo = photo.resize((250,350))
        enhancer = ImageEnhance.Sharpness(resized_photo)
        resized_photo = enhancer.enhance(2)
        return resized_photo
    if choice == 2:
        resized_photo = photo.resize((350, 500))
        enhancer = ImageEnhance.Sharpness(resized_photo)
        resized_photo = enhancer.enhance(2)
        return resized_photo
    if choice == 3:
        resized_photo = photo.resize((330, 480))
        enhancer = ImageEnhance.Sharpness(resized_photo)
        resized_photo = enhancer.enhance(2)
        return resized_photo
def cut_photo(photo,choice):
    width = photo.size[0]
    height = photo.size[1]
    rate = height / width
    if choice == 1:
        if rate < (350/250):
            x = (width - int(height / 350 * 250)) / 2
            y = 0
            cutted_photo = photo.crop((x, y, x + (int(height / 350 * 250)), y + height))
        else:
            x = 0
            y = (height - int(width / 250 * 350)) / 2
            cutted_photo = photo.crop((x, y, x + width, y + (int(width / 250 * 350))))
        return cutted_photo
    if choice == 2:
        if rate < (500/350):
            x = (width - int(height / 500* 350)) / 2
            y = 0
            cutted_photo = photo.crop((x, y, x + (int(height / 500* 350)), y + height))
        else:
            x = 0
            y = (height - int(width / 350 * 500)) / 2
            cutted_photo = photo.crop((x, y, x + width, y + (int(width / 350 * 500))))
        return cutted_photo
    if choice == 3:
        if rate < (480/330):
            x = (width - int(height / 480* 330)) / 2
            y = 0
            cutted_photo = photo.crop((x, y, x + (int(height / 480* 330)), y + height))
        else:
            x = 0
            y = (height - int(width / 330 * 480)) / 2
            cutted_photo = photo.crop((x, y, x + width, y + (int(width / 330 * 480))))
        return cutted_photo
try:
    photo = Image.open('阿豆02.jpg')
except:

photo_1 = resize_photo(cut_photo(photo, 1), 1)
width_px, height_px = photo_1.size
txt = str(width_px) + '-' + str(height_px)
print("一寸比列：" + txt)
photo_2 = resize_photo(cut_photo(photo, 2), 2)
width_px, height_px = photo_2.size
txt = str(width_px) + '-' + str(height_px)
print("二寸比列：" + txt)
photo_3 = resize_photo(cut_photo(photo, 3), 3)
width_px, height_px = photo_3.size
txt = str(width_px) + '-' + str(height_px)
print("小二寸比列：" + txt)
# 6寸背景
print_bg = background = Image.new('RGB', (1524, 1016), 'white')
# 1寸证件照布局
print_bg.paste(photo_1, (40, 50))
print_bg.paste(photo_1, (314, 50))
print_bg.paste(photo_1, (598, 50))
print_bg.paste(photo_1, (882, 50))
print_bg.paste(photo_1, (1146, 50))
# 2寸证件照布局
print_bg.paste(photo_1, (40, 440))
print_bg.paste(photo_1, (314, 440))
print_bg.paste(photo_1, (598, 440))
print_bg.paste(photo_1, (882, 440))
print_bg.paste(photo_1, (1146, 440))
# print_bg.paste(photo_2, (40, 440))
# print_bg.paste(photo_2, (405, 440))
# print_bg.paste(photo_2, (770, 440))
# print_bg.paste(photo_2, (1136, 440))

# 小2寸证件照布局
# print_bg.paste(photo_3, (800, 500))
# print_bg.paste(photo_3, (1170, 500))
# 证件图框线
draw = ImageDraw.Draw(print_bg)
# draw.rectangle((30, 100, 248, 450), outline='black', width=0)
# draw.rectangle((304, 100, 502, 450), outline='black', width=0)
# draw.rectangle((588, 100, 756, 450), outline='black', width=0)
# draw.rectangle((872, 100, 1010, 450), outline='black', width=0)
# draw.rectangle((1146, 100, 1264, 450), outline='black', width=0)
#
# draw.rectangle((30, 500, 390, 1000), outline='black', width=0)
# draw.rectangle((400, 500, 780, 1000), outline='black', width=0)
# draw.rectangle((770, 500, 1133, 1000), outline='black', width=0)
# draw.rectangle((1146, 500, 1523, 1000), outline='black', width=0)

path = os.getcwd() + "/6寸混合证件照(画质优化).jpeg"
enhancer = ImageEnhance.Sharpness(print_bg)
print_bg = enhancer.enhance(2)
print_bg.save(path)
print_bg.show()
print("完毕！")