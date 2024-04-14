
import pysrt

def srt_to_txt(srt_path, des_txtx_path):
    subtitles = pysrt.open(srt_path)
    txt_len = 0
    txt_num = 0;
    for subtitle in subtitles:
        if (txt_len > 1000):
            txt_num = txt_num + 1
            txt_len = 0
        with open(des_txtx_path+'_'+str(txt_num)+".txt", 'a') as fa:  # 写入txt文本文件中
            txt_len = txt_len + len(subtitle.text)
            fa.write(subtitle.text)
            fa.write('\n')

if __name__ == "__main__":
    path = 'N:\\video_develop\\4月12日\\'
    name = '4月12日'
    srt_to_txt(path + name + '.srt', path + name)