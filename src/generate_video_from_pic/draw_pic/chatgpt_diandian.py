import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图片
image_path = 'later-002.jpg'  # 替换为你的素描图片路径
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 以灰度图模式读取

# 获取图片的尺寸
height, width = img.shape

# 创建一个空白画布
canvas = np.ones((height, width), dtype=np.uint8) * 255  # 创建白色画布

# 创建视频输出
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
fps = 10  # 帧率，可以根据需求调整
out = cv2.VideoWriter('drawing_process.mp4', fourcc, fps, (width, height), False)  # False代表灰度图

# 将图像进行阈值处理，确保只有两种颜色（黑/白）
_, img_thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

# 获取非零像素的索引列表（这些像素为黑色，是我们要逐步绘制的部分）
non_zero_pixels = np.column_stack(np.where(img_thresh > 0))

# 打乱这些像素的顺序，模拟随机绘制的过程
np.random.shuffle(non_zero_pixels)

# 逐步绘制
step_size = 200  # 每帧绘制的像素点数量，越大视频越短

for i in range(0, len(non_zero_pixels), step_size):
    # 获取当前步要绘制的像素位置
    for pixel in non_zero_pixels[i:i + step_size]:
        y, x = pixel
        canvas[y, x] = 0  # 将画布对应像素点置为黑色（即绘制出来）
    # 写入当前帧到视频
    out.write(canvas)

# 释放视频资源
out.release()
