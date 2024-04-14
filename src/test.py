import tkinter as tk
import os
import subprocess

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")

        # 显示器
        self.result = tk.StringVar()
        self.result.set(0)
        self.result_label = tk.Label(self.master, textvariable=self.result, font=("Arial", 18), width=20, anchor="e")
        self.result_label.grid(row=0, column=0, columnspan=4)

        # 数字按钮
        self.create_button("7", 1, 0)
        self.create_button("8", 1, 1)
        self.create_button("9", 1, 2)
        self.create_button("4", 2, 0)
        self.create_button("5", 2, 1)
        self.create_button("6", 2, 2)
        self.create_button("1", 3, 0)
        self.create_button("2", 3, 1)
        self.create_button("3", 3, 2)
        self.create_button("0", 4, 1)

        # 运算符按钮
        self.create_button("+", 1, 3)
        self.create_button("-", 2, 3)
        self.create_button("*", 3, 3)
        self.create_button("/", 4, 3)

        # 其他按钮
        self.create_button(".", 4, 0)
        self.create_button("C", 4, 2)
        self.create_button("=", 5, 3)

    def create_button(self, text, row, column):
        button = tk.Button(self.master, text=text, font=("Arial", 18), width=5,
                           command=lambda: self.on_button_click(text))
        button.grid(row=row, column=column)

    def on_button_click(self, text):
        if text == "C":
            # 清空显示器
            self.result.set(0)
            return

        if text == "=":
            # 计算结果
            try:
                result = eval(self.result.get())
                self.result.set(result)
            except:
                messagebox.showerror("Error", "Invalid expression")
            return

        # 更新显示器
        if self.result.get() == "0":
            self.result.set(text)
        else:
            self.result.set(self.result.get() + text)
def is_in(full_str, sub_str):
    try:
        full_str.index(sub_str)
        return True
    except ValueError:
        return False

def sanguo1():
    data_path = data_path = "N:\\三国演义\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".mp4":
                name = os.path.splitext(file)[0]
                name_pre2 = name[:2]
                for root2, dirs2, files2 in os.walk(data_path):
                    for file2 in files2:
                        if os.path.splitext(file2)[1] == ".srt":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file2), os.path.join(root2, name + ".srt"))
                        if os.path.splitext(file2)[1] == ".ts":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file2), os.path.join(root2, name + ".ts"))

def shuihu():
    data_path = data_path = "N:\\水浒传\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".mkv":
                name = os.path.splitext(file)[0]
                name_pre2 = name[:2]
                for root2, dirs2, files2 in os.walk(data_path):
                    for file2 in files2:
                        if os.path.splitext(file2)[1] == ".srt":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file), os.path.join(root2, os.path.splitext(file2)[0] + ".mkv"))
                        if os.path.splitext(file2)[1] == ".ts":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file2), os.path.join(root2, name + ".ts"))

def xiyouji():
    data_path = data_path = "N:\\西游记\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                name = os.path.splitext(file)[0]
                name_pre2 = name[:2]
                for root2, dirs2, files2 in os.walk(data_path):
                    for file2 in files2:
                        if os.path.splitext(file2)[1] == ".mp4":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file), os.path.join(root2, os.path.splitext(file2)[0] + ".srt"))
def xiyouji_xu():
    data_path = data_path = "N:\\西游记续集\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                name = os.path.splitext(file)[0]
                name_pre2 ="第" + name[:2] + "集"
                for root2, dirs2, files2 in os.walk(data_path):
                    for file2 in files2:
                        if os.path.splitext(file2)[1] == ".mp4":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file), os.path.join(root2, os.path.splitext(file2)[0] + ".srt"))


def liangjian():
    data_path = data_path = "N:\\亮剑\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".srt":
                name = os.path.splitext(file)[0]
                name_pre2 = name[:2]
                for root2, dirs2, files2 in os.walk(data_path):
                    for file2 in files2:
                        if os.path.splitext(file2)[1] == ".mp4":
                            if (is_in(os.path.splitext(file2)[0], name_pre2)):
                                os.rename(os.path.join(root2, file), os.path.join(root2, os.path.splitext(file2)[0] + ".srt"))

def rename():
    data_path = "N:\\亮剑\\"
    # data_path = data_path = "N:\\水浒传\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".mp4":
                name = file.replace("李幼斌无删减版.Drawing.Sword.2005.E", "")
                os.rename(os.path.join(root, file), os.path.join(root, name))
           # name = file.split("The")[0] + "srt"
           # os.rename(os.path.join(root, file), os.path.join(root, name))

def transfType():
    data_path = "N:\\水浒传\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".mkv":
                new_name = os.path.splitext(file)[0] + ".mp4"
                subprocess.call(['ffmpeg', '-i', os.path.join(root, file), '-codec', 'copy', os.path.join(root, new_name)])

if __name__ == "__main__":
    xiyouji_xu()
