import cv2
import numpy as np

# 读取图片
image_path = 'paoche.jpg'  # 替换为你的素描图片路径
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 获取图片的尺寸
height, width = img.shape

# 创建一个空白画布
canvas = np.ones((height, width), dtype=np.uint8) * 255  # 创建白色画布

# 创建视频输出
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
fps = 10  # 帧率，可以根据需求调整
out = cv2.VideoWriter('drawing_process_line_by_line.mp4', fourcc, fps, (width, height), False)

# 使用 Canny 边缘检测提取图像的边缘
edges = cv2.Canny(img, threshold1=50, threshold2=150)

# 找到轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 绘制轮廓的顺序
for contour in contours:
    for i in range(1, len(contour)):
        # 绘制当前轮廓的线段
        pt1 = tuple(contour[i - 1][0])
        pt2 = tuple(contour[i][0])
        cv2.line(canvas, pt1, pt2, (0), 1)  # 绘制黑色的线条，1为线条宽度

        # 写入当前帧到视频
        out.write(canvas)

        # 显示当前进度（可以注释掉以提升性能）
        # cv2.imshow('Drawing', canvas)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

# 释放视频资源
out.release()
# cv2.destroyAllWindows()
