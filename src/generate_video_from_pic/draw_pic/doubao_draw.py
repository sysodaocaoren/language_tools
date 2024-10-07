import cv2
import numpy as np
import math


# 加载素描画图片（这里假设名为'sketch.jpg'的图片在当前目录下）
sketch_image = cv2.imread('paoche.jpg', 0)


# 获取素描画的边缘线条坐标
def get_sketch_lines(image):
    edges = cv2.Canny(image, 50, 150)
    height, width = edges.shape
    line_coords = []
    for y in range(height):
        for x in range(width):
            if edges[y, x]!= 0:
                line_coords.append((x, y))
    return line_coords


# 在白色画布上按照边缘线条坐标绘制图像并生成视频
def draw_sketch():
    height, width = sketch_image.shape
    white_canvas = np.ones((height, width), dtype=np.uint8) * 255

    # 设置视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('drawing_process.avi', fourcc, 10.0, (width, height), isColor=False)

    line_coords = get_sketch_lines(sketch_image)
    line_count = len(line_coords)

    skip_frames = 10  # 每5次绘制操作写入一帧视频
    frame_count = 0

    for i in range(line_count):
        if i > 0:
            prev_x, prev_y = line_coords[i - 1]
            curr_x, curr_y = line_coords[i]
            length = int(math.sqrt((curr_x - prev_x) ** 2+(curr_y - prev_y) ** 2))
            dx = (curr_x - prev_x) / length if length > 0 else 0
            dy = (curr_y - prev_y) / length if length > 0 else 0
            for j in range(1, length + 1):
                x = int(prev_x + j * dx)
                y = int(prev_y + j * dy)
                if 0 <= x < width and 0 <= y < height:
                    cv2.line(white_canvas, (prev_x, prev_y), (x, y), 0, 1)
                    if frame_count % skip_frames == 0:
                        frame = white_canvas.copy()
                        out.write(frame)
                    frame_count += 1
        else:
            x, y = line_coords[0]
            cv2.line(white_canvas, (x, y), (x, y), 0, 1)
            if frame_count % skip_frames == 0:
                frame = white_canvas.copy()
                out.write(frame)
            frame_count += 1

    out.release()


# 执行绘制函数
draw_sketch()
