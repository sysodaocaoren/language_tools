import cv2
import numpy as np
import dlib
import time

# 视频设置
fps = 30  # 帧率（帧每秒）
points_per_frame_face = 150  # 面部框内每帧绘制的点数
points_per_frame_non_face = 350  # 面部框外每帧绘制的点数
output_filename = 'final_drawing_with_delay.avi'

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

# 检测到面部特征区域（眼睛、鼻子、嘴巴等）
face_landmarks = []
for face in faces:
    landmarks = predictor(gray_original, face)
    points = []
    for n in range(0, 68):
        points.append((landmarks.part(n).x, landmarks.part(n).y))
    face_landmarks.append(points)


# 绘制特定区域（眼睛、鼻子、嘴巴等）的函数
def draw_region(canvas, region_points, drawn_points, region_name):
    mask = np.zeros_like(sketch_image)
    region_array = np.array(region_points, np.int32)
    cv2.fillConvexPoly(mask, region_array, 255)

    # 获取边缘点
    region_edge_points = np.column_stack(np.where((edges != 0) & (mask == 255)))

    for point in region_edge_points:
        y, x = point
        if (y, x) not in drawn_points:
            canvas[y, x] = [sketch_image[y, x]] * 3
            drawn_points.add((y, x))
            # 在每次绘制后添加延时
            time.sleep(0.001) # 每个点绘制后等待10毫秒
    return canvas, drawn_points


# 获取面部区域
def get_face_region(landmarks):
    left_eye = landmarks[36:42]  # 左眼
    right_eye = landmarks[42:48]  # 右眼
    nose = landmarks[27:36]  # 鼻子
    mouth = landmarks[48:60]  # 嘴巴
    jaw = landmarks[0:17]  # 面部轮廓
    return left_eye, right_eye, nose, mouth, jaw


# 初始化绘制过程
drawn_points = set()

# 主绘制循环
for landmarks in face_landmarks:
    left_eye, right_eye, nose, mouth, jaw = get_face_region(landmarks)

    # 先绘制眼睛
    canvas, drawn_points = draw_region(canvas, left_eye, drawn_points, 'left_eye')
    canvas, drawn_points = draw_region(canvas, right_eye, drawn_points, 'right_eye')

    # 再绘制鼻子
    canvas, drawn_points = draw_region(canvas, nose, drawn_points, 'nose')

    # 绘制嘴巴
    canvas, drawn_points = draw_region(canvas, mouth, drawn_points, 'mouth')

    # 最后绘制面部轮廓
    canvas, drawn_points = draw_region(canvas, jaw, drawn_points, 'jaw')

    video_writer.write(canvas)

# 绘制面部框外扩散区域
background_mask = np.ones_like(sketch_image) * 255
for landmarks in face_landmarks:
    jaw = landmarks[0:17]
    jaw_poly = np.array(jaw, np.int32)
    cv2.fillConvexPoly(background_mask, jaw_poly, 0)

background_edge_points = np.column_stack(np.where((edges != 0) & (background_mask == 255)))

# 处理面部框外区域，按照一定顺序扩散
expand_radius = 10
while len(background_edge_points) > 0:
    region_to_draw = []
    for point in background_edge_points:
        y, x = point
        if any([abs(y - jaw_point[1]) <= expand_radius and abs(x - jaw_point[0]) <= expand_radius for jaw_point in
                jaw]):
            region_to_draw.append(point)

    # 更新画布并记录已绘制点
    for point in region_to_draw:
        y, x = point
        if (y, x) not in drawn_points:
            canvas[y, x] = [sketch_image[y, x]] * 3
            drawn_points.add((y, x))
            # 在每次绘制后添加延时
            time.sleep(0.001) # 每个点绘制后等待10毫秒

    # 扩展范围
    expand_radius += 10
    background_edge_points = [point for point in background_edge_points if (point[0], point[1]) not in drawn_points]
    video_writer.write(canvas)

# 完成绘制
video_writer.release()
