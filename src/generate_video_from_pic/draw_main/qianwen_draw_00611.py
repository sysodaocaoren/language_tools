import cv2
import numpy as np
import dlib
from concurrent.futures import ThreadPoolExecutor

# 视频设置
fps = 30  # 帧率（帧每秒）
total_duration = 75  # 总时长（秒）

# 绘制时间分配（秒）
times = {
    'contour': 3,
    'left_eyebrow': 2,
    'right_eyebrow': 2,
    'right_eye_outline': 2,
    'right_eye_ball': 2,
    'left_eye_outline': 2,
    'left_eye_ball': 2,
    'nose': 2,
    'mouth': 3,
    'jaw': 2,
    'background': 20,
    'coloring': 30
}

# 计算每阶段的总帧数
frames = {key: int(value * fps) for key, value in times.items()}

# 输出视频文件名
output_filename = 'final_drawing_with_optimization.avi'

# 轮廓绘制比例
contour_ratio = 0.3
# 绘画比例
drawing_ratio = 0.7
# 上色比例
coloring_ratio = 0.6

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

# 获取面部特征点列表
face_landmarks = []
for face in faces:
    landmarks = predictor(gray_original, face)
    points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(0, 68)]
    face_landmarks.append(points)


# 扩展面部区域
def expand_face_region(face_landmarks, scale=1.2):
    expanded_regions = []
    for landmarks in face_landmarks:
        jaw = landmarks[0:17]  # 面部轮廓

        # 计算凸包来得到面部的不规则边缘
        hull = cv2.convexHull(np.array(jaw))

        # 创建一个空的掩膜
        mask = np.zeros((height, width), dtype=np.uint8)

        # 在掩膜上填充凸包区域
        cv2.fillConvexPoly(mask, hull, 1)

        # 使用膨胀操作来扩展面部区域
        kernel = np.ones((3, 3), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=int(scale * 1.5))

        # 将膨胀后的掩膜转换为点集
        expanded_points = np.column_stack(np.where(dilated_mask == 1))

        expanded_regions.append(expanded_points)
    return expanded_regions


# 绘制轮廓
def draw_contour(canvas, edges, contour_ratio, frames):
    print("开始绘制轮廓...")
    edge_points = np.column_stack(np.where(edges != 0))
    np.random.shuffle(edge_points)  # Shuffle to randomize order of drawing

    # 选择30%的点进行轮廓绘制
    num_points_to_draw = int(len(edge_points) * contour_ratio)
    points_to_draw = edge_points[:num_points_to_draw]

    points_drawn = 0
    total_points = len(points_to_draw)
    while points_drawn < len(points_to_draw) and frames > 0:
        frame_points = min(int(total_points / frames), len(points_to_draw) - points_drawn)
        for i in range(frame_points):
            point = points_to_draw[points_drawn + i]
            y, x = point
            canvas[y, x] = [sketch_image[y, x]] * 3
        video_writer.write(canvas)
        points_drawn += frame_points
        frames -= 1
        progress = (points_drawn / total_points) * 100
        print(f"绘制轮廓进度: {progress:.2f}% ({points_drawn}/{total_points})")

    # 返回剩余的点
    remaining_points = edge_points[num_points_to_draw:]
    return remaining_points, frames


# 获取面部区域
def get_face_region(landmarks):
    left_eye = landmarks[36:42]  # 左眼
    right_eye = landmarks[42:48]  # 右眼
    nose = landmarks[27:36]  # 鼻子
    mouth = landmarks[48:60]  # 嘴巴
    jaw = landmarks[0:17]  # 面部轮廓
    left_eyebrow = landmarks[17:22]  # 左眉毛
    right_eyebrow = landmarks[22:27]  # 右眉毛

    # 假设没有耳朵的特征点
    left_ear = []
    right_ear = []

    return left_eye, right_eye, nose, mouth, jaw, left_eyebrow, right_eyebrow, left_ear, right_ear


# 辅助函数：绘制特定区域
def draw_region(canvas, region_points, drawn_points, region_name, frames, edges, direction=None):
    mask = np.zeros_like(sketch_image)
    region_array = np.array(region_points, np.int32)
    cv2.fillConvexPoly(mask, region_array, 255)

    # 获取边缘点
    region_edge_points = np.column_stack(np.where((edges != 0) & (mask == 255)))
    np.random.shuffle(region_edge_points)  # Shuffle to randomize order of drawing

    # 根据方向绘制
    if direction == 'up':
        region_edge_points = sorted(region_edge_points, key=lambda p: p[0], reverse=True)
    elif direction == 'down':
        region_edge_points = sorted(region_edge_points, key=lambda p: p[0])
    elif direction == 'left':
        region_edge_points = sorted(region_edge_points, key=lambda p: p[1])
    elif direction == 'right':
        region_edge_points = sorted(region_edge_points, key=lambda p: p[1], reverse=True)

    # 逐点绘制
    points_drawn = 0
    total_points = len(region_edge_points)
    while points_drawn < len(region_edge_points) and frames > 0:
        frame_points = min(int(total_points / frames), len(region_edge_points) - points_drawn)
        for i in range(frame_points):
            point = region_edge_points[points_drawn + i]
            y, x = point
            if (y, x) not in drawn_points:
                canvas[y, x] = [sketch_image[y, x]] * 3
                drawn_points.add((y, x))
        video_writer.write(canvas)
        points_drawn += frame_points
        frames -= 1
        progress = (points_drawn / total_points) * 100
        print(f"{region_name} 绘制进度: {progress:.2f}% ({points_drawn}/{total_points})")

    return frames

def draw_background_point(point, canvas, drawn_points, sketch_image):
    y, x = point
    if (y, x) not in drawn_points:
        canvas[y, x] = [sketch_image[y, x]] * 3
        drawn_points.add((y, x))

def draw_background_in_parallel(background_points, canvas, drawn_points, sketch_image, frames):
    with ThreadPoolExecutor() as executor:
        futures = []
        points_per_frame = len(background_points) // frames['background']
        for i in range(0, len(background_points), points_per_frame):
            futures.append(executor.submit(
                lambda ps: [draw_background_point(p, canvas, drawn_points, sketch_image) for p in ps],
                background_points[i:i + points_per_frame]
            ))
        for future in futures:
            future.result()
        video_writer.write(canvas)

# 主程序
if __name__ == "__main__":
    # 1. 绘制轮廓
    remaining_points, contour_frames_remaining = draw_contour(canvas, edges, contour_ratio, frames['contour'])

    # 2. 绘制详细部分
    print("开始绘制详细部分...")
    drawn_points = set()
    for landmarks in face_landmarks:
        # 获取面部的不同部分
        left_eye, right_eye, nose, mouth, jaw, left_eyebrow, right_eyebrow, left_ear, right_ear = get_face_region(
            landmarks)

        # 打印各区域的点数量
        print(f"左眉毛点数: {len(left_eyebrow)}")
        print(f"右眉毛点数: {len(right_eyebrow)}")
        print(f"左眼点数: {len(left_eye)}")
        print(f"右眼点数: {len(right_eye)}")

        # 绘制左眉毛，从左向右画
        frames['left_eyebrow'] = draw_region(canvas, left_eyebrow, drawn_points, 'left_eyebrow', frames['left_eyebrow'],
                                             edges, 'right')
        print("绘制左眉毛完成")

        # 绘制右眉毛，从左向右画
        frames['right_eyebrow'] = draw_region(canvas, right_eyebrow, drawn_points, 'right_eyebrow', frames['right_eyebrow'], edges, 'right')
        print("绘制右眉毛完成")

        # 绘制右眼轮廓，从上往下画
        frames['right_eye_outline'] = draw_region(canvas, right_eye, drawn_points, 'right_eye_outline', frames['right_eye_outline'], edges, 'down')
        print("绘制右眼轮廓完成")

        # 绘制右眼眼球，从上往下画
        right_eye_center = np.mean(right_eye, axis=0).astype(int)
        right_eye_ball_mask = np.zeros_like(sketch_image)
        cv2.circle(right_eye_ball_mask, tuple(right_eye_center), 10, 255, -1)
        right_eye_ball_points = np.column_stack(np.where((edges != 0) & (right_eye_ball_mask == 255)))
        np.random.shuffle(right_eye_ball_points)
        for point in right_eye_ball_points:
            y, x = point
            if (y, x) not in drawn_points:
                canvas[y, x] = [sketch_image[y, x]] * 3
                drawn_points.add((y, x))
                video_writer.write(canvas)
        print("绘制右眼眼球完成")

        # 绘制左眼轮廓，从上往下画
        frames['left_eye_outline'] = draw_region(canvas, left_eye, drawn_points, 'left_eye_outline',
                                                 frames['left_eye_outline'], edges, 'down')
        print("绘制左眼轮廓完成")

        # 绘制左眼眼球，从上往下画
        left_eye_center = np.mean(left_eye, axis=0).astype(int)
        left_eye_ball_mask = np.zeros_like(sketch_image)
        cv2.circle(left_eye_ball_mask, tuple(left_eye_center), 10, 255, -1)
        left_eye_ball_points = np.column_stack(np.where((edges != 0) & (left_eye_ball_mask == 255)))
        np.random.shuffle(left_eye_ball_points)
        for point in left_eye_ball_points:
            y, x = point
            if (y, x) not in drawn_points:
                canvas[y, x] = [sketch_image[y, x]] * 3
                drawn_points.add((y, x))
                video_writer.write(canvas)
        print("绘制左眼眼球完成")

        # 绘制鼻子，从上往下画
        frames['nose'] = draw_region(canvas, nose, drawn_points, 'nose', frames['nose'], edges, 'down')
        print("绘制鼻子完成")

        # 绘制嘴巴，从下往上画
        frames['mouth'] = draw_region(canvas, mouth, drawn_points, 'mouth', frames['mouth'], edges, 'up')
        print("绘制嘴巴完成")

        # 绘制面部轮廓
        frames['jaw'] = draw_region(canvas, jaw, drawn_points, 'jaw', frames['jaw'], edges, 'down')
        print("绘制面部轮廓完成")

    ## 使用剩余的点绘制面部框外扩散区域
    # 提前计算背景区域的所有点
    background_points = []
    for landmarks in face_landmarks:
        jaw = landmarks[0:17]
        # 创建一个空的掩膜
        mask = np.zeros((height, width), dtype=np.uint8)
        # 在掩膜上填充凸包区域
        cv2.fillConvexPoly(mask, np.array(jaw, np.int32), 1)
        # 使用膨胀操作来扩展面部区域
        kernel = np.ones((3, 3), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=int(1.5))
        # 将膨胀后的掩膜转换为点集
        expanded_points = np.column_stack(np.where(dilated_mask == 1))
        # 计算非面部区域
        non_face_mask = np.ones_like(mask) * 255
        cv2.fillConvexPoly(non_face_mask, np.array(jaw, np.int32), 0)
        non_face_points = np.column_stack(np.where((edges == 0) & (non_face_mask == 255)))
        # 合并非面部区域和面部区域
        background_points.extend(expanded_points)
        background_points.extend(non_face_points)

    # 随机打乱所有背景点
    np.random.shuffle(background_points)

    # 逐点绘制背景
    points_drawn = 0
    total_points = len(background_points)
    while points_drawn < len(background_points) and frames['background'] > 0:
        frame_points = min(int(total_points / frames['background']), len(background_points) - points_drawn)
        # 这里传递一部分点到并行绘制函数
        draw_background_in_parallel(background_points[points_drawn:points_drawn + frame_points],
                                    canvas, drawn_points, sketch_image, frames)
        points_drawn += frame_points
        frames['background'] -= 1
        progress = (points_drawn / total_points) * 100
        print(f"绘制背景区域进度: {progress:.2f}% ({points_drawn}/{total_points})")

    print("绘制背景区域完成")


    # 3. 上色
    print("开始上色...")
    expanded_face_regions = expand_face_region(face_landmarks)

    # 获取所有点（包括面部和非面部区域）
    all_points = []
    for expanded_points in expanded_face_regions:
        all_points.extend(expanded_points)

    # 获取非面部区域的非边缘点
    non_face_mask = np.ones_like(edges) * 255
    for landmarks in face_landmarks:
        jaw = landmarks[0:17]
        jaw_poly = np.array(jaw, np.int32)
        cv2.fillConvexPoly(non_face_mask, jaw_poly, 0)

    non_face_points = np.column_stack(np.where((edges == 0) & (non_face_mask == 255)))
    all_points.extend(non_face_points)

    # 随机打乱所有点
    np.random.shuffle(all_points)

    # 上色
    points_colored = 0
    total_points = len(all_points) * coloring_ratio
    while points_colored < len(all_points) and frames['coloring'] > 0:
        frame_points = min(int(total_points / frames['coloring']), total_points - points_colored)
        for i in range(frame_points):
            point = all_points[points_colored + i]
            y, x = point
            canvas[y, x] = original_image[y, x]
        video_writer.write(canvas)
        points_colored += frame_points
        frames['coloring'] -= 1
        progress = (points_colored / total_points) * 100
        print(f"上色进度: {progress:.2f}% ({points_colored}/{total_points})")

    print("上色完成")

    # 完成绘制
    video_writer.release()