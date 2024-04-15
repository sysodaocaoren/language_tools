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

temp_video_path = ''
temp_srt_des_path = ''
temp_srt_file_name = str(datetime.date.today()) + ".srt"


def jiangying_export_srt():
    pyautogui.moveRel(-200, 200, duration=1)
    pass


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
    export_srt_from_video(video_full_path, srt_des_path, file_name)