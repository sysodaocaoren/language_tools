import os
import shutil

if __name__ == "__main__":
    # root = tk.Tk()
    # calculator = Calculator(root)
    # root.mainloop()
    data_path =  data_path = "N:\\新三国\\"
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if os.path.splitext(file)[1] == ".mp4":
                print(os.path.join(root, file.replace("E", "")))
                shutil.copy(os.path.join(root, file.replace("E", "")), data_path)