import pysrt

def resolve(srt_path):
    srt_text = ''
    srt_text_one = ''
    srt_text_second = ''
    srt_text_three = ''
    subtitles = pysrt.open(srt_path)
    for subtitle in subtitles:
        text = subtitle.text
        if (srt_text_one != '' and srt_text_one in text):
            continue
        if (srt_text_second != '' and srt_text_second in text):
            continue
        if (srt_text_three != '' and srt_text_three in text):
            continue
        srt_text = srt_text + "" + text
        srt_text_three = srt_text_second
        srt_text_second = srt_text_one
        srt_text_one = text
    print(srt_text)

if __name__ == "__main__":
    path = "D:\\计划\\test.srt"
    resolve(path)