import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import ffmpeg
import librosa
import numpy as np
import cv2
import random

st_names = "72司马取印.ts,64安居平五路.ts,69收姜维.ts,74诸葛妆神.ts,52夺占西川.ts,79吴宫干戈.ts"


video_info = {}
video_info["name_pre"]="三国演义"
video_info["jump"]=212
video_ext_infos = []
video_ext_info = {}
video_ext_info["name"]="72司马取印,64安居平五路,69收姜维,74诸葛妆神,52夺占西川,79吴宫干戈"
video_ext_info["ext_jump"]=164
video_ext_infos.append(video_ext_info)

video_ext_info2 = {}
video_ext_info2["name"]="01桃园三结义，07凤仪亭，43甘露寺，25刘备求贤，31智激周瑜，19古城相会，37横槊赋诗，55立嗣之争，73祁山斗智"
video_ext_info2["ext_jump"]=16
video_ext_infos.append(video_ext_info2)

video_info["ext"] = video_ext_infos
video_info_array = []
video_info_array.append(video_info)

video_info_new = {}
video_info_new["name_pre"]="新三国"
video_info_new["jump"]=0
video_ext_infos_new = []

video_ext_info_new = {}
video_ext_info_new["name"]="21"
video_ext_info_new["ext_jump"]=-151
video_ext_infos_new.append(video_ext_info_new)

video_info_new["ext"] = video_ext_infos_new
video_info_array.append(video_info_new)

def clip_video(source_file, target_file, start_time, stop_time):
    """
    利用moviepy进行视频剪切
    :param source_file: 原视频的路径，mp4格式
    :param target_file: 生成的目标视频路径，mp4格式
    :param start_time: 剪切的起始时间点（第start_time秒）
    :param stop_time: 剪切的结束时间点（第stop_time秒）
    :return:
    """
    validate_file(source_file)
    source_video = VideoFileClip(source_file)
    video = source_video.subclip(int(start_time), int(stop_time))  # 执行剪切操作
    video.write_videofile(target_file)  # 输出文件

def combine_no_voice(tree3_data, voice_path):
    target_file_temp = 'N:\\news\\novoice\\temp_'+ str(random.randint(1,1000)) + "_"+ str(random.randint(1,1000)) + ".avi"
    target_file = 'N:\\news\\novoice\\target_'+ str(random.randint(1,1000)) + "_"+ str(random.randint(1,1000)) + ".mp4"

    # 获取第一个视频文件
    video_info_0 = cv2.VideoCapture(tree3_data[0][3])
    # 获得视频的fps
    fps = video_info_0.get(cv2.CAP_PROP_FPS)
    # 定义输出视频
    size = (int(video_info_0.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_info_0.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter(target_file_temp,
                                   cv2.VideoWriter_fourcc(*'XVID'), int(fps), size)
    # 合成
    for video_info in tree3_data:
        source_file = video_info[3]
        video = cv2.VideoCapture(source_file)
        starttime = video_info[1]
        endtime = video_info[2]
        print(source_file, starttime, endtime)
        # 时 分 秒
        start_time = starttime.split(",")[0].split(":")
        print(start_time)
        stop_time = endtime.split(",")[0].split(":")
        print(stop_time)
        jump = 0
        video_file_name = source_file[source_file.rindex("\\") + 1: source_file.rindex(".")]
        for video_info in video_info_array:
            if (video_info["name_pre"] in source_file):
                for ext_info in video_info["ext"]:
                    if (video_file_name in ext_info["name"]):
                        jump = ext_info["ext_jump"]
                        break
                    else:
                        jump = video_info["jump"]
        start_time_s = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2]) + jump
        stop_time_s = int(stop_time[0]) * 3600 + int(stop_time[1]) * 60 + int(stop_time[2]) + jump
        start_time_mills = start_time_s * 1000 + int(starttime.split(",")[1])
        stop_time_mills = stop_time_s * 1000 + int(endtime.split(",")[1])

        # 定义起始时间
        start_frame = int(start_time_mills / 1000 * int(fps)) + 1
        end_frame = int(stop_time_mills / 1000 * int(fps)) + 1
        # 按帧输出视频
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        while (start_frame <= end_frame):
            print(start_frame)
            start_frame = start_frame + 1
            ret, frame = video.read()
            if (ret):
                # cv2.imwrite(path + '\\202221130'+str(i)+'.jpg',frame)
                frame = cv2.resize(frame, size)
                # print(frame)
                video_writer.write(frame)

    # 合成
    combine_video_audio(target_file_temp, voice_path, target_file, True)
    return target_file


def clip_video_mill(source_file, target_file, start_time, stop_time, audio):
    # 生成临时文件名称
    tmp_path = target_file[: target_file.rindex("\\") + 1]
    target_file_name = target_file[target_file.rindex("\\") + 1: target_file.rindex(".")]
    tmp_video = tmp_path + "v_" + target_file_name + ".avi"
    tmp_audio = tmp_path + "a_" + target_file_name + ".mp3"
    # 获取视频文件
    video = cv2.VideoCapture(source_file)
    # 获得视频的fps
    fps = video.get(cv2.CAP_PROP_FPS)
    # 定义起始时间
    start_frame = int(start_time / 1000 * int(fps)) + 1
    end_frame = int(stop_time / 1000 * int(fps)) + 1
    #定义输出视频
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter(tmp_video,
                                   cv2.VideoWriter_fourcc(*'XVID'), int(fps),
                                   size)
    # 按帧输出视频
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while (start_frame <= end_frame):
        start_frame = start_frame +1
        ret, frame = video.read()
        if (ret):
            # cv2.imwrite(path + '\\202221130'+str(i)+'.jpg',frame)
            frame = cv2.resize(frame, size)
            # print(frame)
            video_writer.write(frame)
    # 处理音频
    audio = audio[start_time: stop_time]
    audio.export(tmp_audio, format="mp3")

    # 合成
    combine_video_audio(tmp_video, tmp_audio, target_file, True)


def clip_audio_mill(source_file, target_file, start_time, stop_time):
    """
    利用pydub进行音频剪切。pydub支持源文件为 mp4格式，因此这里的输入可以与视频剪切源文件一致
    :param source_file: 原视频的路径，mp4格式
    :param target_file: 生成的目标视频路径，mp4格式
    :param start_time: 剪切的起始时间点（第start_time秒）
    :param stop_time: 剪切的结束时间点（第stop_time秒）
    :return:
    """
    validate_file(source_file)
    audio = AudioSegment.from_file(source_file, "mp4")
    audio = audio[start_time : stop_time ]
    audio_format = target_file[target_file.rindex(".") + 1:]
    audio.export(target_file, format=audio_format)


def combine_video_audio(video_file, audio_file, target_file, delete_tmp=False):
    """
    利用 ffmpeg将视频和音频进行合成
    :param video_file:
    :param audio_file:
    :param target_file:
    :param delete_tmp: 是否删除剪切过程生成的原视频/音频文件
    :return:
    """
    validate_file(video_file)
    validate_file(audio_file)
    # 注：需要先指定音频再指定视频，否则可能出现无声音的情况
    command = "ffmpeg -y -i {0} -i {1} -vcodec copy -acodec copy {2}".format(audio_file, video_file, target_file)
    os.system(command)


def clip_handle(source_file, target_file, start_time, stop_time, tmp_path=None, delete_tmp=False):
    """
    将一个视频文件按指定时间区间进行剪切
    :param source_file: 原视频文件
    :param target_file: 目标视频文件
    :param start_time: 剪切的起始时间点（第start_time秒）
    :param stop_time: 剪切的结束时间点（第stop_time秒）
    :param tmp_path: 剪切过程的文件存放位置
    :param delete_tmp: 是否删除剪切生成的文件
    :return:
    """
    # 设置临时文件名

    if tmp_path is None or not os.path.exists(tmp_path):
        # 如果没有指定临时文件路径，则默认与目标文件的位置相同
        tmp_path = target_file[: target_file.rindex("\\") + 1]
    target_file_name = target_file[target_file.rindex("\\") + 1: target_file.rindex(".")]
    tmp_video = tmp_path + "v_" + target_file_name + ".mp4"
    tmp_audio = tmp_path + "a_" + target_file_name + ".mp4"

    # 执行文件剪切及合成
    # clip_video(source_file, target_file, start_time, stop_time)
    clip_video_mill(source_file, target_file, start_time, stop_time)
    #clip_audio(source_file, tmp_audio, start_time, stop_time)
    #combine_video_audio(tmp_video, tmp_audio, target_file, delete_tmp)

def validate_file(source_file):
    if not os.path.exists(source_file):
        raise FileNotFoundError("没有找到该文件：" + source_file)
"""
0: 开始时间 +
1: 开始时间 -
3： 结束时间 +
4： 结束时间 -
"""
def resolve_time(time_mills, audio, type, source_file):
    # 如果是开始时间，先往后看看是否有人声
    start_time = 0
    stop_time = 0
    if (type == 0):
        start_time = time_mills
        stop_time = time_mills + 200
        if (ifVoice(audio, start_time, stop_time, source_file) == 0):
            return stop_time
        else:
            return resolve_time(start_time, audio, 1, source_file)
    if (type == 1):
        start_time = time_mills - 200
        stop_time = time_mills
        if (ifVoice(audio, start_time, stop_time, source_file) == 0):
            return stop_time
        else:
            return resolve_time(start_time, audio, 1, source_file)
    if (type == 2):
        start_time = time_mills
        stop_time = time_mills - 200
        if (ifVoice(audio, start_time, stop_time, source_file) == 0):
            return start_time
        else:
            return resolve_time(stop_time, audio, 3, source_file)
    if (type == 3):
        start_time = time_mills
        stop_time = time_mills + 200
        if (ifVoice(audio, start_time, stop_time, source_file) == 0):
            return start_time
        else:
            return resolve_time(stop_time, audio, 3, source_file)

def ifVoice(audio, start_time, stop_time, source_file):
    audio = audio[start_time : stop_time]
    tmp_path = source_file[: source_file.rindex("\\") + 1]
    tarfile = tmp_path +"c_"+ str(start_time) + "_" + str(stop_time) + ".mp3"
    audio.export(tarfile, format="mp3")
    y, sr = librosa.load(tarfile)
    energy = np.sum(np.abs(y) ** 2)
    threshold = 0.1
    print(str(energy))
    if energy > threshold:
        return 1
    else:
        return 0

def get_start_time(source_file, starttime):
    jump = 0
    video_file_name = source_file[source_file.rindex("\\") + 1: source_file.rindex(".")]
    for video_info in video_info_array:
        if (video_info["name_pre"] in source_file):
            for ext_info in video_info["ext"]:
                if (video_file_name in ext_info["name"]):
                    jump = ext_info["ext_jump"]
                    break
                else:
                    jump = video_info["jump"]
    print(jump)
    start_time = starttime.split(",")[0].split(":")
    start_time_s = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2]) + jump
    start_time_mills = start_time_s * 1000 + int(starttime.split(",")[1])
    return start_time_mills

def gettimeStr(source_file, time_mill):
    jump = 0
    video_file_name = source_file[source_file.rindex("\\") + 1: source_file.rindex(".")]
    for video_info in video_info_array:
        if (video_info["name_pre"] in source_file):
            for ext_info in video_info["ext"]:
                if (video_file_name in ext_info["name"]):
                    jump = ext_info["ext_jump"]
                    break
                else:
                    jump = video_info["jump"]
    millis = time_mill -  (jump * 1000)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    lay = millis - hours * 1000 * 60 * 60 - minutes * 1000 * 60 - seconds * 1000
    return ("%d:%d:%d,%d" % (hours, minutes, seconds,lay))


def getTimeSecond(startTimePa, endTimePa):
    timeDuration = getTimeMill(endTimePa) - getTimeMill(startTimePa);
    second = timeDuration / 1000;
    return str(second)

def getTimeMill(time):
    start_time = time.split(",")[0].split(":")
    start_time_s = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2])
    return start_time_s * 1000 + int(time.split(",")[1])

def getVideoTyoe(name):
    if ("三国演义" in name) :
        return "mp4"
    if ("西游记" in name) :
        return "mp4"
    if ("红楼梦" in name) :
        return "mp4"
    if ("水浒传" in name) :
        return "mp4"

def generateVideoFile(tree_selected):
    source_file = tree_selected[4]
    source_file = source_file.replace(".mkv", ".mp4")
    starttime = tree_selected[2]
    endtime = tree_selected[3]
    # 时 分 秒
    start_time = starttime.split(",")[0].split(":")
    print(start_time)
    stop_time = endtime.split(",")[0].split(":")
    print(stop_time)
    jump = 0
    video_file_name = source_file[source_file.rindex("\\") + 1: source_file.rindex(".")]
    for video_info in video_info_array:
        if (video_info["name_pre"] in source_file):
            for ext_info in video_info["ext"]:
                if (video_file_name in ext_info["name"]):
                    jump = ext_info["ext_jump"]
                    break
                else:
                    jump = video_info["jump"]
    start_time_s = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2]) + jump
    stop_time_s = int(stop_time[0]) * 3600 + int(stop_time[1]) * 60 + int(stop_time[2]) + jump

    # 处理主函数
    # clip_handle(source_file, target_file, start_time_s, stop_time_s, "N:\\三国演义\\tmp\\")
    start_time_mills = start_time_s * 1000 + int(starttime.split(",")[1])
    stop_time_mills = stop_time_s * 1000 + int(endtime.split(",")[1])
    if (stop_time_mills - start_time_mills < 3000):
        stop_time_mills =  start_time_mills + 3000
    audio = AudioSegment.from_file(source_file, getVideoTyoe(source_file))
    #start_time_mills = resolve_time(start_time_mills, audio, 0, source_file)
    #stop_time_mills = resolve_time(stop_time_mills, audio, 2, source_file)

    # 设置目标文件名
    root_path = source_file.split(source_file.split("\\")[-1])[0];
    print(root_path)
    target_name = str(start_time_mills) + "_" + str(stop_time_mills)
    target_file = root_path + "c_" + target_name + ".mp4"
    print(target_file)

    clip_video_mill(source_file, target_file, start_time_mills, stop_time_mills, audio)
    return target_file

def get_lens(path):
    clip = VideoFileClip(path)
    # 计算视频的时长，单位为分钟
    len = round(clip.duration / 60, 0)
    clip.close()
    print("总时长:",len)

if __name__ == "__main__":
    source_file = "G:\workspace\language_tools\src\output.mp4";
    starttime = '00:42:06,900'
    endtime = '00:42:09,900'
    # # 时 分 秒
    # start_time = starttime.split(",")[0].split(":")
    # print(start_time)
    # stop_time = endtime.split(",")[0].split(":")
    # print(stop_time)
    # start_time_s = int(start_time[0]) * 3600 + int(start_time[1]) * 60 + int(start_time[2])
    # stop_time_s = int(stop_time[0]) * 3600 + int(stop_time[1]) * 60 + int(stop_time[2])
    # # 设置目标文件名
    # root_path = source_file.split(source_file.split("\\")[-1])[0]+"\\target";
    # print(root_path)
    # target_name = str(start_time_s) + "_" + str(stop_time_s)
    # target_file = root_path + "c_" + target_name + ".mp4"
    # print(target_file)
    # # 处理主函数
    # clip_handle(source_file, target_file, start_time_s, stop_time_s, "N:\\三国演义\\tmp\\")
    get_lens(source_file)

