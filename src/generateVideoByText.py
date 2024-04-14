from moviepy.editor import *
import os
import pyttsx3
import random
import librosa
import cv2
import edge_tts
import asyncio

from pydub import AudioSegment
import numpy as np

from aip import AipSpeech
from PIL import Image

IMAGEMAGICK_BINARY = r"G:\\software\\imageMagick\\ImageMagick-7.0.9-Q16-HDRI\\magick.exe"

# 定义生成视频的函数
def generate_video(text, bgm_path, output_path):
    bgm_clip = AudioFileClip(bgm_path)
    # 设置视频参数
    fps = 30
    duration = bgm_clip.duration
    print(duration)
    width = 1280
    height = 720

    # 创建视频帧
    clips = []
    print_text = ''
    for i in range(int(fps * duration)):
        # print_text = text[: int((i*4/fps)+1)]
        print_text = text
        print(print_text)
        txt_clip = (TextClip(print_text, font='xk_font.TTF', fontsize=110, color='yellow')
                    .set_position(('center', 'center'))
                    .set_duration(1 / fps)
                    .set_start(i / fps))
        clips.append(txt_clip)

    # 合成视频
    final_clip = CompositeVideoClip(clips, size=(width, height))

    # 添加背景音乐

    # bgm_duration = final_clip.duration
    # bgm_clip = bgm_clip.set_duration(bgm_duration)
    final_clip = final_clip.set_audio(bgm_clip)

    # 保存视频文件
    final_clip.write_videofile(output_path, fps=fps, codec='libx264')
    # 删除音频
    os.remove(bgm_path)

text_align = {"1":"0.3", "2":"0.3", "3":"0.35", "4":"0.2", "5":"0.2","6":"0.15","7":"0.1"}
text_fount = {"1":"100","2":"100","3":"100","4":"100", "5":"90","6":"90","7":"80"}
# 定义生成视频的函数
def generate_video2(text, bgm_path, output_path):
    bgm_clip = AudioFileClip(bgm_path)
    # 设置视频参数
    fps = 30
    duration = bgm_clip.duration
    print(duration)
    width = 1280
    height = 720

    # 首先根据图片生成视频
    image_path = "D:\\pandian\\pic\\xiaonvhai.jpg"
    # 统一图片大小
    resize_image(image_path, (width, height))
    # 根据图片生成视频
    bg_video = "N:\\picture\\temp_001.mp4"
    generateVideoByImage(image_path, bg_video, fps, duration)
    # 创建视频帧
    clips = []
    bg_video_clip = VideoFileClip(bg_video)
    clips.append(bg_video_clip)
    print_text = ''
    position_height = float(text_align.get(str(len(text))))
    for i in range(int(fps * duration)):
        print_text = text
        print(print_text)
        txt_clip = (TextClip(print_text, font='xk_font.TTF', fontsize=90, color='yellow')
                    .set_position((position_height, 0.4), True)
                    .set_duration(1 / fps)
                    .set_start(i / fps))
        clips.append(txt_clip)

    # 合成视频
    final_clip = CompositeVideoClip(clips, size=(width, height))
    # bgm_duration = final_clip.duration
    # bgm_clip = bgm_clip.set_duration(bgm_duration)
    final_clip = final_clip.set_audio(bgm_clip)

    # 保存视频文件
    final_clip.write_videofile(output_path, fps=fps, codec='libx264')
    # 删除音频
    os.remove(bgm_path)
    os.remove(bg_video)

def generateVideoByImage(image_path, outVideoPath, fps, duration):
    print(image_path)
    image = cv2.imread(image_path)  # 读取图片
    if image is None:
        print("none")
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # 设置视频编码器为MP4V
    video_writer = cv2.VideoWriter(outVideoPath, fourcc, fps, (image.shape[1], image.shape[0]))  # 创建视频写入对象
    i = 0
    while i < (fps * duration):
        video_writer.write(image)  # 将图片写入视频
        i = i + 1
    video_writer.release()  # 释放资源

# 图片处理
def resize_image(target_image_path, target_size):
    """
    调整图片大小，缺失的部分用黑色填充
    :param target_image_path: 图片路径
    :param target_size: 分辨率大小
    :return:
    """
    image = Image.open(target_image_path)

    iw, ih = image.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    scale = min(w / iw, h / ih)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()

    new_image = Image.new('RGB', target_size, (0, 0, 0, 0))  # 生成黑色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
    # new_image.show()

    # 覆盖原图片
    new_image.save(target_image_path)


def generateMap3(local, text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice)
    # 获取所有可用的声音列表
    voices = engine.getProperty('voices')
    # 选择一个指定语音(粤语语音sinji)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.2)
    engine.say(text)
    mp3_path = local + "audio_pyttsx3"+ str(random.randint(1,1000)) + "_"+ str(random.randint(1,1000)) +".mp3"
    engine.save_to_file(text, mp3_path)
    engine.runAndWait()
    return mp3_path

async def generateMap3_new(local, text):
    voice = 'zh-CN-YunxiNeural'
    mp3_path = local + "audio_edge_tts_" + str(random.randint(1, 1000)) + "_" + str(random.randint(1, 1000)) + ".mp3"
    rate = '-4%'
    volume = '+0%'

    tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    await tts.save(mp3_path)
    return mp3_path


APP_ID = "41555004"
API_KEY = "sMy9iQVd18RmGWKOblbRk6Nh"
SECRET_KEY = "filX3AEBir8Kmk6flu5RjaImCuSwu97Z "
def generateMp3_baidu(local, text, per = 5003, spd = 7, pit = 5):
    bd_parameter = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    #result = bd_parameter.synthesis(text, 'zh', 1, {'vol': 9, 'per': 5118, 'spd': 8, pit: '3'})
    result = bd_parameter.synthesis(text, 'zh', 1, {'vol': 9, 'per': int(per), 'pit': int(pit), 'spd': int(spd)})
    """
    lan	必填	固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
    spd	选填	语速，取值0-15，默认为5中语速
    pit	选填	音调，取值0-15，默认为5中语调
    vol	选填	音量，取值0-15，默认为5中音量
    per	选填	度逍遥（精品）=5003，度小鹿=5118，度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5
    aue	选填	3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）; 注意aue=4或者6是语音识别要求的格式，
                但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
    """
    bgm_path = local + "\\001" + str(random.randint(1,100000)) + ".mp3"
    with open(bgm_path, 'wb') as f:
        # 存放路径
        f.write(result)
    return bgm_path

def change_voice(path, output_path):
    # 读取原始音频文件
    sound = AudioSegment.from_file(path, format='mp3')

    # 调整音调
    octaves = 1.5
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    new_sound.export(output_path, format='mp3')

def get_voice_by_text(text, per, sped, spit):
    local = 'N:\\result\\temp_mp3\\'
    return generateMp3_baidu(local, text, per, sped, spit)

# 测试生成视频的函数
def getVideo(text, type):
    output_path = "N:\\result\\temp_mp4\\output1"+ str(random.randint(1,1000)) + "_"+ str(random.randint(1,1000)) +".mp4"
    local = 'N:\\result\\temp_mp3\\'
    bgm_path = generateMp3_baidu(local, text)
    if (type == 1):
        generate_video(text, bgm_path, output_path)
    if (type == 2):
        generate_video2(text, bgm_path, output_path)
    return  output_path
