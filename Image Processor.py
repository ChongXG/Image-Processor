import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from tkinter import messagebox
from datetime import datetime
import os

def open_file_dialog():
    global file_paths
    global folder_path
    file_paths = filedialog.askopenfilenames(title="选择图片文件",filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.ico")],multiple=True)
    folder_path = os.path.dirname(file_paths[0]) + "/output/"
    
    # 确保输出文件夹存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for file_path in file_paths:
        # 打开用户选择的图像
        input_image = Image.open(file_path)
        print(file_path)

        # 获取图像通道
        bands = input_image.getbands()

        # 判断图片是否具备透明通道
        if 'A' in bands:
            pre_image = Image.new("RGB", input_image.size, (255, 255, 255))
            pre_image.paste(input_image, (0, 0), input_image)
        else:
            pre_image = input_image

        # 获取原始图像的宽度和高度
        width, height = pre_image.size

        # 计算新的尺寸，以保持最短边为预设像素
        if width < height:
            new_width = int(entry.get())
            new_height = int(int(entry2.get()) * (height / width))
        else:
            new_width = int(int(entry.get()) * (width / height))
            new_height = int(entry2.get())

        # 使用Image.LANCZOS算法等比例缩放图像
        resized_image = pre_image.resize((new_width, new_height), Image.LANCZOS)

        # 计算裁剪的坐标以使图像变为预设值
        left = (new_width - int(entry.get())) / 2
        top = (new_height - int(entry2.get())) / 2
        right = left + int(entry.get())
        bottom = top + int(entry2.get())

        # 裁剪图像
        cropped_image = resized_image.crop((left, top, right, bottom))
        now = datetime.now()
        # 保存结果图像
        time_string = now.strftime("%Y-%m-%d %H-%M-%S.%f") + ".jpg"
        print(file_path)
        cropped_image.save(f"{folder_path}" + f"{time_string}", "JPEG", quality=100)

    os.startfile(folder_path)

# 创建一个简单的GUI窗口
root = tk.Tk()
root.title("Image Processor   By ChongXG")

# 设置窗口尺寸，例如设置为宽800像素、高600像素
root.geometry("310x90")

# 创建一个框架以容纳按钮，并使用grid布局管理器
frame = tk.Frame(root)
frame.grid(row=0, column=0, padx=0, pady=0)

# 添加一个按钮，用于触发文件对话框，并使用grid布局管理器
button = tk.Button(frame, text=" 选 择 \n 图 像 ", command=open_file_dialog, height=3, font=("font",12))
button.grid(row=0, column=3, rowspan=2, padx=10, pady=0)

# 在框架中创建一个标签，并使用grid布局管理器
label = tk.Label(frame, text="请输入宽:", font=("font",15))
label.grid(row=0, column=1, padx=10, pady=10)

# 在框架中创建一个文本输入框，并使用grid布局管理器
entry = tk.Entry(frame, width=8, font=("font",15))
entry.grid(row=0, column=2, padx=10, pady=10)
entry.insert(0, "600")

# 在框架中创建一个标签，并使用grid布局管理器
label2 = tk.Label(frame, text="请输入高:", font=("font",15))
label2.grid(row=1, column=1, padx=0, pady=5)

# 在框架中创建一个文本输入框，并使用grid布局管理器
entry2 = tk.Entry(frame, width=8, font=("font",15))
entry2.grid(row=1, column=2, padx=0, pady=5)
entry2.insert(0, "600")

# 启动GUI主循环
root.mainloop()