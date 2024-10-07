import cv2
import numpy as np


def enhance_sketch_lines(image_path, output_path, contrast_factor=1.3, brightness_increase=10):
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"The image file at {image_path} was not found.")

        # 调整对比度

    def adjust_contrast(image, factor):
        # 转换为浮点型进行运算
        float_image = image.astype(np.float32)
        # 标准化到0-255范围并乘以对比度因子
        adjusted = cv2.convertScaleAbs(float_image, alpha=factor, beta=0)
        return adjusted

        # 调整亮度（增加固定值）

    def adjust_brightness(image, value):
        # 确保不溢出，先裁剪到0-255范围，然后加上亮度值
        clipped = np.clip(image, 0, 255 - value)
        brightened = np.clip(clipped + value, 0, 255).astype(np.uint8)
        return brightened

        # 先调整对比度，再调整亮度

    contrast_enhanced = adjust_contrast(image, contrast_factor)
    final_image = adjust_brightness(contrast_enhanced, brightness_increase)

    # 保存结果图像
    cv2.imwrite(output_path, final_image)
    print(f"Enhanced image saved to {output_path}")


def enhance_sketch_lines2(image_path, output_path, block_size=11, c_value=2):
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"The image file at {image_path} was not found.")

        # 应用自适应阈值化来增强线条
    # 参数解释：
    # - blockSize: 用来计算像素阈值的邻域大小（必须是奇数）
    # - C: 从平均或加权平均值中减去的常数，可以是正数或负数
    enhanced_image = cv2.adaptiveThreshold(
        image,
        255,  # 最大值
        cv2.ADAPTIVE_THRESH_MEAN_C,  # 使用平均阈值化
        cv2.THRESH_BINARY,  # 二值化类型
        blockSize=block_size,
        C=c_value
    )

    # 保存结果图像
    cv2.imwrite(output_path, enhanced_image)
    print(f"Enhanced image saved to {output_path}")

# 示例用法
input_image_path = 'nverguo_xs.jpg'  # 输入素描图像路径
output_image_path = 'nverguo_xs2.jpg'  # 输出图像路径
enhance_sketch_lines2(input_image_path, output_image_path)