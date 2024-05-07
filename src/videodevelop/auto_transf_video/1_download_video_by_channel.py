from pytube import Channel
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import os
from pytube import YouTube
import subprocess
import trans_utils
import trans_config

def list_videos(play_list_url):
    playlist = Playlist(play_list_url)
    path = trans_config.params["path_step1"]
    for url in playlist:
        try:
            video_id = url.split('v=')[-1]
            mkdir_flag = True
            exits_mp4_flag = False
            exits_vtt_flag = False
            exits_readme_flag = False
            language = ''
            if os.path.exists(path + video_id):
                mkdir_flag = False
                for root, dirs, files in os.walk(path + video_id):
                    for file in files:
                        if file.lower().endswith("mp4"):
                            exits_mp4_flag = True
                        if file.lower().endswith("vtt"):
                            exits_vtt_flag = True
                        if file.lower().endswith("json"):
                            exits_readme_flag = True
                # 如果该有的文件都有，就下一个
                print(str(mkdir_flag) + ":" + str(exits_mp4_flag)+ ":" + str(exits_vtt_flag)+ ":" + str(exits_readme_flag))
                if (not mkdir_flag and exits_mp4_flag and exits_vtt_flag and exits_readme_flag):
                    continue
            if mkdir_flag:
                os.mkdir(path + video_id)
            if not exits_mp4_flag:
                print("download:" + video_id + " start")
                download_video(url, path + video_id)
                print("download:" + video_id + " success")
            if not exits_vtt_flag:
                print("download vtt:" + video_id + "start")
                # 下载字幕
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                for x, tr in enumerate(transcript_list):
                    language = tr.language_code
                    if ("hi" == language):
                         break
                os.chdir(path + video_id)
                command = "yt-dlp --write-auto-subs --sub-format srt --sub-lang " + language +" --skip-download " + url
                subprocess.run(command)
                print("download vtt:" + video_id + " end")
            if not exits_readme_flag:
                file_name = path + video_id + "\\" +video_id + "_readme.json"
                data = {}
                data["language"] = language
                data["step"] = "download_vtt"
                trans_utils.save_to_json(data, file_name)
        except Exception as e:
            continue



def download_video(video_url, save_path):
    yt = YouTube(video_url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(save_path)

if __name__ == '__main__':
    list_videos("https://www.youtube.com/watch?v=QQpZetENa-s&list=PLkEp6SAg45PvwD9U4lB2EHEjAJyA9QL4c");