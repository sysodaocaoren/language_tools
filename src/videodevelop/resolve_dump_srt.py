import pysrt
from chagpt import chat_gpt_utils

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
    return srt_text

if __name__ == "__main__":
    path = "_translate/Run (2020) Movie Explained in Hindi⧸Urdu Story Summarized हिन्दी [W4QmDg517tk].en.srt"
    print(chat_gpt_utils.question("以下是一个电影解说的台词，但是语句不是很通顺，你是一个有名的电影解说，请帮我翻译成中文，并且整理一下：" + resolve(path)))