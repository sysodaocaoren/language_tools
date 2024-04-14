
import arrow
import time
from datetime import datetime, timedelta
import subprocess
import re
import datetime
import os
import torch
import accelerate
import whisper

from faster_whisper import WhisperModel

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def fast_model():
    model_size = "large-v2"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe("N:\\result\\result_797_902_722.mp4", beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

def extract_subtitles(video_file, output_file, actual_start_time=None):
    # 加载whisper模型
    model = whisper.load_model("large-v2")  # 根据需要选择合适的模型
    subtitles = []
    # 提取字幕
    result = model.transcribe(video_file)
    start_time = arrow.get(actual_start_time, 'HH:mm:ss.SSS') if actual_start_time is not None else arrow.get(0)

    for segment in result["segments"]:
        # 计算开始时间和结束时间
        start = format_time(start_time.shift(seconds=segment["start"]))
        end = format_time(start_time.shift(seconds=segment["end"]))
        # 构建字幕文本
        subtitle_text = f"【{start} -> {end}】: {segment['text']}"
        print(subtitle_text)
        subtitles.append(subtitle_text)
    # 将字幕文本写入到指定文件中
    with open(output_file, "w", encoding="utf-8") as f:
        for subtitle in subtitles:
            f.write(subtitle + "\n")

"""
从目标视频中提取字幕并生成到指定文件
参数:

video_file (str): 目标视频文件的路径
output_file (str): 输出文件的路径
actual_start_time (str): 音频的实际开始时间，格式为'时:分:秒.毫秒'（可选）
target_lang (str): 目标语言代码，例如'en'表示英语，'zh-CN'表示简体中文等（可选）
"""

def extract_subtitles_translate(video_file, output_file, actual_start_time=None, target_lang=None):
	# 指定whisper的路径
    whisper_path = r"G:\env\python-3.10\Scripts\whisper"
    subtitles = []
    # 构建命令行参数
    command = [whisper_path, video_file, "--task", "translate", "--language", target_lang, "--model", "large-v2"]

    if actual_start_time is not None:
        command.extend(["--start-time", actual_start_time])

    print(command)

    try:
        # 运行命令行命令并获取字节流输出
        with torch.no_grad():
            output = subprocess.check_output(command)
            print(output)
            output = output.decode('utf-8') # 解码为字符串
            subtitle_lines = output.split('\n')  # 按行分割字幕文本

        start_time = time_to_milliseconds(actual_start_time) if actual_start_time is not None else 0
        for line in subtitle_lines:
            line = line.strip()
            if line:  # 空行跳过
                # 解析每行字幕文本
                match = re.match(r'\[(\d{2}:\d{2}.\d{3})\s+-->\s+(\d{2}:\d{2}.\d{3})\]\s+(.+)', line)
                if match:
                    # 这是秒转时间
                    # start = seconds_to_time(start_time + time_to_seconds(match.group(1)))
                    # end = seconds_to_time(start_time + time_to_seconds(match.group(2)))
                    start = start_time + time_to_milliseconds(match.group(1))
                    end = start_time + time_to_milliseconds(match.group(2))
                    text = match.group(3)
                    # 构建字幕文本 自定义输出格式
                    subtitle_text = f"【{start} -> {end}】: {text}"
                    print(subtitle_text)
                    subtitles.append(subtitle_text)
        # 将字幕文本写入指定文件
        with open(output_file, "w", encoding="utf-8") as f:
            for subtitle in subtitles:
                f.write(subtitle + "\n")

    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")


def time_to_milliseconds(time_str):
    h, m, s = time_str.split(":")
    seconds = int(h) * 3600 + int(m) * 60 + float(s)
    return int(seconds * 1000)


def format_time(time):
    return time.format('HH:mm:ss.SSS')


def format_time_dot(time):
    return str(timedelta(seconds=time.total_seconds())).replace(".", ",")[:-3]


# 封装一个计算方法运行时间的函数
def time_it(func, *args, **kwargs):
    start_time = time.time()
    print("开始时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    result = func(*args, **kwargs)

    end_time = time.time()
    total_time = end_time - start_time

    minutes = total_time // 60
    seconds = total_time % 60

    print("结束时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
    print("总共执行时间: {} 分 {} 秒".format(minutes, seconds))

    return result

if __name__ == '__main__':
    # video_file = "N:\\result\\result_797_902_722.mp4"  # 替换为目标视频文件的路径
    # output_file = "N:\\result\\result_797_902_722.txt"  # 替换为输出txt文件的路径
    # actual_start_time = '00:00:00.000'  # 替换为实际的音频开始时间，格式为'时:分:秒.毫秒'，如果未提供则默认为00:00:00.000时刻
	# # 直接在main方法中调用
    # extract_subtitles(video_file, output_file, actual_start_time)
    # time_it(extract_subtitles_translate, video_file, output_file, None, 'Chinese')
    fast_model()