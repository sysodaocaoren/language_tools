import pysrt

subtitles = pysrt.open('testdushiniang.srt')
for subtitle in subtitles:
    print(subtitle.text)