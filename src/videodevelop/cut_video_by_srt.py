# 解析srt文件，间隔5秒钟没有解说的声音，就将此片段裁剪出来
import pysrt
from moviepy.video.io.VideoFileClip import VideoFileClip

def split(path, name):
    video_path = path + "/" + name + ".mp4"
    srt_path = path + "/" + name + ".srt"
    des_path = path + "/temp/"
    # 解析srt文件
    subtitles = pysrt.open(srt_path, encoding='GBK')
    endTime = 0
    startTime = 0
    num = 0
    for srtSig in subtitles:
        if (endTime == 0):
            endTime = srtSig.end
            continue
        if (srtSig.start - endTime > 5):
            cutStart = startTime
            cutEnd = endTime
            # 分割视频
            cutVideo(video_path, cutStart, cutEnd, des_path + name + "_" + num + ".mp4")
            num = num + 1
            cutStart = cutEnd
            cutEnd = srtSig.start
            cutVideo(video_path, cutStart, cutEnd, des_path + name + "_" + num + ".mp4")
            num = num + 1
            startTime = srtSig.start
        else:
            endTime = srtSig.end

def cutVideo(video_path, start_time, end_time, target_path):
    source_video = VideoFileClip(video_path)
    video = source_video.subclip(int(start_time), int(end_time))  # 执行剪切操作
    video.write_videofile()


if __name__ == "__main__":
    print("come in")