import cv2
import numpy as np
import dlib
import random

# 视频设置
fps = 30  # 帧率
points_per_frame_face = 100  # 面部框内每帧绘制的点数
points_per_frame_non_face = 500  # 面部框外每帧绘制的点数
expand_step = 10  # 扩展像素数
output_filename = 'improved_drawing.avi'

# 初始化人脸检测器和特征点检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 读取原始图像和黑白素描画
original_image = cv2.imread('nverguo_ehance.jpg')
sketch_image = cv2.imread('nverguo_sumiao.jpg', cv2.IMREAD_GRAYSCALE)

# 获取图像尺寸
height, width = sketch_image.shape

# 使用Canny边缘检测提取素描画中的轮廓
edges = cv2.Canny(sketch_image, 30, 100)

# 创建空白画布用于绘制过程
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

# 视频输出设置
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height), isColor=True)

# 灰度处理原始图像
gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
faces = detector(gray_original)

# 检测到的人脸框
face_rects = []

# 处理检测到的人脸，放大矩形框并记录
for face in faces:
    x, y, w, h = face.left(), face.top(), face.width(), face.height()

    # 扩大面部框尺寸1.2倍
    padding_w = int(w * 0.1)
    padding_h = int(h * 0.1)

    x1 = max(0, x - padding_w)
    y1 = max(0, y - padding_h)
    x2 = min(width, x + w + padding_w)
    y2 = min(height, y + h + padding_h)

    face_rects.append((x1, y1, x2, y2))

# 优先绘制的区域：眼睛，鼻子，嘴巴（按4x4网格分块）
def divide_face_into_blocks(face_rect, grid_size=4):
    x1, y1, x2, y2 = face_rect
    block_width = (x2 - x1) // grid_size
    block_height = (y2 - y1) // grid_size

    blocks = []
    for row in range(grid_size):
        for col in range(grid_size):
            bx1 = x1 + col * block_width
            by1 = y1 + row * block_height
            bx2 = min(bx1 + block_width, x2)
            by2 = min(by1 + block_height, y2)
            blocks.append((bx1, by1, bx2, by2))

    # 按顺序绘制眼睛(靠近顶部中间的块)、鼻子(中间偏下)、嘴巴(底部中间)
    order = [(1, 1), (0, 1), (1, 2), (0, 2), (2, 1), (2, 2), (3, 1), (3, 2),
             (0, 0), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0), (3, 3)]
    return [blocks[4 * r + c] for r, c in order]

# 获取所有边缘点
def get_edge_points(edges, region_mask):
    return np.column_stack(np.where((edges != 0) & (region_mask == 255)))

# 获取面部区域边缘点
face_edge_points = []
for face_rect in face_rects:
    x1, y1, x2, y2 = face_rect
    face_mask = np.zeros_like(sketch_image)
    face_mask[y1:y2, x1:x2] = 255
    face_edge_points.append(get_edge_points(edges, face_mask))

# 绘制面部框内区域，按网格顺序绘制
def draw_face_blocks(canvas, face_points, face_rect, drawn_points_face):
    remaining_points = face_points[~np.isin(face_points, list(drawn_points_face), assume_unique=True).all(axis=1)]

    if len(remaining_points) > 0:
        blocks = divide_face_into_blocks(face_rect)
        for block in blocks:
            x1, y1, x2, y2 = block
            block_points = remaining_points[(remaining_points[:, 1] >= x1) & (remaining_points[:, 1] < x2) &
                                            (remaining_points[:, 0] >= y1) & (remaining_points[:, 0] < y2)]
            if len(block_points) > 0:
                selected_points = block_points[:min(points_per_frame_face, len(block_points))]
                for point in selected_points:
                    y, x = point
                    canvas[y, x] = [sketch_image[y, x]] * 3
                    drawn_points_face.add((y, x))
                return canvas, drawn_points_face, False
    return canvas, drawn_points_face, True

# 面部框外扩散绘制
def draw_outside_face(canvas, background_edge_points, drawn_points_outside, expand_radius):
    remaining_points = background_edge_points[
        ~np.isin(background_edge_points, list(drawn_points_outside), assume_unique=True).all(axis=1)]

    if len(remaining_points) > 0:
        # 随机选择面部框周围的点
        selected_points = []

        for point in remaining_points:
            y, x = point

            # 检查点是否在扩散半径范围内
            for (x1, y1, x2, y2) in face_rects:
                if abs(y - (y1 + y2) // 2) <= expand_radius and abs(x - (x1 + x2) // 2) <= expand_radius:
                    selected_points.append(point)
                    break

        # 选择最多 points_per_frame_non_face 个点进行绘制
        selected_points = selected_points[:min(points_per_frame_non_face, len(selected_points))]

        for point in selected_points:
            y, x = point
            canvas[y, x] = [sketch_image[y, x]] * 3
            drawn_points_outside.add((y, x))

        return canvas, drawn_points_outside, False
    return canvas, drawn_points_outside, True

# 获取背景掩码
background_mask = np.ones_like(sketch_image) * 255
for face_rect in face_rects:
    x1, y1, x2, y2 = face_rect
    background_mask[y1:y2, x1:x2] = 0
background_edge_points = get_edge_points(edges, background_mask)

# 初始化绘制过程
drawn_points_outside = set()
drawn_points_face = set()
expand_radius = expand_step

# 绘制主循环
while True:
    complete = True
    for face_points, face_rect in zip(face_edge_points, face_rects):
        canvas, drawn_points_face, finished = draw_face_blocks(canvas, face_points, face_rect, drawn_points_face)
        video_writer.write(canvas)
        complete &= finished

    canvas, drawn_points_outside, finished = draw_outside_face(canvas, background_edge_points, drawn_points_outside, expand_radius)
    video_writer.write(canvas)
    expand_radius += expand_step
    complete &= finished

    if complete:
        break

# 关闭视频写入
video_writer.release()
