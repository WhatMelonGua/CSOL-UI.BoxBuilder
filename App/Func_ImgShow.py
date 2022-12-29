# coding:utf-8
from PIL import Image, ImageTk

imgFile = None  # 展示图像
wheelSize = 1   # 缩放系数
boxMult = 1
multType = 'num'

def imgUpdate(imgIn, canvas):
    global imgFile, wheelSize
    if multType == 'num':
        img = imgIn.copy().resize( ( int(imgIn.size[0]*wheelSize*boxMult), int(imgIn.size[1]*wheelSize*boxMult) ), Image.Resampling.NEAREST )
    elif multType == 'var':
        img = imgIn.copy().resize( ( int(imgIn.size[0]*wheelSize), int(imgIn.size[1]*wheelSize) ), Image.Resampling.NEAREST )
    else:
        return None
    imgFile = ImageTk.PhotoImage(img)
    canvasObj = canvas.create_image(312, 302, anchor="center", image=imgFile)
    return canvasObj
# 更新imgShow数据后，通过imgFile更新画布的函数      |img:更新的图像
def showInit(path, canvas):
    global imgFile
    imgFile = ImageTk.PhotoImage(Image.open(path).convert('RGBA'))
    canvasObj = canvas.create_image(312, 302, anchor="center", image=imgFile)
    return canvasObj
# 用于返回一个 canvasImage对象,不过是直接path路径进行转换，用于软件启动的展示窗口初始化，展示“图片未选择”

def imgWheelSize(delta):
    global wheelSize
    # 确定缩放系数
    if delta > 0:
        wheelSize *= 1.1
    if delta < 0:
        wheelSize *= 0.9
    else:
        pass
# tkCanvas滚轮的虚拟图像缩放函数                   |delta:鼠标滚动量，img:更新的图像
def imgWheelSizeInit():
    global wheelSize
    wheelSize = 1
# tkCanvas滚轮大小初始化函数                       |img:更新的图像