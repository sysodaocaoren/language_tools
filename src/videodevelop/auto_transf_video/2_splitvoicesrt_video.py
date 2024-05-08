
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
from moviepy.editor import VideoFileClip

def resolve_video_step2():
    path = trans_config.params["path_step1"]
    print("1_" + path)
    path_step2 = trans_config.params["path_step2"]
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            print("1_" + dir)
            exits_mp4_flag = False
            exits_vtt_flag = False
            exits_readme_flag = False
            mp4_name = ""
            vtt_name = ""
            readme_name = ""
            for root, dirs, files in os.walk(path + "//" + dir):
                for file in files:
                    print(file)
                    if file.lower().endswith("mp4"):
                        exits_mp4_flag = True
                        mp4_name = file
                    if file.lower().endswith("vtt"):
                        exits_vtt_flag = True
                        vtt_name = file
                    if file.lower().endswith("json"):
                        exits_readme_flag = True
                        readme_name = file
            print(str(exits_mp4_flag) + ":" + str(exits_vtt_flag) + ":" + str(exits_readme_flag) )
            # 判断文件是否齐全
            if (not exits_mp4_flag or not exits_vtt_flag or not exits_readme_flag):
                continue
            # 判断是否执行过第二部
            readme_file = path + "//" + dir + "//" + dir +"_readme.json"
            data = trans_utils.get_from_json(readme_file)
            if (data["step"] == "resolve_step2"):
                print("alread step2:" + data["step"])
                continue
            # 看一下目标文件有该文件夹, 删掉
            if os.path.exists(path_step2 + dir):
                shutil.rmtree(path_step2 + dir)
            # 将MP4和vtt copy到目标文件夹
            os.mkdir(path_step2 + dir)
            shutil.copy2(path + dir + "\\" +  mp4_name, path_step2 + dir + "\\" + mp4_name)
            shutil.copy2(path + dir + "\\" + vtt_name, path_step2 + dir + "\\" + vtt_name)
            shutil.copy2(path + dir + "\\" + readme_name, path_step2 + dir + "\\" + readme_name)
            # 将vtt转换为srt
            vtt2srt.covert(path_step2 + dir)
            print("success convert srt:" + dir)
            # 去除音频
            video_clip = VideoFileClip(path_step2 + dir + "\\" + mp4_name)
            video_clip_without_audio = video_clip.set_audio(None)
            video_clip_without_audio.write_videofile(path_step2 +  dir + "\\" + "no_audio_" + mp4_name)
            video_clip_without_audio.close()
            video_clip.close()
            print("success  crash audio:" + dir)
            # 保存readme
            file_name = path_step2 + dir + "\\" + readme_name
            trans_utils.update_json_key(file_name, "step", "resolve_step2")
            trans_utils.update_json_key(file_name, "origin_file_name", mp4_name)
            # 删掉之前的MP4和vtt
            os.remove(path_step2 + dir + "\\" + mp4_name)
            os.remove(path_step2 + dir + "\\" + vtt_name)
            # 修改步骤一的step
            step1_file_name = path+ dir + "\\" + dir + "_readme.json"
            trans_utils.update_json_key(step1_file_name, "step", "resolve_step2")
            break
if __name__ == '__main__':
    resolve_video_step2()