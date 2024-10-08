import cv2
import numpy as np


# Step 1: 将原始图片转换为素描效果
def image_to_sketch(image_path):
    # 读取彩色图像
    img = cv2.imread(image_path)

    # 转换为灰度图像
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 反转灰度图像的颜色（负片效果）
    inverted_gray = 255 - gray_img

    # 使用高斯模糊
    blurred = cv2.GaussianBlur(inverted_gray, (21, 21), 0)

    # 反转模糊后的图像
    inverted_blurred = 255 - blurred

    # 得到最终的素描效果
    sketch = cv2.divide(gray_img, inverted_blurred, scale=256.0)

    return sketch


# Step 2: 逐步擦除蒙版以露出素描图像
def reveal_sketch(sketch_img, video_output_path, contours, faces, fps=30):
    height, width = sketch_img.shape
cd src
    # 创建一个全白的画布（蒙版）
    canvas = np.ones_like(sketch_img, dtype=np.uint8) * 255

    # 创建视频输出
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (width, height))

    # Step 1: 先擦除外部轮廓
    for contour in contours:
        for i in range(1, len(contour)):
            pt1 = tuple(contour[i - 1][0])
            pt2 = tuple(contour[i][0])
            # 确保从 sketch_img 中取到的值作为单一数值（灰度）
            color = int(sketch_img[pt1[1], pt1[0]])
            cv2.line(canvas, pt1, pt2, color, 1)
            # 将灰度图转换为三通道伪RGB
            rgb_canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
            out.write(rgb_canvas)  # 写入视频
            # cv2.imshow('Drawing Progress', rgb_canvas)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    # Step 2: 擦除五官部分（基于人脸检测区域）
    for (x, y, w, h) in faces:
        roi_canvas = canvas[y:y + h, x:x + w]
        roi_sketch = sketch_img[y:y + h, x:x + w]

        edges = cv2.Canny(roi_sketch, threshold1=50, threshold2=150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            for i in range(1, len(contour)):
                pt1 = tuple(contour[i - 1][0] + np.array([x, y]))
                pt2 = tuple(contour[i][0] + np.array([x, y]))
                color = int(sketch_img[pt1[1], pt1[0]])  # 从素描图中提取正确的颜色
                cv2.line(canvas, pt1, pt2, color, 1)
                rgb_canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
                out.write(rgb_canvas)
                # cv2.imshow('Drawing Progress', rgb_canvas)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

    # Step 3: 擦除剩余的周边细节
    edges = cv2.Canny(sketch_img, threshold1=50, threshold2=150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        for i in range(1, len(contour)):
            pt1 = tuple(contour[i - 1][0])
            pt2 = tuple(contour[i][0])
            color = int(sketch_img[pt1[1], pt1[0]])  # 转换为灰度值
            cv2.line(canvas, pt1, pt2, color, 1)
            rgb_canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
            out.write(rgb_canvas)
            # cv2.imshow('Drawing Progress', rgb_canvas)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    # 释放视频资源
    out.release()
    # cv2.destroyAllWindows()


# Step 3: 主函数，按照顺序擦除蒙版，展示素描效果
def draw_in_steps(image_path, video_output_path, fps=30):
    # 将图像转化为素描效果
    sketch_img = image_to_sketch(image_path)

    # 提取人脸及五官区域
    faces, gray_img = detect_face_and_features(image_path)

    # 提取整体轮廓
    contours = extract_contours(sketch_img)

    # 生成逐步模拟擦除蒙版的效果
    reveal_sketch(sketch_img, video_output_path, contours, faces, fps)


# Step 4: 人脸检测及五官区域分割
def detect_face_and_features(image_path):
    # 读取彩色图像
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 加载OpenCV的人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    return faces, gray


# Step 5: 提取轮廓线条
def extract_contours(sketch_img):
    # 使用 Canny 边缘检测提取轮廓线
    edges = cv2.Canny(sketch_img, threshold1=50, threshold2=150)

    # 找到轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


# 主程序入口
if __name__ == "__main__":
    # 输入图像路径
    image_path = 'nverguo.jpg'  # 替换为你的图像路径
    video_output_path = 'sketch_drawing_process_reveal.mp4'  # 输出视频路径

    # 生成逐步擦除蒙版，展示素描的效果
    draw_in_steps(image_path, video_output_path)
