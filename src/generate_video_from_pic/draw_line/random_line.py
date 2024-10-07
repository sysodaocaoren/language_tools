import cv2
import numpy as np
import random


# 创建一个空白的白色图像（这里假设为640x480大小）
width, height = 640, 480
white_paper = np.ones((height, width), dtype=np.uint8) * 255


# 定义一个简单的素描线条绘制函数
def draw_sketch_lines(image, num_lines):
    h, w = image.shape[:2]
    img = image.copy()
    for _ in range(num_lines):
        start_x = random.randint(0, w - 1)
        start_y = random.randint(0, h - 1)
        length = random.randint(10, 100)
        angle = random.uniform(0, 2 * np.pi)
        end_x = int(start_x + length * np.cos(angle))
        end_y = int(start_y + length * np.sin(angle))
        if end_x < 0:
            end_x = 0
        if end_x > w - 1:
            end_x = w - 1
        if end_y < 0:
            end_y = 0
        if end_y > h - 1:
            end_y = h - 1
        cv2.line(img, (start_x, start_y), (end_x, end_y), 0, 1)
    return img


# 设置视频编码器
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# 创建VideoWriter对象，输出文件名为 'output.avi'，帧率为10.0，视频尺寸与图像一致
out = cv2.VideoWriter('output.avi', fourcc, 10.0, (width, height), isColor=False)


# 逐渐增加线条数量来生成视频帧
num_lines_per_frame = 1
for num_lines in range(1, 1000, num_lines_per_frame):
    frame = draw_sketch_lines(white_paper, num_lines_per_frame)
    out.write(frame)


# 释放资源
out.release()
