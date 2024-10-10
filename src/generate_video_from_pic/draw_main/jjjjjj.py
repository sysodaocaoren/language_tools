import cv2
import dlib
import numpy as np

# 初始化人脸检测器和特征点检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 读取原始图像
original_image = cv2.imread('nverguo_ehance.jpg')

# 降低图像分辨率加快处理速度
scale_factor = 0.5  # 缩放因子
resized_image = cv2.resize(original_image, (0, 0), fx=scale_factor, fy=scale_factor)

# 灰度处理原始图像
gray_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# 检测人脸
faces = detector(gray_resized)

# 如果没有检测到人脸，输出警告
if len(faces) == 0:
    print("没有检测到人脸")
else:
    for face in faces:
        # 映射回原始图像中的坐标
        (x, y, w, h) = (int(face.left() / scale_factor), int(face.top() / scale_factor),
                        int(face.width() / scale_factor), int(face.height() / scale_factor))

        # 绘制人脸边框
        cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 获取并绘制面部关键点
        landmarks = predictor(gray_resized, face)
        for n in range(0, 68):
            x_point = int(landmarks.part(n).x / scale_factor)
            y_point = int(landmarks.part(n).y / scale_factor)
            cv2.circle(original_image, (x_point, y_point), 2, (0, 0, 255), -1)

    # 显示结果
    cv2.imshow("Face and Landmarks", original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存标注结果
    cv2.imwrite('detected_faces_with_landmarks.jpg', original_image)
