import cv2
import numpy as np
import dlib

# 视频设置
fps = 30  # 帧率（帧每秒）
points_per_frame_face = 150  # 面部框内每帧绘制的点数
points_per_frame_non_face = 300  # 面部框外每帧绘制的点数
coloring_speed_factor = 2  # 上色速度因子
output_filename = 'final_drawing_with_optimization.avi'

# 轮廓绘制比例
contour_ratio = 0.3
# 绘画比例
drawing_ratio = 0.7
# 上色比例
coloring_ratio = 0.5

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


# 获取面部区域
def get_face_region(landmarks):
    left_eye = landmarks[36:42]  # 左眼
    right_eye = landmarks[42:48]  # 右眼
    nose = landmarks[27:36]  # 鼻子
    mouth = landmarks[48:60]  # 嘴巴
    jaw = landmarks[0:17]  # 面部轮廓
    left_eyebrow = landmarks[17:22]  # 左眉毛
    right_eyebrow = landmarks[22:27]  # 右眉毛
    left_ear = landmarks[0:2]  # 左耳
    right_ear = landmarks[14:17]  # 右耳
    return left_eye, right_eye, nose, mouth, jaw, left_eyebrow, right_eyebrow, left_ear, right_ear


# 绘制轮廓
def draw_contour(canvas, edges, contour_ratio, points_per_frame_face):
    print("开始绘制轮廓...")
    edge_points = np.column_stack(np.where(edges != 0))
    np.random.shuffle(edge_points)  # Shuffle to randomize order of drawing

    # 选择30%的点进行轮廓绘制
    num_points_to_draw = int(len(edge_points) * contour_ratio)
    points_to_draw = edge_points[:num_points_to_draw]

    points_drawn = 0
    total_points = len(points_to_draw)
    while points_drawn < len(points_to_draw):
        frame_points = min(points_per_frame_face, len(points_to_draw) - points_drawn)
        for i in range(frame_points):
            point = points_to_draw[points_drawn + i]
            y, x = point
            canvas[y, x] = [sketch_image[y, x]] * 3
        video_writer.write(canvas)
        points_drawn += frame_points
        progress = (points_drawn / total_points) * 100
        print(f"绘制轮廓进度: {progress:.2f}% ({points_drawn}/{total_points})")

    # 返回剩余的点
    remaining_points = edge_points[num_points_to_draw:]
    return remaining_points


# 绘制详细部分
def draw_detailed(canvas, edges, face_landmarks, remaining_points, drawing_ratio, points_per_frame_face,
                  points_per_frame_non_face):
    print("开始绘制详细部分...")
    drawn_points = set()

    # 绘制面部区域
    for landmarks in face_landmarks:
        left_eye, right_eye, nose, mouth, jaw, left_eyebrow, right_eyebrow, left_ear, right_ear = get_face_region(
            landmarks)

        # 绘制左眉毛，从左向右画
        canvas, drawn_points = draw_region(canvas, left_eyebrow, drawn_points, 'left_eyebrow', points_per_frame_face,
                                           edges, 'right')
        print("绘制左眉毛完成")

        # 绘制右眉毛，从左向右画
        canvas, drawn_points = draw_region(canvas, right_eyebrow, drawn_points, 'right_eyebrow', points_per_frame_face,
                                           edges, 'right')
        print("绘制右眉毛完成")

        # 绘制右眼轮廓，从上往下画
        canvas, drawn_points = draw_region(canvas, right_eye, drawn_points, 'right_eye', points_per_frame_face, edges,
                                           'down')
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
        canvas, drawn_points = draw_region(canvas, left_eye, drawn_points, 'left_eye', points_per_frame_face, edges,
                                           'down')
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
        canvas, drawn_points = draw_region(canvas, nose, drawn_points, 'nose', points_per_frame_face, edges, 'down')
        print("绘制鼻子完成")

        # 绘制嘴巴，从下往上画
        canvas, drawn_points = draw_region(canvas, mouth, drawn_points, 'mouth', points_per_frame_face, edges, 'up')
        print("绘制嘴巴完成")

        # 绘制左耳，从上往下画
        canvas, drawn_points = draw_region(canvas, left_ear, drawn_points, 'left_ear', points_per_frame_face, edges,
                                           'down')
        print("绘制左耳完成")

        # 绘制右耳，从上往下画
        canvas, drawn_points = draw_region(canvas, right_ear, drawn_points, 'right_ear', points_per_frame_face, edges,
                                           'down')
        print("绘制右耳完成")

        # 绘制面部轮廓
        canvas, drawn_points = draw_region(canvas, jaw, drawn_points, 'jaw', points_per_frame_face, edges, 'down')
        print("绘制面部轮廓完成")

    # 使用剩余的点绘制面部框外扩散区域
    np.random.shuffle(remaining_points)  # Shuffle to randomize order of drawing

    # 使用扩散算法绘制面部框外区域
    radius = 0
    while len(remaining_points) > 0:
        points_to_draw = []
        for point in remaining_points:
            y, x = point
            if any([abs(y - jaw_point[1]) <= radius and abs(x - jaw_point[0]) <= radius for jaw_point in jaw]):
                if (y, x) not in drawn_points:
                    points_to_draw.append(point)

        # 逐点绘制
        frame_points = min(len(points_to_draw), points_per_frame_non_face)
        for i in range(frame_points):
            point = points_to_draw[i]
            y, x = point
            if (y, x) not in drawn_points:
                canvas[y, x] = [sketch_image[y, x]] * 3
                drawn_points.add((y, x))
        video_writer.write(canvas)
        radius += 1
        remaining_points = [point for point in remaining_points if (point[0], point[1]) not in drawn_points]
        print(f"绘制背景区域，半径：{radius}")
    print("绘制背景区域完成")


# 上色逻辑
def color_regions(canvas, face_landmarks, original_image, edges, coloring_ratio, points_per_frame_face,
                  points_per_frame_non_face, coloring_speed_factor):
    print("开始上色...")

    # 分离面部区域和非面部区域的点
    face_points = []
    non_face_points = []
    for landmarks in face_landmarks:
        jaw = landmarks[0:17]
        jaw_poly = np.array(jaw, np.int32)
        cv2.fillConvexPoly(edges, jaw_poly, 0)

    face_mask = np.zeros_like(edges)
    non_face_mask = np.ones_like(edges) * 255
    for landmarks in face_landmarks:
        jaw = landmarks[0:17]
        jaw_poly = np.array(jaw, np.int32)
        cv2.fillConvexPoly(face_mask, jaw_poly, 255)
        cv2.fillConvexPoly(non_face_mask, jaw_poly, 0)

    # 获取面部区域的非边缘点
    face_points = np.column_stack(np.where((edges == 0) & (face_mask == 255)))
    np.random.shuffle(face_points)  # Shuffle to randomize order of coloring

    # 获取非面部区域的非边缘点
    non_face_points = np.column_stack(np.where((edges == 0) & (non_face_mask == 255)))
    np.random.shuffle(non_face_points)  # Shuffle to randomize order of coloring

    # 对面部区域上色
    num_points_to_color_face = int(len(face_points) * coloring_ratio)
    points_to_color_face = face_points[:num_points_to_color_face]

    # 每次上色的速度加快
    points_per_frame_color_face = points_per_frame_face * coloring_speed_factor

    # 上色
    points_colored_face = 0
    total_points_face = len(points_to_color_face)
    while points_colored_face < len(points_to_color_face):
        frame_points = min(points_per_frame_color_face, len(points_to_color_face) - points_colored_face)
        for i in range(frame_points):
            point = points_to_color_face[points_colored_face + i]
            y, x = point
            canvas[y, x] = original_image[y, x]
        video_writer.write(canvas)
        points_colored_face += frame_points
        progress = (points_colored_face / total_points_face) * 100
        print(f"面部区域上色进度: {progress:.2f}% ({points_colored_face}/{total_points_face})")

    # 对非面部区域上色
    num_points_to_color_non_face = int(len(non_face_points) * coloring_ratio)
    points_to_color_non_face = non_face_points[:num_points_to_color_non_face]

    # 每次上色的速度加快
    points_per_frame_color_non_face = points_per_frame_non_face * coloring_speed_factor

    # 上色
    points_colored_non_face = 0
    total_points_non_face = len(points_to_color_non_face)
    while points_colored_non_face < len(points_to_color_non_face):
        frame_points = min(points_per_frame_color_non_face, len(points_to_color_non_face) - points_colored_non_face)
        for i in range(frame_points):
            point = points_to_color_non_face[points_colored_non_face + i]
            y, x = point
            canvas[y, x] = original_image[y, x]
        video_writer.write(canvas)
        points_colored_non_face += frame_points
        progress = (points_colored_non_face / total_points_non_face) * 100
        print(f"非面部区域上色进度: {progress:.2f}% ({points_colored_non_face}/{total_points_non_face})")

    print("上色完成")


# 辅助函数：绘制特定区域
def draw_region(canvas, region_points, drawn_points, region_name, points_per_frame, edges, direction=None):
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
    while points_drawn < len(region_edge_points):
        frame_points = min(points_per_frame, len(region_edge_points) - points_drawn)
        for i in range(frame_points):
            point = region_edge_points[points_drawn + i]
            y, x = point
            if (y, x) not in drawn_points:
                canvas[y, x] = [sketch_image[y, x]] * 3
                drawn_points.add((y, x))
        video_writer.write(canvas)
        points_drawn += frame_points
        progress = (points_drawn / total_points) * 100
        print(f"{region_name} 绘制进度: {progress:.2f}% ({points_drawn}/{total_points})")

    return canvas, drawn_points


# 主程序
if __name__ == "__main__":
    # 1. 绘制轮廓
    remaining_points = draw_contour(canvas, edges, contour_ratio, points_per_frame_face)

    # 2. 绘制详细部分
    draw_detailed(canvas, edges, face_landmarks, remaining_points, drawing_ratio, points_per_frame_face,
                  points_per_frame_non_face)

    # 3. 上色
    color_regions(canvas, face_landmarks, original_image, edges, coloring_ratio, points_per_frame_face,
                  points_per_frame_non_face, coloring_speed_factor)

    # 完成绘制
    video_writer.release()