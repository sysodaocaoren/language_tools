import cv2
import numpy as np
import dlib
import random

# 视频设置
fps = 30  # 帧率（帧每秒）
points_per_frame = 100  # 每帧绘制的点数
output_filename = 'optimized_drawing_with_full_color3.avi'

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
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255  # 创建彩色画布

# 视频输出设置
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

# 灰度处理原始图像
gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
faces = detector(gray_original)

face_masks = []
body_masks = []

# 处理每个人脸，提取面部表情和身体区域
for face in faces:
    landmarks = predictor(gray_original, face)
    face_mask = np.zeros_like(sketch_image)
    body_mask = np.zeros_like(sketch_image)

    # 绘制面部轮廓
    for i in range(17):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        face_mask[y, x] = 255

    # 绘制五官区域
    for i in range(17, 68):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        face_mask[y, x] = 255

    # 人体的估计区域
    body_x1 = face.left() - int(face.width() * 0.2)
    body_y1 = face.bottom()
    body_x2 = face.right() + int(face.width() * 0.2)
    body_y2 = min(height, face.bottom() + face.height() * 2)

    cv2.rectangle(body_mask, (body_x1, body_y1), (body_x2, body_y2), 255, -1)

    face_masks.append(face_mask)
    body_masks.append(body_mask)

# 获取背景掩码
background_mask = np.ones_like(sketch_image) * 255
for face_mask, body_mask in zip(face_masks, body_masks):
    background_mask[face_mask == 255] = 0
    background_mask[body_mask == 255] = 0


# 获取所有需要绘制的像素点
def get_edge_points(edges, region_mask):
    return np.column_stack(np.where((edges != 0) & (region_mask == 255)))


# 获取面部、身体和背景的边缘点
face_edge_points = [get_edge_points(edges, face_mask) for face_mask in face_masks]
body_edge_points = [get_edge_points(edges, body_mask) for body_mask in body_masks]
background_edge_points = get_edge_points(edges, background_mask)

# 准备绘制面部、身体和背景的所有点
all_edge_points = {
    "face": np.vstack(face_edge_points),
    "body": np.vstack(body_edge_points),
    "background": background_edge_points
}


# 绘制函数，使用 NumPy 高效绘制
def draw_pixels(canvas, sketch_image, points, drawn_points):
    # 计算剩余点
    remaining_points = [p for p in points if tuple(p) not in drawn_points]
    print(len(remaining_points))
    if len(remaining_points) == 0:
        return canvas, drawn_points, True  # 如果没有剩余点，返回绘制完成标志

    # 随机选择绘制的点索引
    selected_indices = random.sample(range(len(remaining_points)), min(len(remaining_points), points_per_frame))

    # 获取对应的点
    selected_points = np.array(remaining_points)[selected_indices]

    # 将素描图的颜色直接应用于画布的对应位置
    for (y, x) in selected_points:
        canvas[y, x] = [sketch_image[y, x]] * 3  # 将灰度值扩展到三个通道

    # 更新已绘制的点
    drawn_points.update(map(tuple, selected_points))  # 使用集合加速查找

    return canvas, drawn_points, False  # 返回绘制完成标志


# 按顺序绘制面部、身体和背景
for phase in ["face", "body", "background"]:
    points = all_edge_points[phase]
    drawn_points = set()  # 用于跟踪已绘制的点

    drawing_complete = False
    while not drawing_complete:
        canvas, drawn_points, drawing_complete = draw_pixels(canvas, sketch_image, points, drawn_points)

        # 转换为彩色帧并保存
        video_writer.write(canvas)

# 关闭视频写入
video_writer.release()
