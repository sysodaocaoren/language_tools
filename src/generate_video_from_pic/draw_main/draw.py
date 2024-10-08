from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import cv2 as cv2
import numpy as np
import os

step_size = 200  # 每帧绘制的像素点数量，越大视频越短

# 提高照片分辨率
def ehance_image(image_path, image_path_ehance):
    image = Image.open(image_path)
    # 先放大
    resized_image = image.resize((1920, 1080))
    # 高清出来
    enhancer = ImageEnhance.Sharpness(resized_image)
    resized_image = enhancer.enhance(2)
    resized_image.save(image_path_ehance)

# 将原始图片转为素描画
def resolve_image_sumiao(image_path, target_path):
    image = cv2.imread(image_path)
    # 检查图片是否正确加载
    if image is None:
        print(f"Error: 当前图片加载失败 {image_path}")
    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blurred = 255 - blurred
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    # 保存素描到文件
    cv2.imwrite(target_path, pencil_sketch)

def generate_diancai(image_path, vodeo_path):
    # 读取图片
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 以灰度图模式读取

    # 获取图片的尺寸
    height, width = img.shape

    # 创建一个空白画布
    canvas = np.ones((height, width), dtype=np.uint8) * 255  # 创建白色画布

    # 创建视频输出
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
    fps = 10  # 帧率，可以根据需求调整
    out = cv2.VideoWriter(vodeo_path, fourcc, fps, (width, height), False)  # False代表灰度图

    # 将图像进行阈值处理，确保只有两种颜色（黑/白）
    _, img_thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # 获取非零像素的索引列表（这些像素为黑色，是我们要逐步绘制的部分）
    non_zero_pixels = np.column_stack(np.where(img_thresh > 0))

    # 打乱这些像素的顺序，模拟随机绘制的过程
    np.random.shuffle(non_zero_pixels)



    for i in range(0, len(non_zero_pixels), step_size):
        # 获取当前步要绘制的像素位置
        for pixel in non_zero_pixels[i:i + step_size]:
            y, x = pixel
            canvas[y, x] = 0  # 将画布对应像素点置为黑色（即绘制出来）
        # 写入当前帧到视频
        out.write(canvas)

    # 释放视频资源
    out.release()

if __name__ == '__main__':
    # 文件类型
    image_type = ".jpg"
    # 原始文件名称
    image_name = "nverguo"
    # 原始文件路径
    image_path = image_name + image_type
    # 高清处理过的文件
    image_path_ehance = image_name + "_ehance" + image_type

    # 对文件进行高清处理
    ehance_image(image_path, image_path_ehance)

    #对文件进行素描画处理
    image_sumiao = image_name + "_sumiao" + image_type
    resolve_image_sumiao(image_path_ehance, image_sumiao)

    # 生成点彩画视频
    video_path = image_name + "_progress.mp4"
    generate_diancai(image_sumiao, video_path)
