from tkinter import *
from tkinter import messagebox

class Application(Frame):

    def __init__(self, master=None):  # master模板容器，画纸放到哪
        # 继承方法，父类的重新定义
        super().__init__(master)  # 定义属性
        self.master = master
        self.pack()  # 画纸几何布局，默认摆放
        self.CreatWidget()  # 创建示例对象时，自动进行调用


    def CreatWidget(self):
        '''创建组件'''
        self.label01 = Label(self, text='关键字')
        self.label01.pack()

        # 获取输入框的信息，输入框的内容是可变的
        # v1是可变的,创建变量StringVar绑定到组件上,StringVar发生变化，组件内容entry01的值也会发生变化
        v1 = StringVar()
        self.entry01 = Entry(self, textvariable=v1)
        self.entry01.pack()
        print(v1.get())  # 获取变量的信息
        Button(self, text='查询', command=self.login).pack()

        var2 = StringVar()
        var2.set((1,2,3,4))
        self.lb0 = Listbox(self, listvariable=var2)
        self.lb0.pack()

    def login(self):
        # 用组件接受用户输入的信息
        keywords = self.entry01.get()
        print(keywords)
        select = self.lb0.get(self.lb0.curselection())
        print(select)


if __name__ == "__main__":
    root = Tk()  # 创建主窗口
    root.title('标题-经典GUI程序类的测试')
    root.geometry('1000x600+900+300')

    # 创建画纸对象放到root画板上
    Application(master=root)
    root.mainloop()  # 消息循环