import cv2
import numpy as np
import dlib
import cupy as cp

# 视频设置
duration = 10  # 视频持续时间（秒）
fps = 30       # 帧率（帧每秒）
frames = duration * fps  # 动态计算总帧数
output_filename = 'drawing_process_fixed_fps_with_points_gpu.avi'

# 初始化人脸检测器和特征点检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 读取原始图像和黑白素描画
original_image = cv2.imread('nverguo_ehance.jpg')
sketch_image = cv2.imread('nverguo_sumiao.jpg', cv2.IMREAD_GRAYSCALE)

# 获取图像尺寸
height, width = sketch_image.shape

# 将图像上传到 GPU
gpu_sketch_image = cv2.cuda_GpuMat()
gpu_sketch_image.upload(sketch_image)

# 使用CUDA加速的Canny边缘检测提取素描画中的轮廓
edges_gpu = cv2.cuda_Canny(gpu_sketch_image, 30, 100)
edges = edges_gpu.download()  # 下载回到CPU

# 创建空白画布用于绘制过程
canvas = np.ones((height, width), dtype=np.uint8) * 255

# 将图像转换到GPU上
canvas_gpu = cp.array(canvas)

# 视频输出设置
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height), isColor=True)

# 灰度处理原始图像
gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
faces = detector(gray_original)

face_masks = []
body_masks = []

# 处理每个人脸，提取面部表情和身体区域
for face in faces:
    landmarks = predictor(gray_original, face)
    face_mask = np.zeros_like(edges)  # 这里使用NumPy创建掩码
    body_mask = np.zeros_like(edges)

    # 绘制面部轮廓
    for i in range(17):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        cv2.circle(face_mask, (x, y), 1, 255, -1)  # 使用OpenCV绘制

    # 绘制五官区域
    for i in range(17, 68):
        x = landmarks.part(i).x
        y = landmarks.part(i).y
        cv2.circle(face_mask, (x, y), 1, 255, -1)  # 使用OpenCV绘制

    # 人体的估计区域
    body_x1 = face.left() - int(face.width() * 0.2)
    body_y1 = face.bottom()
    body_x2 = face.right() + int(face.width() * 0.2)
    body_y2 = min(height, face.bottom() + face.height() * 2)

    cv2.rectangle(body_mask, (body_x1, body_y1), (body_x2, body_y2), 255, -1)  # 使用OpenCV绘制

    face_masks.append(face_mask)
    body_masks.append(body_mask)

# 背景掩码（非人物部分）
background_mask = np.ones_like(edges) * 255
for face_mask, body_mask in zip(face_masks, body_masks):
    background_mask[face_mask == 255] = 0
    background_mask[body_mask == 255] = 0

# 动态分配帧数
face_frames = int(frames * 0.5)  # 面部占50%
body_frames = int(frames * 0.3)   # 身体占30%
background_frames = frames - face_frames - body_frames  # 背景占剩余的20%

# 绘制的步长控制
step_size_face = 1  # 脸部更精细的笔触
step_size_body = 3  # 身体使用略粗的笔触
step_size_background = 5  # 背景使用最粗的笔触

# 绘制的点数
points_per_frame = 20  # 每帧绘制的点数

# 绘制过程的控制：根据掩码分区域绘制
def draw_dots(canvas, edges, region_mask, intensity=1, step_size=5, dot_size=1, num_points=20):
    points_drawn = 0
    while points_drawn < num_points:
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)
        if region_mask[y, x] == 255 and edges[y, x] != 0:
            if np.random.rand() < intensity:  # 控制点的密度
                cv2.circle(canvas, (x, y), dot_size, 0, -1)  # 使用OpenCV绘制小点
                points_drawn += 1
    return canvas

# 绘制面部表情
for i in range(face_frames):
    for face_mask in face_masks:
        canvas = draw_dots(canvas, edges, face_mask, intensity=0.9, step_size=step_size_face, dot_size=1, num_points=points_per_frame)
    color_frame = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
    video_writer.write(color_frame)

# 绘制身体轮廓
for i in range(body_frames):
    for body_mask in body_masks:
        canvas = draw_dots(canvas, edges, body_mask, intensity=0.7, step_size=step_size_body, dot_size=2, num_points=points_per_frame)
    color_frame = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
    video_writer.write(color_frame)

# 最后绘制背景
for i in range(background_frames):
    canvas = draw_dots(canvas, edges, background_mask, intensity=0.5, step_size=step_size_background, dot_size=3, num_points=points_per_frame)
    color_frame = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
    video_writer.write(color_frame)

# 关闭视频写入
video_writer.release()
