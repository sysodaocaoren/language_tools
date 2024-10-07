import cv2 as cv2
import os

# 设置源文件夹和目标文件夹
source_folder = 'D:\\python\\before'
target_folder = 'D:\\python\later'
# 确保目标文件夹存在
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有文件
def resolve_image(image_path):
    image = cv2.imread(image_path)
    # 检查图片是否正确加载
    if image is None:
        print(f"Error: 当前图片加载失败 {image_path}")
    # cv2.imshow("old", image)
    # cv2.waitKey(0)
    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray_image)
    # cv2.waitKey(0)
    inverted_image = 255 - gray_image
    # cv2.imshow("inverted", inverted_image)
    # cv2.waitKey()
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blurred = 255 - blurred
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    # cv2.imshow("inverted_blurred", pencil_sketch)
    # cv2.waitKey(0)

    # cv2.imshow("original image", image)
    # cv2.imshow("pencil sketch", pencil_sketch)
    # 构造目标文件路径
    target_path = os.path.join(target_folder, 'later-002.jpg')
    # 保存素描到文件
    cv2.imwrite(target_path, pencil_sketch)

resolve_image("nverguo.jpg")
