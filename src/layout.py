from tkinter import *
from tkinter import ttk
import tkinter as tk
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
import cutVideo
import os
from PIL import ImageTk, Image
import cv2
import pylab
import imageio
from ffpyplayer.player import MediaPlayer
from moviepy.editor import VideoFileClip,concatenate_videoclips
import datetime
import random
import generateVideoByText
import chengyu
import uuid
from ffmpy import FFmpeg
import pickle
import mysqlutils
import addwhoosh_new
import vlc
import datetime
import time
from pydub import AudioSegment

tree1_selected = []
tree2_selected = []
tree3_selected = []
tree4_selected = []
tree2_data = []
tree3_data = []
tree4_data = []
tree2_data_map = {}
tree2_data_order_array = []
play_start_time = 0
play_end_time = 0
play_set_flag=0

audio_path = ''
cache_file_dir = "N:\\result\\cache_file\\"

indexPath = {"三国演义": "t_video_sanguo","2010版三国演义": "t_video_sanguo_new", "水浒传": "t_video_shuihu", "西游记": "t_video_xiyou", "红楼梦": "t_video_honglou", "亮剑": "t_video_liangjian"}
##############  methods  ##############
# 模糊查询
def query ():
    for item in tree.get_children():
        tree.delete(item)
    content = ent1.get()
    if(content == ''):
       return
    # 下拉框
    indexPath={"三国演义":"N:\\三国演义\\indexdir"}
    ix = open_dir(indexPath.get(combobox.get()), indexname='article_index')
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(content)
        results = searcher.search_page(query, 1, 1000)
        for i, hit in enumerate(results):
            Data = [str(i), hit["content"], hit["starttime"], hit["endtime"], hit["path"]]
            tree.insert('', Data[0], text='', values=Data)

# 模糊查询
def querydb ():
    for item in tree.get_children():
        tree.delete(item)
    content = ent1.get()
    if(content == ''):
       return
    print(combobox.get())
    print(indexPath.get(combobox.get()))
    results = mysqlutils.query(content, indexPath.get(combobox.get()))
    count = 0
    for hit in results:
        Data = [str(count), hit[1], hit[2], hit[3], hit[4], hit[0]]
        tree.insert('', Data[0], text='', values=Data)
        count = count + 1

#模糊查询 搜成语
def querychengyu ():
    for item in tree.get_children():
        tree.delete(item)
    content = ent1.get()
    if(content == ''):
       return
    print(combobox.get())
    print(indexPath.get(combobox.get()))
    results = mysqlutils.query(content, indexPath.get(combobox.get()))
    count = 0
    for hit in results:
        Data = [str(count), hit[1], hit[2], hit[3], hit[4], hit[0]]
        tree.insert('', Data[0], text='', values=Data)
        count = count + 1

#模糊查询 搜成语
def queryyayun ():
    for item in tree.get_children():
        tree.delete(item)
    content = ent1.get()
    if(content == ''):
       return
    print(combobox.get())
    print(indexPath.get(combobox.get()))
    # results = mysqlutils.query(content, indexPath.get(combobox.get()))
    results = addwhoosh_new.getByPinyinEnd(indexPath.get(combobox.get()), content)
    count = 0
    for hit in results:
        Data = [str(count), hit[1], hit[2], hit[3], hit[4], hit[0]]
        tree.insert('', Data[0], text='', values=Data)
        count = count + 1

#模糊查询 搜成语
def queryjielong ():
    for item in tree.get_children():
        tree.delete(item)
    content = ent1.get()
    if(content == ''):
       return
    print(combobox.get())
    print(indexPath.get(combobox.get()))
    chengyuresults = chengyu.get_chengyu_list(content)
    print(str(chengyuresults))
    for result in chengyuresults:
        # results = mysqlutils.query(content, indexPath.get(combobox.get()))
        results = mysqlutils.query(result, indexPath.get(combobox.get()))
        count = 0
        for hit in results:
            Data = [str(count), hit[1], hit[2], hit[3], hit[4], hit[0]]
            tree.insert('', Data[0], text='', values=Data)
            count = count + 1

# 表格编辑行
def edit_row(event):
    # 获取被点击的行号
    row = tree.identify_row(event.y)

    # 获取行的各个列
    columns = [tree.set(row, column) for column in tree["columns"]]

    # 创建编辑窗口
    window = tk.Toplevel(root)

    # 创建编辑窗口的标题
    window.title("编辑行")

    # 创建编辑窗口的输入框和标签
    entries = []
    for i, (column, value) in enumerate(zip(tree["columns"], columns)):
        label = tk.Label(window, text=column)
        label.grid(row=i, column=0, sticky="e")

        entry = tk.Entry(window)
        entry.insert(0, value)
        entry.grid(row=i, column=1, sticky="w")

        entries.append(entry)

    # 创建确认按钮
    def apply_edit():
        new_values = [entry.get() for entry in entries]
        tree.item(row, values=new_values)
        window.destroy()

    confirm_button = tk.Button(window, text="确认", command=apply_edit)
    confirm_button.grid(row=len(tree["columns"]), column=0, columnspan=2)

# 表格编辑行
def edit_row2(event):
    # 获取被点击的行号
    row = tree2.identify_row(event.y)

    # 获取行的各个列
    columns = [tree2.set(row, column) for column in tree2["columns"]]

    # 创建编辑窗口
    window = tk.Toplevel(root)

    # 创建编辑窗口的标题
    window.title("编辑行")

    # 创建编辑窗口的输入框和标签
    entries = []
    for i, (column, value) in enumerate(zip(tree2["columns"], columns)):
        label = tk.Label(window, text=column)
        label.grid(row=i, column=0, sticky="e")

        entry = tk.Entry(window)
        entry.insert(0, value)
        entry.grid(row=i, column=1, sticky="w")

        entries.append(entry)

    # 创建确认按钮
    def apply_edit():
        new_values = [entry.get() for entry in entries]
        tree2.item(row, values=new_values)
        window.destroy()

    confirm_button = tk.Button(window, text="确认", command=apply_edit)
    confirm_button.grid(row=len(tree2["columns"]), column=0, columnspan=2)
# 选中
def select():
    global tree2_data
    global tree2_data_map
    global tree2_data_order_array
    data = [tree1_selected[1], tree1_selected[2], tree1_selected[3], tree1_selected[4], "片段", str(uuid.uuid4())]
    tree2_data.append(data)
    reloadTree2()

def choose():
    global tree2_data
    global tree2_data_map
    global tree2_data_order_array
    data = [tree1_selected[1], cutVideo.gettimeStr(tree1_selected[4], play_start_time), cutVideo.gettimeStr(tree1_selected[4], play_end_time), tree1_selected[4], "片段", str(uuid.uuid4())]
    tree2_data.append(data)
    reloadTree2()

# 插入
def insert():
    global tree2_data
    global tree2_data_map
    global tree2_data_order_array
    data = [tree1_selected[1], tree1_selected[2], tree1_selected[3], tree1_selected[4], "片段", str(uuid.uuid4())]
    tree2_data.insert(int(tree2_selected[0]), data)
    reloadTree2()

def view1():
    # video_name = cutVideo.generateVideoFile(tree1_selected)
    # print(video_name)
    # # 可以选择解码工具
    # PlayVideo(video_name)
    # #os.remove(video_name)
    player.play_list(tree2_data)

def PlayVideo(video_path):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()

def delete():
    global tree2_data
    select_uuid = tree2_selected[6]
    for data2 in tree2_data:
        if (data2[5] == select_uuid):
            tree2_data.remove(data2)
    reloadTree2()

# 重新加载tree2  
def reloadTree2():
    for item in tree2.get_children():
        tree2.delete(item)
    count = 0
    for data in tree2_data:
        dataTree2 = [str(count), data[0], data[1], data[2], data[3], data[4], data[5]]
        tree2.insert('', dataTree2[0], text='', values=dataTree2)
        count = count + 1

def save_cache():
    content = ent3.get()
    if (len(tree2_data) == 0):
        return
    if (content != ''):
        cache_file(content)

def cache_file(content):
    file_name = cache_file_dir + content + ".pk1"
    if (os.path.exists(file_name)):
        os.remove(file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(tree2_data, f)

def load_cache():
    content = ent3.get()
    if (content != ''):
        file_name = cache_file_dir + content + ".pk1"
        if (os.path.exists(file_name)):
            global tree2_data
            with open(file_name, 'rb') as f:
                content_all = pickle.load(f)
                for content in content_all:
                    if (content[4] == "片段"):
                        tree2_data.append(content)
                    if (content[4] == "视频" and content[0] != ''):
                        if (os.path.exists(content[3])):
                            tree2_data.append(content)
                        else:
                            tree2_data.append(generateVideoByText.getVideo(content[0]))
            reloadTree2()



# tree1 选中事件
def on_tree_select(event):
    print("")
    global tree1_selected
    for item in tree.selection():
        tree1_selected = tree.item(item,"values")
    #     if (len(tree1_selected) > 0):
    #         reloadTree3(tree1_selected[5])

def reloadTree3(id):
    results = mysqlutils.queryAroud(id, indexPath.get(combobox.get()))
    count = 0
    for hit in results:
        Data = [str(count), hit[1], hit[2], hit[3], hit[4]]
        tree3.insert('', Data[0], text='', values=Data)
        count = count + 1

# tree1 选中事件  
def on_tree2_select(event):
    global tree2_selected
    for item in tree2.selection():
        tree2_selected = tree2.item(item,"values")

def on_tree3_select(event):
    global tree3_selected
    for item in tree3.selection():
        tree3_selected = tree3.item(item, "values")



# 合成
def combine():
    video_clips = []
    video_names = []
    count = 0
    for data in tree2_data:
        if (data[4] == "片段") :
            select_data = [count, data[0], data[1], data[2], data[3]]
            name = cutVideo.generateVideoFile(select_data)
            video_names.append(name)
            videoname_resize = change_size(name)
            video_names.append(videoname_resize)
            video_clips.append(VideoFileClip(videoname_resize))
        if (data[4] == "视频"):
            videoname = data[3]
            video_names.append(videoname)
            videoname_resize = change_size(videoname)
            video_names.append(videoname_resize)
            video_clips.append(VideoFileClip(videoname_resize))
    if (len(video_names) > 0):
        save_path = "N:\\result\\result_" + str(random.randint(1,1000)) + "_"+ str(random.randint(1,1000)) + "_"+ str(random.randint(1,1000)) + ".mp4"
        clip = concatenate_videoclips(video_clips)
        # 生成目标视频文件, 修改fps
        clip.to_videofile(save_path, fps=18, remove_temp=False)
    # for name in video_names:
    #     os.remove(name)


def change_size(video_path: str, width=1366, height=768, bit_rate=2000):
    ext = os.path.basename(video_path).strip().split('.')[-1]
    if ext not in ['mp4']:
        raise Exception('format error')
    output_dir = "N:\\result\\"
    _result_path = os.path.join(
        output_dir, '{}.{}'.format(
            uuid.uuid1().hex, ext))
    ff = FFmpeg(inputs={'{}'.format(video_path): None}, outputs={
        _result_path: '-s {}*{} -b {}k'.format(width, height, bit_rate)})
    print(ff.cmd)
    ff.run()
    return _result_path

def resize_video(input_path):
    clip = VideoFileClip(input_path)
    resized_clip = clip.resize(width=1366, height=768)
    output_path = input_path.replace(".mp4", "_temp.mp4")
    resized_clip.write_videofile(output_path)
    return output_path

def geneVideo():
    text = ent2.get()
    if (text == ''):
        return
    video_path = generateVideoByText.getVideo(text, 1)
    data2_array=[text, "-", "-", video_path, "视频", str(uuid.uuid4())]
    global tree2_data
    tree2_data.append(data2_array)
    reloadTree2()

def geneVideo2():
    text = ent2.get()
    if (text == ''):
        return
    video_path = generateVideoByText.getVideo(text, 2)
    data2_array=[text, "-", "-", video_path, "视频", str(uuid.uuid4())]
    global tree2_data
    tree2_data.append(data2_array)
    reloadTree2()
# 搜成语


# 搜押韵


def play_cache():
    video_path = tree4_selected[4]
    global play_start_time
    play_start_time = cutVideo.get_start_time(tree4_selected[4], tree4_selected[2])
    player.play(video_path, play_start_time)

def insertVideo():
    text = ent2.get()
    if (text == ''):
        return
    video_path = generateVideoByText.getVideo(text)
    data2_array=[text, "-", "-", video_path, "视频", str(uuid.uuid4())]
    global tree2_data
    tree2_data.insert(int(tree2_selected[0]), data2_array)
    reloadTree2()

def table2_play():
    video_path = tree2_selected[4]
    if ("视频" == tree2_selected[5]):
        player.play(video_path, 0)
    else:
        global play_start_time
        play_start_time = cutVideo.get_start_time(tree2_selected[4], tree2_selected[2])
        player.play(video_path, play_start_time)

def table2_save():
    for data in tree2_data:
        if(tree2_selected[6] == data[5]):
            data[1] = cutVideo.gettimeStr(tree2_selected[4], play_start_time)
            data[2] = cutVideo.gettimeStr(tree2_selected[4], play_end_time)
    reloadTree2()

def play():
    video_path = tree1_selected[4]
    global play_start_time
    play_start_time = cutVideo.get_start_time(tree1_selected[4], tree1_selected[2])
    player.play(video_path, play_start_time)

def repeat():
    player.setTime(play_start_time)

def back1000():
    if (play_set_flag == 0) :
        global play_start_time
        play_start_time = play_start_time - 1000
        player.setTime(play_start_time)
    else:
        global play_end_time
        play_end_time = play_end_time - 1000
        player.setTime(play_end_time)

def back100():
    if (play_set_flag == 0):
        global play_start_time
        play_start_time = play_start_time - 100
        player.setTime(play_start_time)
    else:
        global play_end_time
        play_end_time = play_end_time - 100
        player.setTime(play_end_time)

def forward1000():
    if (play_set_flag == 0):
        global play_start_time
        play_start_time = play_start_time + 1000
        player.setTime(play_start_time)
    else:
        global play_end_time
        play_end_time = play_end_time + 1000
        player.setTime(play_end_time)

def forward100():
    if (play_set_flag == 0):
        global play_start_time
        play_start_time = play_start_time + 100
        player.setTime(play_start_time)
    else:
        global play_end_time
        play_end_time = play_end_time + 100
        player.setTime(play_end_time)

def pause():
    player.pause()
    global play_end_time
    play_end_time = player.get_time()
    print(player.get_time())

def set_start_time():
    global play_start_time
    play_start_time = player.get_time()
    print(player.get_time())

def resume():
    player.resume()

def stop():
    player.stop()

def start_set():
    global play_set_flag
    play_set_flag = 0

def end_set():
    global play_set_flag
    play_set_flag = 1

def normal():
    player.set_rate(1)

def fast_120():
    player.set_rate(1.2)

def fast_150():
    player.set_rate(1.5)

def fast_200():
    player.set_rate(2)
###### cache ######

def add_cache():
    global tree4_data
    print(str(tree2_selected))
    data = [tree2_selected[1], tree2_selected[2], tree2_selected[3], tree2_selected[4], tree2_selected[5], tree2_selected[6]]
    tree4_data.append(data)
    reloadTree4()

def add_cache_select():
    global tree2_data
    data = [tree4_selected[1], tree4_selected[2], tree4_selected[3], tree4_selected[4], tree4_selected[5], str(uuid.uuid4())]
    tree2_data.append(data)
    reloadTree2()

def insert_cache_select():
    global tree2_data
    data = [tree4_selected[1], tree4_selected[2], tree4_selected[3], tree4_selected[4], tree4_selected[5], str(uuid.uuid4())]
    tree2_data.insert(int(tree2_selected[0]), data)
    reloadTree2()

def on_tree4_select(event):
    global tree4_selected
    for item in tree4.selection():
        tree4_selected = tree4.item(item, "values")

# 重新加载tree4
def reloadTree4():
    for item in tree4.get_children():
        tree4.delete(item)
    count = 0
    for data in tree4_data:
        dataTree4 = [str(count), data[0], data[1], data[2], data[3], data[4], data[5]]
        tree4.insert('', dataTree4[0], text='', values=dataTree4)
        count = count + 1

# news
# 重新加载tree4
def reloadTree3():
    for item in tree3.get_children():
        tree3.delete(item)
    count = 0
    for data in tree3_data:
        dataTree3 = [str(count), data[0], data[1], data[2], data[3]]
        tree3.insert('', dataTree3[0], text='', values=dataTree3)
        count = count + 1
    count_long()

def choose_3():
    global tree3_data
    print(str(tree2_selected))
    data = [tree2_selected[1], tree2_selected[2], tree2_selected[3], tree2_selected[4]]
    tree3_data.append(data)
    reloadTree3()


def count_long():
    time_duration_total = 0
    for data in tree3_data:
        print(str(data))
        start_time_mill = cutVideo.getTimeMill(data[1])
        end_time_mill = cutVideo.getTimeMill(data[2])
        time_duration = end_time_mill - start_time_mill
        time_duration_total = time_duration_total + time_duration
    namestr301.set(str(time_duration_total))



def delete_3():
    global tree3_data
    select_uuid = tree3_selected[1]
    for data3 in tree3_data:
        if (data3[0] == select_uuid):
            tree3_data.remove(data3)
    reloadTree3()

def update_3():
    print(str(111))

def combine_3():
    # 首先将视频合成一个
    video_path = cutVideo.combine_no_voice(tree3_data, cache_ent304.get())
    # 插入到table2中
    global tree2_data
    ata2_array = ["", "-", "-", video_path, "视频", str(uuid.uuid4())]
    tree2_data.append(ata2_array)
    reloadTree2()

def import_voice():
    voice_path = cache_ent304.get()
    audio = AudioSegment.from_file(voice_path, "wav")
    namestr303.set(str(len(audio)))

def cleanall_3():
    print(111)

def combine_voice_3():
    # 获取输入的语音文字
    voice_text = cache_ent302.get()
    voice_path = generateVideoByText.get_voice_by_text(voice_text, 5118, 7, 3)
    global audio_path
    audio_path = voice_path
    # 获取音频长度
    audio = AudioSegment.from_file(voice_path, "mp3")
    namestr304.set(voice_path)
    namestr303.set(str(len(audio)))

def import_cache():
    content = cache_ent1.get()
    if (content != ''):
        file_name = cache_file_dir + content + ".pk1"
        if (os.path.exists(file_name)):
            global tree4_data
            with open(file_name, 'rb') as f:
                content_all = pickle.load(f)
                for content in content_all:
                    if (content[4] == "片段"):
                        tree4_data.append(content)
                    if (content[4] == "视频" and content[0] != ''):
                        if (os.path.exists(content[3])):
                            tree4_data.append(content)
                        else:
                            tree4_data.append(generateVideoByText.getVideo(content[0]))
            reloadTree4()
####### cache #########
curr_index=0
##############  UI   ##############
class Screen(tk.Frame):

    '''
    Screen widget: Embedded video player from local or youtube
    '''

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg='black')
        self.parent = parent
        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def add_callback(self, event_type, callback):
        self.player.event_manager().event_attach(event_type, callback)

    def play(self, _source, starttime):
        # Function to start player from given source
        Media = self.instance.media_new(_source)
        Media.get_mrl()
        self.player.set_media(Media)
        self.player.set_hwnd(self.winfo_id())
        self.player.play()
        print(starttime)
        self.player.set_time(starttime)

    def play_list(self, tree2_data):
        print(11)
        # # Function to start player from given source
        # global  curr_index
        # curr_index = 0
        # play(tree2_data[0][3], ree2_data[0][1])

    def my_callback(self):
        print(11)

    def setTime(self, starttime):
        self.player.set_time(starttime)

    def isPlaying(self):
        return self.player.is_playing()

    # 暂停
    def pause(self):
        self.player.pause()

    # 恢复
    def resume(self):
        self.player.set_pause(0)

    # 停止
    def stop(self):
        self.player.stop()

    # 释放资源
    def release(self):
        return self.player.release()

    def get_time(self):
        return self.player.get_time()

    def set_rate(self, rate):
        return self.player.set_rate(rate)

if __name__ == "__main__":
    #1
    root = Tk()
    player = Screen(root)

    #2
    root.geometry('1600x1100')
    #3
    root.title('my window')
    btn1 = Button(root,text='添加视频')
    btn1.grid(row=0,column=0, ipadx=20,ipady=1,padx=10,pady=10)

    btn2 = Button(root,text='文字视频', command=geneVideo)
    btn2.grid(row=1,column=7, ipadx=20,ipady=1,padx=10,pady=10)

    btn2 = Button(root, text='插入背景文字', command=geneVideo2)
    btn2.grid(row=1, column=9, ipadx=20, ipady=1, padx=10, pady=10)

    btn2yayun = Button(root, text='搜押韵', command=queryyayun)
    btn2yayun.grid(row=1, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    btn2chengyu = Button(root, text='搜接龙', command=queryjielong)
    btn2chengyu.grid(row=1, column=13, ipadx=20, ipady=1, padx=10, pady=10)

    btn3 = Button(root,text='选中', command=select)
    btn3.grid(row=0,column=2, ipadx=20,ipady=1,padx=10,pady=10)

    btn4 = Button(root,text='搜索', command=querydb)
    btn4.grid(row=1,column=4, ipadx=20,ipady=1,padx=10,pady=10)

    btn5 = Button(root,text='预览', command=view1)
    btn5.grid(row=0,column=3, ipadx=20,ipady=1,padx=10,pady=10)

    btn6 = Button(root,text='删除', command=delete)
    btn6.grid(row=0,column=4, ipadx=20,ipady=1,padx=10,pady=10)

    btn7 = Button(root,text='插入', command=insert)
    btn7.grid(row=0,column=5, ipadx=20,ipady=1,padx=10,pady=10)

    btn8 = Button(root,text='播放', command=play)
    btn8.grid(row=0,column=6, ipadx=20,ipady=1,padx=10,pady=10)

    btn9 = Button(root,text='合成', command=combine)
    btn9.grid(row=0,column=7, ipadx=20,ipady=1,padx=10,pady=10)

    btn10 = Button(root, text='保存', command=save_cache)
    btn10.grid(row=0, column=10, ipadx=20, ipady=1, padx=10, pady=10)

    btn10 = Button(root, text='加载', command=load_cache)
    btn10.grid(row=0, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    
    value = StringVar()
    values = ["三国演义","2010版三国演义", "水浒传", "西游记", "红楼梦", "亮剑"]
    value.set(values[0])
    combobox = ttk.Combobox(
      master=root, # 父容器
      height=8, # 高度,下拉显示的条目数量
      width=16, # 宽度
      state="normal", # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
      cursor="arrow", # 鼠标移动时样式 arrow, circle, cross, plus...
      font=("", 15), # 字体
      textvariable = value, # 通过StringVar设置可改变的值
      values = values, # 设置下拉框的选项
    )
    combobox.grid(row=1, column=0, columnspan=2,sticky=W, ipadx=10, ipady=1,padx=10,pady=10)

    # 输入框
    ent1 = ttk.Entry(root, width=25)
    ent1.grid(row=1, column=2, columnspan=2, sticky=W, padx=10, pady=10)

    # 文字视频输入框
    ent2 = ttk.Entry(root, width=25)
    ent2.grid(row=1, column=5, columnspan=2, sticky=W, padx=10, pady=10)

    # 保存的目录名称
    ent3 = ttk.Entry(root, width=25)
    ent3.grid(row=0, column=8, columnspan=2, sticky=W, padx=10, pady=10)

    # 查询表格
    tree = ttk.Treeview(root, show="headings", height=20)  # 创建表格对象，show="headings" 为隐藏首列，height 为表格高度（行）
    columns = {
        'ID': 20,
        '字幕': 200,
        '开始时间': 100,
        '结束时间': 100,
        '': 1,
        'u': 1
    }  # 列头标题和对应的宽度，随便增删改查
    tree['columns'] = list(columns)  # 批量设置列头标题
    for column in columns:  # 批量设置列属性
        tree.heading(column, text=column)  # #设置列标题
        tree.column(column, width=columns[column], anchor='center')  # 设置列酷安，anchor 为锚点，'center' 表示中央居中
        # 也可以用方位词东南西北的英文缩写表示，即 N(North, 北): 上中对齐、SW(South West, 西南)：左下对齐
        # tree.column(column, width=columns[column], anchor=tkinter.SW)  # 示例，只改 SW 就行
        # anchor: n, ne, e, se, s, sw, w, nw, or center
        # tree.heading(column, command=lambda _col=column: treeview_sort_column(tree, _col, False))  # 设置点击执行排序操作
    tree.grid(row=2, column=0, rowspan=15, columnspan=5, sticky=W, padx=10, pady=10)
    tree.bind("<Double-1>", edit_row)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # 播放窗口
    player = Screen(root)
    player.place(x=950, y=115, width=60, height=40)

    #按钮1
    play_btn1 = Button(root, text='暂停', command=pause)
    play_btn1.grid(row=20, column=9, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn2 = Button(root, text='恢复' , command=resume)
    play_btn2.grid(row=20, column=10, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn3 = Button(root, text='停止', command=stop)
    play_btn3.grid(row=20, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn4 = Button(root, text='选中', command = choose)
    play_btn4.grid(row=20, column=12, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn5 = Button(root, text='重播', command=repeat)
    play_btn5.grid(row=20, column=13, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn10 = Button(root, text='开始', command=set_start_time)
    play_btn10.grid(row=20, column=14, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn6 = Button(root, text='起点', command=start_set)
    play_btn6.grid(row=21, column=9, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn7 = Button(root, text='退1秒', command=back1000)
    play_btn7.grid(row=21, column=10, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn8 = Button(root, text='退100毫秒', command=back100)
    play_btn8.grid(row=21, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn9 = Button(root, text='进100毫秒', command=forward100)
    play_btn9.grid(row=21, column=12, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn11 = Button(root, text='进1秒', command=forward1000)
    play_btn11.grid(row=21, column=13, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn12 = Button(root, text='终点', command=end_set)
    play_btn12.grid(row=21, column=14, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn13 = Button(root, text='正常', command=normal)
    play_btn13.grid(row=22, column=9, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn14 = Button(root, text='1.2倍', command=fast_120)
    play_btn14.grid(row=22, column=10, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn15 = Button(root, text='1.5倍', command=fast_150)
    play_btn15.grid(row=22, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn16 = Button(root, text='2倍', command=fast_200)
    play_btn16.grid(row=22, column=12, ipadx=20, ipady=1, padx=10, pady=10)



    # 查询表格
    tree3 = ttk.Treeview(root, show="headings", height=10)  # 创建表格对象，show="headings" 为隐藏首列，height 为表格高度（行）
    columns3 = {
        'ID': 20,
        '字幕': 200,
        '开始时间': 100,
        '结束时间': 100,
        '': 1
    }  # 列头标题和对应的宽度，随便增删改查
    tree3['columns'] = list(columns3)  # 批量设置列头标题
    for column in columns3:  # 批量设置列属性
        tree3.heading(column, text=column)  # #设置列标题
        tree3.column(column, width=columns3[column], anchor='center')  # 设置列酷安，anchor 为锚点，'center' 表示中央居中
        # 也可以用方位词东南西北的英文缩写表示，即 N(North, 北): 上中对齐、SW(South West, 西南)：左下对齐
        # tree.column(column, width=columns[column], anchor=tkinter.SW)  # 示例，只改 SW 就行
        # anchor: n, ne, e, se, s, sw, w, nw, or center
        # tree.heading(column, command=lambda _col=column: treeview_sort_column(tree, _col, False))  # 设置点击执行排序操作
    tree3.grid(row=21, column=0, rowspan=6, columnspan=15, sticky=W, padx=10, pady=10)
    tree3.bind("<Double-1>", edit_row)
    tree3.bind("<<TreeviewSelect>>", on_tree3_select)

    play_btn301 = Button(root, text='选中', command=choose_3)
    play_btn301.grid(row=28, column=0, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn302 = Button(root, text='删除', command=delete_3)
    play_btn302.grid(row=28, column=1, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn303 = Button(root, text='保存', command=update_3)
    play_btn303.grid(row=28, column=2, ipadx=20, ipady=1, padx=10, pady=10)

    namestr301 = StringVar()
    cache_ent301 = ttk.Entry(root, width=10, textvariable=namestr301)
    cache_ent301.grid(row=28, column=3, columnspan=2, sticky=W, padx=10, pady=10)

    namestr302 = StringVar()
    cache_ent302 = ttk.Entry(root, width=30, textvariable=namestr302)
    cache_ent302.grid(row=29, column=0, columnspan=5, sticky=W, padx=10, pady=10)

    namestr303 = StringVar()
    cache_ent303 = ttk.Entry(root, width=10, textvariable=namestr303)
    cache_ent303.grid(row=29, column=3, columnspan=5, sticky=W, padx=10, pady=10)

    namestr304 = StringVar()
    cache_ent304 = ttk.Entry(root, width=30, textvariable=namestr304)
    cache_ent304.grid(row=29, column=9, columnspan=5, sticky=W, padx=10, pady=10)

    play_btn307 = Button(root, text='导入', command=import_voice)
    play_btn307.grid(row=29, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn306 = Button(root, text='语音', command=combine_voice_3)
    play_btn306.grid(row=30, column=0, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn304 = Button(root, text='合成', command=combine_3)
    play_btn304.grid(row=30, column=1, ipadx=20, ipady=1, padx=10, pady=10)

    play_btn305 = Button(root, text='清空', command=cleanall_3)
    play_btn305.grid(row=30, column=2, ipadx=20, ipady=1, padx=10, pady=10)




    # 缓存表格
    tree4 = ttk.Treeview(root, show="headings", height=20)  # 创建表格对象，show="headings" 为隐藏首列，height 为表格高度（行）
    columns4 = {
        'ID': 20,
        '字幕': 200,
        '开始时间': 100,
        '结束时间': 100,
        '': 1,
        '类型': 50,
        'uuid': 1
    }  # 列头标题和对应的宽度，随便增删改查
    tree4['columns'] = list(columns4)  # 批量设置列头标题
    for column in columns4:  # 批量设置列属性
        tree4.heading(column, text=column)  # #设置列标题
        tree4.column(column, width=columns4[column], anchor='center')  # 设置列酷安，anchor 为锚点，'center' 表示中央居中
        # 也可以用方位词东南西北的英文缩写表示，即 N(North, 北): 上中对齐、SW(South West, 西南)：左下对齐
        # tree.column(column, width=columns[column], anchor=tkinter.SW)  # 示例，只改 SW 就行
        # anchor: n, ne, e, se, s, sw, w, nw, or center
        # tree.heading(column, command=lambda _col=column: treeview_sort_column(tree, _col, False))  # 设置点击执行排序操作
    tree4.grid(row=21, column=4, rowspan=15, columnspan=5, sticky=W, padx=10, pady=10)
    tree4.bind("<Double-1>", edit_row)
    tree4.bind("<<TreeviewSelect>>", on_tree4_select)

    cache_btn1 = Button(root, text='增加', command=add_cache)
    cache_btn1.grid(row=24, column=9, ipadx=20, ipady=1, padx=10, pady=10)

    cache_btn2 = Button(root, text='选中', command=add_cache_select)
    cache_btn2.grid(row=24, column=10, ipadx=20, ipady=1, padx=10, pady=10)

    cache_btn3 = Button(root, text='插入', command=insert_cache_select)
    cache_btn3.grid(row=24, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    cache_btn3 = Button(root, text='播放', command=play_cache)
    cache_btn3.grid(row=24, column=12, ipadx=20, ipady=1, padx=10, pady=10)

    # 输入框
    cache_ent1 = ttk.Entry(root, width=25)
    cache_ent1.grid(row=25, column=9, columnspan=2, sticky=W, padx=10, pady=10)

    cache_btn4 = Button(root, text='导入', command=import_cache)
    cache_btn4.grid(row=25, column=11, ipadx=20, ipady=1, padx=10, pady=10)

    # 选中表格
    tree2 = ttk.Treeview(root, show="headings", height=20)  # 创建表格对象，show="headings" 为隐藏首列，height 为表格高度（行）
    columns2 = {
        'ID': 20,
        '字幕': 200,
        '开始时间': 100,
        '结束时间': 100,
        '': 1,
        '类型': 50,
        'uuid': 1
    }  # 列头标题和对应的宽度，随便增删改查
    tree2['columns'] = list(columns2)  # 批量设置列头标题
    for column in columns2:  # 批量设置列属性
        tree2.heading(column, text=column)  # #设置列标题
        tree2.column(column, width=columns2[column], anchor='center')  # 设置列酷安，anchor 为锚点，'center' 表示中央居中
        # 也可以用方位词东南西北的英文缩写表示，即 N(North, 北): 上中对齐、SW(South West, 西南)：左下对齐
        # tree.column(column, width=columns[column], anchor=tkinter.SW)  # 示例，只改 SW 就行
        # anchor: n, ne, e, se, s, sw, w, nw, or center
        # tree2.heading(column, command=lambda _col=column: treeview_sort_column(tree, _col, False))  # 设置点击执行排序操作
    tree2.grid(row=2, column=4, rowspan=15, columnspan=5, sticky=W, padx=10, pady=10)
    tree2.bind("<Double-1>", edit_row2)
    tree2.bind("<<TreeviewSelect>>", on_tree2_select)

    select_btn1 = Button(root, text='播放', command=table2_play)
    select_btn1.grid(row=20, column=4, ipadx=20, ipady=1, padx=10, pady=10)

    select_btn2 = Button(root, text='保存', command=table2_save)
    select_btn2.grid(row=20, column=5, ipadx=20, ipady=1, padx=10, pady=10)

    # Create a frame
    app = Frame(root, bg="white")
    app.grid(row=2, column=8, rowspan=15, columnspan=4, sticky=W, padx=10, pady=10)
    # Create a label in the frame
    lmian = Label(app)
    lmian.grid(row=2, column=8, rowspan=20, columnspan=5, sticky=W, padx=10, pady=10)

    root.mainloop()