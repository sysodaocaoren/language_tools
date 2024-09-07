import cv2
import numpy as np

from PIL import Image


def change_background(image_path, background_color, output_path):
    # 打开图片
    image = Image.open(image_path)
    # 创建一个新的背景图像，与原图大小相同，背景色为你指定的颜色
    background = Image.new('RGB', image.size, background_color)

    # 这里你需要添加代码来区分哪些区域是背景，哪些区域是前景
    # 假设我们直接处理整个图像（这通常不是实际场景）

    # 这里为了示例，我们假设整个图像都是前景，因此直接复制原图到背景上
    # 实际应用中，你可能需要使用图像处理技术（如边缘检测、颜色分割等）来区分背景和前景
    background.paste(image, mask=image.split()[3] if image.mode == 'RGBA' else None)

    # 保存结果
    background.save(output_path)


# 使用示例
change_background('阿豆.jpg', (255, 0, 0), 'output_image.png')  # 白色背景


def replace_color(image_path, old_color, new_color):
    # 加载图片
    image = cv2.imread(image_path)

    # 转换颜色空间，从BGR到RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 创建掩膜，用于找到特定颜色
    h, w = old_color[0], old_color[1]
    mask = cv2.inRange(image, old_color[2:], old_color[2:])

    # 创建一个完全是新颜色的图片
    replacement = image.copy()
    replacement[:] = new_color

    # 应用掩膜，将旧颜色替换为新颜色
    image[mask == 255] = replacement[mask == 255]

    # 转换回BGR颜色空间并保存结果
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite('result.jpg', image)


# 使用示例：将图片底色从白色更换为蓝色
# 白色的OpenCV颜色代码是(255, 255, 255)
# 蓝色的OpenCV颜色代码是(255, 0, 0)
# replace_color('阿豆.jpg', (250, 250, 250), (255, 0, 0))