# coding:utf-8
# region
from PIL import Image, ImageSequence
# endregion
#库导入完成
import App.threadHandle as threadHandle
import copy

''' 图片简化处理模块 '''
#region
setMode = 0         # 依据 RGB or HSV or Nil 进行优化
simVector = True    # 块状优化搜寻方向
setR = 20
setG = 20
setB = 20
setA = 40
alphaSet = 50       # 透明度识别阈值
#endregion
#简化使用的全局设置变量
# region
def parmGet():
    global setR, setG, setB, setA, alphaSet, setMode
    return setR, setG, setB, setA, alphaSet, setMode
def RGBAset(R, G, B, A, alpha):
    global setR, setG, setB, setA, alphaSet
    setR = R
    setG = G
    setB = B
    setA = A
    alphaSet = alpha
# R G B A alpha 阈值设定
def switchVector():
    global simVector
    simVector = not simVector
    return simVector
# 块优化方向更改               |return:bool True为横向，False为纵向
def switchMode():
    global setMode
    setMode = (setMode + 1) % 3
    return setMode
# 优化方式调整                 |return: 0 / 1 / 2 分别代表 RGB / HSV / 无优化
# endregion
#RGB阈值更改接口
# region
def rgbColorInfect(imgIn:Image.Image, setR:int, setG:int, setB:int, setA:int, vector:str):
    img = imgIn.copy()
    srcPix = img.getpixel((0, 0))
    imgSize = img.size
    if vector == "y":
        for w in range(imgSize[0]):
            for h in range(imgSize[1]):
                pos = (w, h)
                newPix = img.getpixel(pos)
                if abs(newPix[0] - srcPix[0]) < setR and abs(newPix[1] - srcPix[1]) < setG \
                        and abs(newPix[2] - srcPix[2]) < setB and abs(newPix[3] - srcPix[3]) < setA:
                    img.putpixel(pos, srcPix)
                else:
                    srcPix = newPix
    elif vector == "x":
        for h in range(imgSize[1]):
            for w in range(imgSize[0]):
                pos = (w, h)
                newPix = img.getpixel(pos)
                if abs(newPix[0] - srcPix[0]) < setR and abs(newPix[1] - srcPix[1]) < setG \
                        and abs(newPix[2] - srcPix[2]) < setB and abs(newPix[3] - srcPix[3]) < setA:
                    img.putpixel(pos, srcPix)
                else:
                    srcPix = newPix
    else:
        print("Error: vector can only be x | y")
        return
    return img
def hsvColorInfect(imgIn:Image.Image, setH:int, setS:int, setV:int,  vector:str):
    img = imgIn.copy()
    srcPix = img.getpixel((0, 0))
    imgSize = img.size
    if vector == "y":
        for w in range(imgSize[0]):
            for h in range(imgSize[1]):
                pos = (w, h)
                newPix = img.getpixel(pos)
                if abs(newPix[0] - srcPix[0]) < setH and abs(newPix[1] - srcPix[1]) < setS \
                        and abs(newPix[2] - srcPix[2]) < setV:
                    img.putpixel(pos, srcPix)
                else:
                    srcPix = newPix
    elif vector == "x":
        for h in range(imgSize[1]):
            for w in range(imgSize[0]):
                pos = (w, h)
                newPix = img.getpixel(pos)
                if abs(newPix[0] - srcPix[0]) < setH and abs(newPix[1] - srcPix[1]) < setS \
                        and abs(newPix[2] - srcPix[2]) < setV:
                    img.putpixel(pos, srcPix)
                else:
                    srcPix = newPix
    else:
        print("Error: vector can only be x | y")
        return
    return img
def alphaFilter(imgIn:Image.Image,Set:int):
    img = imgIn.copy()
    for w in range(img.size[0]):
        for h in range(img.size[1]):
            pixNow = img.getpixel((w, h))
            if pixNow[3] < Set:
                img.putpixel((w, h),(pixNow[0],pixNow[1],pixNow[2],0))
    return img
# endregion
#图像块化函数
def imgSimple(imgIn):
    global simVector, imgShow
    img = copy.deepcopy(imgIn)
    for i in range(len(img)):
        img[i] = alphaFilter(img[i], alphaSet)
    funcSeq=("y", "x")
    if simVector == False:
        funcSeq = ("x", "y")
    for i in range(len(img)):
        if setMode == 0:
            img[i] = rgbColorInfect(img[i], setR, setG, setB, setA, funcSeq[0])
            img[i] = rgbColorInfect(img[i], setR, setG, setB, setA, funcSeq[1])
        elif setMode == 1:
            img[i] = hsvColorInfect(img[i], setR, setG, setB, funcSeq[0])
            img[i] = hsvColorInfect(img[i], setR, setG, setB, funcSeq[1])
        else:
            pass
    imgShow = img
    threadHandle.outputTaskExit = False
    return
# 优化色块实际调用主函数
def imgColorDecrease(colorNum:int):
    global imgShow
    for i in range(len(imgShow)):
        imgShow[i] = (imgShow[i].convert("P", palette=Image.Palette.ADAPTIVE, colors=colorNum)).convert("RGBA")
# 减少颜色调用主函数
'''图像导入及处理'''
# region
graySwitch = False
imgData = []
imgShow = []
# endregion
# 基本
# region
frameVal = 0
frameNum = 0
speed = 100
gifTicker = None
def speedChange(n):
    global speed
    speed = n
# endregion
# gif
# 储存图像基本数据的变量声明

# region
def imgGet(path):
    global frameNum, frameVal, imgShow, imgData
    imgData = []
    imgData.append(Image.open(path).convert("RGBA"))
    frameNum = len(imgData)
    frameVal = 0
    imgShow = copy.deepcopy(imgData)
    return imgData[0].size
# 打开img后获取信息并储存处理的函数        |path:图像路径      |return:原图像尺寸
def imgsGet(path):
    global frameNum, frameVal, imgShow, imgData
    imgData = []
    for imgPath in path:
        imgData.append(Image.open(imgPath).convert("RGBA"))
    frameNum = len(imgData)
    frameVal = 0
    imgShow = copy.deepcopy(imgData)
    return imgData[0].size, len(imgData)
def gifGet(path):
    global frameNum, frameVal, imgShow, imgData
    imgData = []
    gifSrc = Image.open(path,'r')
    for frame in ImageSequence.Iterator(gifSrc):
        imgData.append(frame.convert('RGBA'))
    frameNum = len(imgData)
    frameVal = 0
    imgShow = copy.deepcopy(imgData)
    return ( imgData[0].size, len(imgData) )
# gif读取，返回 序列尺寸 和 序列帧数
def imgGetback():
    global frameNum, frameVal, imgShow, imgData
    imgShow = copy.deepcopy(imgData)
    frameNum = len(imgShow)
    frameVal = 0
    return imgData[0].size[0], imgData[0].size[1]
# 还原图像至最初导入状态
def imgResize(width, height):
    global imgData, imgShow
    width = int(width)
    height = int(height)
    for i in range(frameNum):
        imgShow[i] = imgData[i].copy().resize((width, height), Image.Resampling.NEAREST)
# 图像尺寸更改
def imgGray():
    global graySwitch, imgShow, imgData
    if graySwitch:
        graySwitch = False
        for i in range(len(imgShow)):
            imgShow[i] = imgData[i].copy().resize((imgShow[i].size[0], imgShow[i].size[1]))
    else:
        graySwitch = True
        for i in range(len(imgShow)):
            for w in range(imgShow[i].size[0]):
                for h in range(imgShow[i].size[1]):
                    pix = imgShow[i].getpixel((w, h))
                    avr = int((pix[0] * 0.3 + pix[1] * 0.59 + pix[2] * 0.11))
                    if pix[3] < alphaSet:
                        imgShow[i].putpixel((w, h), (avr, avr, avr, 0))
                    else:
                        imgShow[i].putpixel((w, h), (avr, avr, avr, pix[3]))
    return
# 生成灰度图                              |imgIn:图像        |return:灰度图像
# endregion
# 函数们