
#
#此py作用
# 1. 是将视频进行音频视频的分离
# 2. 将vtt转换为srt
#

import os
import trans_utils
import trans_config
import shutil
import vtt2srt

def resolve_video_step2():
    path = trans_config.params["path_step1"]
    path_step2 = trans_config.params["path_step2"]
    for root, dirs, files in os.walk(path):
        for file in files:
            exits_mp4_flag = False
            exits_vtt_flag = False
            exits_readme_flag = False
            mp4_name = ""
            vtt_name = ""
            for root, dirs, files in os.walk(path + "//" + file):
                for file in files:
                    if file.lower().endswith("mp4"):
                        exits_mp4_flag = True
                        mp4_name = file
                    if file.lower().endswith("vtt"):
                        exits_vtt_flag = True
                        vtt_name = file
                    if file.lower().endswith("json"):
                        exits_readme_flag = True
            # 判断文件是否齐全
            if (not exits_mp4_flag or not exits_vtt_flag or not exits_readme_flag):
                continue
            # 判断是否执行过第二部
            readme_file = path + "//" + file + "//" + file +"_readme.json"
            data = trans_utils.get_from_json(readme_file)
            if (data["step"] == "resolve_step2"):
                continue
            # 看一下目标文件有该文件夹, 删掉
            if os.path.exists(path_step2 + file):
                shutil.rmtree(path_step2 + file)
            # 将MP4和vtt copy到目标文件夹
            os.mkdir(path_step2 + file)
            shutil.copy2(path + file + "\\" +  mp4_name, path_step2 + file + "\\" + mp4_name)
            shutil.copy2(path + file + "\\" + vtt_name, path_step2 + file + "\\" + vtt_name)
            # 将vtt转换为srt
            vtt2srt.covert(path_step2 + file)
            # 音频视频分离

if __name__ == '__main__':
    resolve_video_step2()