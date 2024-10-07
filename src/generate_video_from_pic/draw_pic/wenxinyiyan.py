import cv2
import numpy as np
import random


# 加载原始图片并转换为灰度图
original_image = cv2.imread('nverguo.jpg', cv2.IMREAD_GRAYSCALE)
if original_image is None:
    raise FileNotFoundError("请确保提供了正确的图片路径。")

# 将图片转换为边缘图（使用Canny边缘检测）
edges = cv2.Canny(original_image, 100, 200)

# 查找边缘图的轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# 定义一个函数来生成手绘风格的线条（使用numpy数组优化）
def generate_sketch_line(start_point, end_point, noise_amplitude=5, num_points=100):
    t_values = np.linspace(0, 1, num_points)
    x_values = start_point[0] * (1 - t_values) + end_point[0] * t_values + np.random.uniform(-noise_amplitude,
                                                                                             noise_amplitude,
                                                                                             num_points)
    y_values = start_point[1] * (1 - t_values) + end_point[1] * t_values + np.random.uniform(-noise_amplitude,
                                                                                             noise_amplitude,
                                                                                             num_points)
    # 限制坐标在图像范围内
    height, width = original_image.shape
    x_values = np.clip(x_values, 0, width - 1).astype(np.int32)
    y_values = np.clip(y_values, 0, height - 1).astype(np.int32)
    line_points = np.stack((x_values, y_values), axis=-1)
    return line_points


# 创建一个白色的画布
canvas_size = original_image.shape
white_canvas = np.ones_like(original_image) * 255

# 定义一些参数
frame_rate = 30
video_length = 10  # 视频长度（秒）
output_video_path = 'sketch_drawing_video_optimized.avi'
num_lines_per_frame = 50  # 每帧的线条数量（减少以提升性能）
line_thickness = 2  # 固定的线条粗细（减少随机性以提升性能）

# 初始化视频写入器
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (canvas_size[1], canvas_size[0]))

if not isinstance(contours, list):
    contours = list(contours)

# 打乱轮廓顺序以增加随机性（只需在开始时做一次）
random.shuffle(contours)

# 主循环：逐帧绘制素描（使用numpy数组和减少随机性来提升性能）
for frame_idx in range(int(frame_rate * video_length)):
    # 创建一个当前帧的副本（使用numpy数组）
    frame = white_canvas.copy()

    # 随机选择轮廓并绘制线条（使用固定数量的线条和减少轮廓选择的随机性）
    for contour_idx, contour in enumerate(contours):
        if contour_idx >= num_lines_per_frame * frame_idx // int(frame_rate * video_length) * int(
                frame_rate * video_length / num_lines_per_frame):
            break

        # 将轮廓分割为线段（这里简化处理，直接选择轮廓上的两个随机点，但确保不超出轮廓长度）
        num_points = len(contour)
        if num_points > 1:
            start_idx = random.randint(0, num_points - 2)
            end_idx = (start_idx + random.randint(1, num_points - start_idx - 1)) % num_points
            start_point = contour[start_idx][0]
            end_point = contour[end_idx][0]
            # 调整坐标顺序以符合OpenCV的要求
            start_point = start_point[::-1]
            end_point = end_point[::-1]

            # 生成手绘风格的线条（使用numpy数组优化）
            line_points = generate_sketch_line(start_point, end_point)

            # 将线条绘制到帧上（使用OpenCV的polylines函数）
            cv2.polylines(frame, [line_points], isClosed=False, color=0, thickness=line_thickness)

    # 将当前帧（已经是修改后的）写入视频
    video_writer.write(frame)

# 释放视频写入器
video_writer.release()

print(f"Sketch drawing video saving process completed. Check the file at {output_video_path} for results.")
