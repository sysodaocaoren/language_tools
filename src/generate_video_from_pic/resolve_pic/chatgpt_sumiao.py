import cv2
import numpy as np

# 读取图片
image = cv2.imread('nverguo.jpg')

# 转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 反转灰度图像
inverted_image = cv2.bitwise_not(gray_image)

# 减小模糊核的大小，减少模糊 (模糊核从21降为5)
blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)

# 反转模糊图像
inverted_blurred = cv2.bitwise_not(blurred)

# 生成素描图像
sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

# 增强对比度和细节
alpha = 1.0  # 对比度控制 (较高的对比度)
beta = 0     # 保持原始亮度
sketch = cv2.convertScaleAbs(sketch, alpha=alpha, beta=beta)

# 使用自适应直方图均衡化 (CLAHE) 增强图像对比度
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(12,12))
sketch = clahe.apply(sketch)

# 保存生成的素描图像
cv2.imwrite('clear_sketch_image.jpg', sketch)

