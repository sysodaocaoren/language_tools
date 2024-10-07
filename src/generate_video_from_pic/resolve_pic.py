# 照片转字符画
# USAGE
# python img2zfh.py --image images/ym.jpg
# python img2zfh.py --image images/comic.jpg
import argparse

import cv2
import imutils

# 构建命令行参数及解析
# --image 要转字符画的图像
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, default="nverguo.jpg", help="path to input image to be ZFH'd")
args = vars(ap.parse_args())


def zcfg(src_image, dst_image):
    img_rgb = cv2.imread(src_image)
    # cv2.imshow("origin", imutils.resize(img_rgb, width=300))

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    # adaptiveThreshold()会在图片的每一个小的局部区域内进行二值化操作，因此对于一些清晰度比较高、色彩区分比较细腻的图片，就会出现上面这样密密麻麻的情况。
    img_edge = cv2.adaptiveThreshold(img_gray, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, blockSize=3, C=2)

    cv2.imwrite(dst_image, img_edge)

    # cv2.imshow("zcfg_dst", imutils.resize(img_edge, width=300))
    # cv2.waitKey(0)


def mhfg(src_image, dst_image):
    img_rgb = cv2.imread(src_image)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.medianBlur(img_gray, 5)  # 漫画风格

    # adaptiveThreshold()会在图片的每一个小的局部区域内进行二值化操作，因此对于一些清晰度比较高、色彩区分比较细腻的图片，就会出现上面这样密密麻麻的情况。
    img_edge = cv2.adaptiveThreshold(img_gray, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, blockSize=3, C=2)

    cv2.imwrite(dst_image, img_edge)

    # cv2.imshow("mhfg_dst", imutils.resize(img_edge, width=300))
    # cv2.waitKey(0)


def xsfg(src_image, dst_image):
    img_rgb = cv2.imread(src_image)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, ksize=(21, 21), sigmaX=0, sigmaY=0)  # 写实风格

    # cv2.divide()本质上进行的是两幅图像素级别的除法操作，其得到的结果可以简单理解为两幅图之间有明显差异的部分。
    img_edge = cv2.divide(img_gray, img_blur, scale=255)

    cv2.imwrite(dst_image, img_edge)

    # cv2.imshow("xsfg_dst", imutils.resize(img_edge, width=300))
    # cv2.waitKey(0)


src_image = 'nverguo.jpg'
# zcfg(src_image=src_image, dst_image=src_image.replace(".jpg", "_zc.jpg"))
# mhfg(src_image=src_image, dst_image=src_image.replace(".jpg", "_mh.jpg"))
xsfg(src_image=src_image, dst_image=src_image.replace(".jpg", "_xs.jpg"))
