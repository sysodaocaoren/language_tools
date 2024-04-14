import cv2
import numpy as np

video = cv2.VideoCapture("N:\\result\\result_696_482_835.mp4")


denoised_video = cv2.fastNlMeansDenoisingColored(video, None, 10, 10, 7, 21)


sharpened_video = cv2.filter2D(denoised_video, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


cv2.imwrite("N:\\result\\00000_output_video.mp4", sharpened_video)
