import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip
import math


def preprocess_image(image_path):
    # 加载图像为灰度图
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image


def detect_contours(image):
    # 使用OTSU算法进行二值化
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 查找轮廓
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def interpolate_points(p1, p2, num_points=10):
    # 在两点之间生成num_points-1个等距点
    points = []
    for t in np.linspace(0, 1, num_points):
        x = int(p1[0] * (1 - t) + p2[0] * t)
        y = int(p1[1] * (1 - t) + p2[1] * t)
        points.append((x, y))
    return points


def simulate_hand_drawing(image, contours, steps_between_points=10, line_thickness=2):
    height, width = image.shape
    # 创建一个白色背景图像用于绘制
    drawing = np.full((height, width, 3), 255, dtype=np.uint8)
    frames = []
    current_frame = drawing.copy()

    for contour in contours:
        contour_points = contour[:, 0, :].astype(np.int32)
        num_points = len(contour_points)
        for i in range(num_points):
            p1 = contour_points[i]
            p2 = contour_points[(i + 1) % num_points]  # 确保轮廓是闭合的
            # 在p1和p2之间插值生成点，并逐帧绘制
            for j, point in enumerate(interpolate_points(p1, p2, steps_between_points + 1)):
                if j == 0:
                    # 如果是第一个点，直接绘制到当前帧
                    cv2.circle(current_frame, point, line_thickness // 2, (0, 0, 0), -1)  # 使用圆点来模拟画笔起始
                else:
                    # 绘制从上一个点到当前点的线段
                    prev_point = interpolate_points(p1, p2, j)[0]  # 注意这里要取j-1对应的点，但因为j从0开始，所以直接取j即可（因为上面循环已经生成了j-1的点）
                    # 但由于我们是从0开始绘制，所以实际上prev_point就是上一帧的最后一个点（除了第一个点）
                    # 为了简化，我们直接绘制到当前点，因为插值已经保证了平滑过渡
                    cv2.line(current_frame, prev_point, point, (0, 0, 0), line_thickness)
                    # 添加当前帧到列表中（这里为了演示效果，每插值一个点就添加一帧，实际上可以根据需要调整）
                # 注意：这样做会导致帧数非常多，视频可能很大或播放很慢
                # 为了优化，可以考虑合并相近的帧或使用其他方法减少帧数
                frames.append(current_frame.copy())

                # 由于最后一帧会是完整的轮廓，我们不需要再次添加它（因为上面的循环已经包含了）
        # 但为了确保完整性，可以在这里再次添加（实际上是多余的）
        # frames.append(current_frame.copy())

    # 注意：上面的代码会生成非常多的帧，因为每对轮廓点之间都插值了多个点，并且每个点都作为一帧
    # 为了优化，可以考虑以下策略之一：
    # 1. 增加steps_between_points的值，减少每对点之间的插值点数。
    # 2. 合并相近的帧，例如只保留每N帧中的一帧。
    # 3. 使用更高级的动画技术，如贝塞尔曲线或关键帧动画，来减少帧数同时保持平滑效果。

    # 这里为了演示，我们不做进一步优化，但请注意生成的视频可能会很大。

    return frames


def create_video(frames, output_path, fps=10):
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_path, codec='libx264')


if __name__ == "__main__":
    image_path = 'test-09.jpg'  # 替换为您的素描图片路径
    sketch_image = preprocess_image(image_path)
    contours = detect_contours(sketch_image)

    # 注意：下面的参数可能会生成一个非常大的视频文件，因为帧数非常多。
    # 您可以根据需要调整steps_between_points和fps的值来优化输出。
    frames = simulate_hand_drawing(sketch_image, contours, steps_between_points=18, line_thickness=1)

    output_video_path = 'test-09.mp4'
    create_video(frames, output_video_path)

    print(f"Video saved to {output_video_path}")