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


# Step 2: 提取轮廓线条
def extract_contours(sketch_img):
    # 使用 Canny 边缘检测提取轮廓线
    edges = cv2.Canny(sketch_img, threshold1=50, threshold2=150)

    # 找到轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


# Step 3: 逐步模拟绘制轮廓线（逐线段画线）
def draw_contours_step_by_step(sketch_img, contours, video_output_path, fps=30):
    height, width = sketch_img.shape

    # 创建一个空白的白色画布，模拟画布的蒙版
    canvas = np.ones_like(sketch_img, dtype=np.uint8) * 255

    # 创建视频输出
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (width, height), False)

    # 逐条线段绘制轮廓
    for contour in contours:
        for i in range(1, len(contour)):
            # 绘制当前轮廓的线段
            pt1 = tuple(contour[i - 1][0])
            pt2 = tuple(contour[i][0])
            cv2.line(canvas, pt1, pt2, (0), 1)  # 绘制黑色的线条，1为线条宽度

            # 写入当前帧到视频
            out.write(canvas)

            # 显示当前进度（可以注释掉以提升性能）
            # cv2.imshow('Drawing Progress', canvas)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    # 释放视频资源
    out.release()
    # cv2.destroyAllWindows()


# Step 4: 人脸检测及五官区域分割
def detect_face_and_features(image_path):
    # 读取彩色图像
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 加载OpenCV的人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    return faces, gray


# Step 5: 按区域分步绘制轮廓、五官和细节
def draw_in_steps(image_path, video_output_path, fps=30):
    # 将图像转化为素描效果
    sketch_img = image_to_sketch(image_path)

    # 提取人脸及五官区域
    faces, gray_img = detect_face_and_features(image_path)

    # 提取整体轮廓
    contours = extract_contours(sketch_img)

    height, width = sketch_img.shape
    canvas = np.ones_like(sketch_img, dtype=np.uint8) * 255  # 创建空白画布

    # 创建视频输出
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (width, height), False)

    # Step 1: 绘制轮廓
    for contour in contours:
        for i in range(1, len(contour)):
            pt1 = tuple(contour[i - 1][0])
            pt2 = tuple(contour[i][0])
            cv2.line(canvas, pt1, pt2, (0), 1)
            out.write(canvas)
            # cv2.imshow('Drawing Progress', canvas)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    # Step 2: 绘制五官（基于人脸检测的区域）
    for (x, y, w, h) in faces:
        roi_gray = gray_img[y:y + h, x:x + w]
        roi_canvas = canvas[y:y + h, x:x + w]

        # 使用 Canny 边缘检测五官
        edges = cv2.Canny(roi_gray, threshold1=50, threshold2=150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # 绘制五官轮廓
        for contour in contours:
            for i in range(1, len(contour)):
                pt1 = tuple(contour[i - 1][0] + np.array([x, y]))  # 相对坐标转换为绝对坐标
                pt2 = tuple(contour[i][0] + np.array([x, y]))
                cv2.line(canvas, pt1, pt2, (0), 1)
                out.write(canvas)
                # cv2.imshow('Drawing Progress', canvas)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

    # Step 3: 绘制周边细节
    # 可以根据图片的其他区域自行分割处理，这里作为一个简化部分

    out.release()
    # cv2.destroyAllWindows()


# 主程序入口
if __name__ == "__main__":
    # 输入图像路径
    image_path = 'nverguo.jpg'  # 替换为你的图像路径
    video_output_path = 'sketch_drawing_process_detailed.mp4'  # 输出视频路径

    # 生成逐步模拟绘制素描的效果
    draw_in_steps(image_path, video_output_path)
