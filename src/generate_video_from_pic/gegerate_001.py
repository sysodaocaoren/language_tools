import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip


def preprocess_image(image_path):
    # 加载图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 假设输入已经是素描图片，所以直接加载为灰度图
    return image


def detect_contours(image):
    # 由于已经是素描图片，可能不需要进行二值化或模糊处理，但可以尝试调整阈值
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # 使用OTSU算法自动计算阈值
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def simulate_hand_drawing(image, contours, steps_per_contour=10, line_thickness=1):
    height, width = image.shape
    # 创建一个与原始图像大小相同的白色背景图像用于绘制
    drawing = np.full((height, width, 3), 255, dtype=np.uint8)  # 白色背景
    frames = []
    current_frame = drawing.copy()  # 用于逐步绘制的当前帧

    for contour in contours:
        draw_contour(contour, current_frame, steps_per_contour, line_thickness)
        frames.append(current_frame.copy())  # 添加每一帧到列表中

    return frames


def draw_contour(contour, frame, steps_per_contour, line_thickness):
    contour_length = len(contour)
    contour_points = contour[:, 0, :].astype(np.int32)  # 转换为整数坐标
    for i in range(0, contour_length, steps_per_contour):
        for j in range(max(0, i - steps_per_contour), i + 1):
            if j < contour_length:
                cv2.line(frame, tuple(contour_points[j]), tuple(contour_points[(j + 1) % contour_length]), (0, 0, 0),
                         line_thickness)  # 使用黑色线条
                # 注意：这里使用了模运算来确保线条是闭合的（如果轮廓是闭合的）


def create_video(frames, output_path, fps=10):
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_path, codec='libx264')


if __name__ == "__main__":
    image_path = 'paoche.jpg'  # 替换为您的素描图片路径
    sketch_image = preprocess_image(image_path)
    contours = detect_contours(sketch_image)

    frames = simulate_hand_drawing(sketch_image, contours, steps_per_contour=17, line_thickness=1)  # 调整steps_per_contour以查看更多细节

    output_video_path = 'paoche.mp4'
    create_video(frames, output_video_path)

    print(f"Video saved to {output_video_path}")