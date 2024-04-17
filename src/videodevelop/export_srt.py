# 1.首先新建两个临时文件，一个负责把源文件拷到这个文件夹下，剪映导入默认导这个文件夹下的
# 另一个负责srt文件的导出，默认导出srt文件到这个文件夹下
# 2. 如果要提取视频的srt，首先清空第一个文件夹，将视频文件copy到第一个文件夹下
# 3. python控制鼠标，选择该文件，然后提取字幕
# 4. 提取完成后，导入srt到第二个文件夹
# 5. 将导出的srt文件拷贝到目标文件，修改名称
import os
import shutil
import datetime
import pyautogui
import time

temp_video_path = ''
temp_srt_des_path = ''
temp_srt_file_name = str(datetime.date.today()) + ".srt"


def jiangying_export_srt():
    pyautogui.click(394, 1421,  button='left')
    pyautogui.click(500, 425,  button='left')
    pyautogui.doubleClick(259, 182,  button='left')
    pyautogui.moveTo(177,243, duration=1)
    pyautogui.click(224, 257,  button='left')
    pyautogui.click(149, 53,  button='left')
    pyautogui.click(194, 247,  button='left')
    wait_color_finish((151, 151, 153), 76, 1053)
    pyautogui.click(2423, 17, button='left')
    time.sleep(1)
    pyautogui.click(1330, 523, button='left')
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.click(1466, 1005, button='left')


def are_colors_equal(color1, color2, tolerance=0):
    # 将颜色转换为RGB整数值
    rgb1 = [int(round(c * 255)) if c <= 1 else int(c) for c in color1]
    rgb2 = [int(round(c * 255)) if c <= 1 else int(c) for c in color2]

    # 如果指定了容差，则允许在对比中有一定的误差
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(rgb1, rgb2))

def wait_color_finish(targetcolor, x, y):
    res = pyautogui.screenshot().getpixel((x, y))
    print(res)
    if (are_colors_equal(targetcolor, res, tolerance=10)):
        return
    else:
        time.sleep(1)
        wait_color_finish(targetcolor, x, y)


def del_video_by():
    pyautogui.click(394, 1421, button='left')
    pyautogui.click(37, 50, button='left')
    pyautogui.click(156, 216, button='left')
    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.click(1242, 777, button='left')

def export_srt_from_video(video_full_path, srt_des_path, file_name):
    file_full_name = file_name + ".mp4"
    file_full_path = video_full_path + "/" + file_full_name
    # 将视频拷贝到临时文件
    shutil.copy(file_full_path, temp_video_path + "/" + file_full_name)
    # 移动鼠标导出srt文件
    jiangying_export_srt()
    # 处理导出的srt文件
    srt_file_full_path = temp_srt_des_path + "/" + temp_srt_file_name
    shutil.copy(srt_file_full_path, video_full_path + "/" + temp_srt_file_name)
    os.rename(video_full_path + "/" + temp_srt_file_name, video_full_path + "/" + file_name + ".srt")



if __name__ == "__main__":
    video_full_path = ''
    srt_des_path = ''
    file_name = ''
    # export_srt_from_video(video_full_path, srt_des_path, file_name)
    jiangying_export_srt();
    # del_video_by()