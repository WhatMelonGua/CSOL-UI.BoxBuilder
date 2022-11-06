# coding:utf-8
import re
import numpy as np
from PIL import Image

def exp(txt):
    pat_var = '^([A-Z]|_)\w+'
    pat_num = '(\d+[.]\d+)|(\d+)'
    res = None
    get = re.fullmatch(pat_num, txt, re.I)
    if not get:
        get = re.fullmatch(pat_var, txt, re.I)
        if get:
            res = "var"
        else:
            res = None
    else:
        res = "num"
    return res
# 用于检验StringVar的类型，变量名or数字

'''声明导出用变量'''
# region
varName = ''
pos = (0, 0)
# endregion

'''块化导出函数'''
# region
def maskCreate(img:Image.Image):
    shape = (img.size[0], img.size[1], 1)
    mask = np.zeros(shape, np.uint8)
    return mask
# 创建colorMask 用于块分析
def colorList(imgData:Image.Image):
    color = []
    mask = []
    for w in range(imgData.size[0]):
        for h in range(imgData.size[1]):
            pix = imgData.getpixel((w,h))
            if pix[3] == 0:
                pass
            elif not pix in color:
                color.append(pix)
                singleMask = maskCreate(imgData)
                singleMask[w,h] = 1
                mask.append(singleMask)
            else:
                i = color.index(pix)
                mask[i][w,h] = 1
    return (color,mask)      # 返回 输出色板 与 半处理单色蒙版
# 创建色表用于输出 与 色表对应的Mask 用于后续分析处理
def colorToBox(color,Arr:np.ndarray):
    # cArr指 maskList中的 singleMask元素
    cArr = Arr.copy()
    index = 0
    boxData = []
    while index < len(cArr)-1:  #当index未遍历完，持续进行
        if 1 in cArr[index]:
            start = np.where(cArr[index] == 1)[0][0]
            vHLen = 1
            hWidth = []    # 存每个像素向下box高度
            while ( (start+vHLen) < len(cArr[index]) and cArr[index][start+vHLen][0] == 1):
                vHLen += 1
            for i in range(vHLen):    # 逐像素向下延伸
                hWLen = 1
                while ( (index+hWLen) < len(cArr) and cArr[index+hWLen][start+i][0] == 1 ):
                    hWLen += 1
                hWidth.append(hWLen)    # 竖向 单像素点 右延 的长度序列
            box = (index, start, min(hWidth), vHLen, color[0], color[1], color[2], color[3])    # box 创建 储存8个值，按顺序分别是 x, y, width, height, r, g, b, a
            boxData.append(box)
            # 清除区域
            cArr[index:index+min(hWidth), start:start+vHLen] = np.uint8(0)
            # 有 遗留未创建box的像素 继续处理
        else:
            # 全0后进入下一行
            index += 1
    return boxData
# Box数据存储输出，仅用于单个Mask对应color输出，若对图像处理，应搭配for循环遍历色表，以 颜色->Mask 一一输出
def boxAnalysis(imgData:Image.Image):
    img = imgData
    colorData = []
    boxData = []
    for frame in img:
        dataList = colorList(frame)
        colorData.append(dataList[0])
        singleBoxData = []          # 单张数据储存
        for color in range(len(dataList[0])):
            singleBoxData.append(colorToBox(dataList[0][color], dataList[1][color]))
        boxData.append(singleBoxData)
    return colorData, boxData
# 输出图像 对应色版 colors 的 boxData
def colorCount(frames):
    img = frames
    cNum = 0
    for frame in img:
        color = []
        for w in range(frame.size[0]):
            for h in range(frame.size[1]):
                pix = frame.getpixel((w, h))
                if pix[3] == 0:
                    pass
                elif not pix in color:
                    color.append(pix)
                else:
                    pass
        if cNum < len(color):
            cNum = len(color)
    return cNum
def boxCount(framesData):
    numList = []
    max = 0
    for frameBox in framesData[1]:
        num = 0
        for boxList in frameBox:
            num += len(boxList)
        if num > max:
            max = num
        numList.append(num)
    return max, numList
# Box计数，前提是colorToBox已经运行，才可知道 box 使用量          |boxData:指的是boxAnalysis返回值
def _fix(num):
    return int(round(num,0))
# 四舍五入快捷函数
def boxData2UI(boxData,name='',pos=(0,0),boxMult=1,funcSet=(False,False,False,False),speed=100):       # pos必须事先整型化，函数没内置！cj储存pos和box的信息，是int还是str,如（T，T，F），代表posX、posY是int，boxfactor是str
    name = str(name)
    colorList = boxData[0]
    boxList = boxData[1]
    maxNum,numList = boxCount(boxData)
    info = "--导出UI.Box表（一个表存储了一个图片的set信息）共"+str(len(colorList))+"个\n--分别占用Box数目为："+str(numList)+"\n--其中单图最大使用数为："+ str(maxNum)
    # 项目说明
    t_funcUse = []
    if funcSet[1] == True:  # 首图绘制函数添加
        t_funcUse.append("function _boxDraw(boxTable,setTable,pos,mult)\n"
                         "\t_boxUseNum = 0\n"
                         "\tfor index,set in pairs(setTable) do\n"
                         "\t\tboxTable[index]:Show()\n"
                         "\t\tboxTable[index]:Set({x=pos[1]+set[1]*mult,y=pos[2]+set[2]*mult,width=set[3]*mult,height=set[4]*mult,r=set[5],g=set[6],b=set[7],a=set[8]})\n"
                         "\tend\n"
                         "end\n\n")
    if funcSet[2] == True:  # 追加绘制函数添加
        t_funcUse.append("_boxUseNum = 0\n")
        t_funcUse.append("function _boxAddDraw(boxTable,setTable,pos,mult)\n"
                         "\tfor index,set in pairs(setTable) do\n"
                         "\t\tboxTable[index]:Show()\n"
                         "\t\tboxTable[index+_boxUseNum]:Set({x=pos[1]+set[1]*mult,y=pos[2]+set[2]*mult,width=set[3]*mult,height=set[4]*mult,r=set[5],g=set[6],b=set[7],a=set[8]})\n"
                         "\tend"
                         "\nend\n\n")
    if funcSet[4] == True:
        t_funcUse.append("_t_animAct="+str(speed/1000)+"\n"
                         "_anim_frameVal=1\n"
                         "_t_tick=0\n"
                         "function _AnimationImgList(boxTable,setList,pos,mult)\n"
                         "\t--确定前后帧的方块用量\n"
                         "\t_leftBox_Num = #setList[#setList]\n"
                         "\tif _anim_frameVal > 1 then\n"
                         "\t\t_leftBox_Num = #setList[_anim_frameVal-1]\n"
                         "\tend\n"
                         "\t_rightBox_Num = #setList[_anim_frameVal]+1\n"
                         "\t--绘制本帧\n"
                         "\tfor index,set in pairs(setList[_anim_frameVal]) do\n"
                         "\t\tboxTable[index]:Show()\n"
                         "\t\tboxTable[index]:Set({x=pos[1]+set[1]*mult,y=pos[2]+set[2]*mult,width=set[3]*mult,height=set[4]*mult,r=set[5],g=set[6],b=set[7],a=set[8]})\n"
                         "\tend\n\t--如若前帧比本帧调用UI.Box更多，则把多的部分Hide\n"
                         "\tif _leftBox_Num > _rightBox_Num then\n"
                         "\t\tfor index = _rightBox_Num,_leftBox_Num,1 do\n"
                         "\t\t\tboxTable[index]:Hide()\n"
                         "\t\tend\n"
                         "\tend\n"
                         "\t_anim_frameVal = (_anim_frameVal % #setList) + 1\n"
                         "end\n")
    # 功能函数
    t_colorTable = name + "_cT = {\n"
    for frame in range(len(colorList)):
        singleColor = ", {"
        if frame == 0:
            singleColor = " {"
        for color in range(len(colorList[frame])):
            t_sColor = ","
            if color == 0:
                t_sColor = ""
            t_sColor += "{" + str(colorList[frame][color][0]) + "," + str(colorList[frame][color][1]) + "," + str(colorList[frame][color][2]) + "," + str(colorList[frame][color][3]) + "}"
            singleColor += t_sColor
        singleColor += "}\n"
        t_colorTable += singleColor
    t_colorTable += " }"
    # 输出色表
    max, numList = boxCount(boxData)
    t_boxTable = name + "_bT = {"
    for i in range(max):
        t_sBox = ","
        if i == 0:
            t_sBox = ""
        t_sBox += "UI.Box.Create()"
        t_boxTable += t_sBox
    t_boxTable += "}"
    # 创建box表
    t_setTable = name + "_sT = {\n"
    for frame in range(len(boxList)):
        singleSet = ",{"
        if frame == 0:
            singleSet = " {"
        for box in range(len(boxList[frame])):
            for set in range(len(boxList[frame][box])):
                t_set = ","
                if box == 0 and set == 0:
                    t_set = ""
                t_set += "{" + str(boxList[frame][box][set][0]) + "," + str(boxList[frame][box][set][1]) + "," + str(boxList[frame][box][set][2]) + "," + str(boxList[frame][box][set][3]) + "," \
                         + name + "_cT[" + str(frame + 1) + "][" + str(box + 1) + "][1]" + "," + name + "_cT[" + str(frame + 1) + "][" + str(box + 1) + "][2]" + "," \
                         + name + "_cT[" + str(frame + 1) + "][" + str(box + 1) + "][3]" + "," + name + "_cT[" + str(frame + 1) + "][" + str(box + 1) + "][4]}"
                singleSet += t_set
        singleSet += "}\n"
        t_setTable += singleSet
    t_setTable += "}"
    # 创建set表
    t_act = []
    if funcSet[0] == True:  # 色彩偏移计算支持
        t_act.append("meta_add = {\n"
                         "\t__add = function(colorList,colorAdd)\n"
                         "\t\tres = {}\n"
                         "\t\tfor index,color in pairs(colorList) do\n"
                         "\t\t\tr = (color[1]+colorAdd[1])%255;g = (color[2]+colorAdd[2])%255;b = (color[3]+colorAdd[3])%255;a = color[4]+colorAdd[4]\n"
                         "\t\t\tif r < 0 then r = 255-r end if g < 0 then g = 255-g end if b < 0 then b = 255-b end if a > 255 then a = 255 end\n"
                         "\t\t\tres[index] = {r,g,b,a}\n"
                         "\t\tend\n"
                         "\t\treturn res\n"
                         "\tend\n"
                         "}\n")
        for i in range(len(colorList)):
            t_act.append("setmetatable(" + name + "_cT[" + str(i + 1) + "],meta_add)\n")
    if funcSet[3] == True:
        t_act.append("_boxDraw(" + name + "_bT," + name + "_sT[1],{" + str(pos[0]) + "," + str(pos[1]) + "}," + str(boxMult) + ")\n")
    if funcSet[4] == True:
        t_act.append("function UI.Event:OnUpdate(t)\n"
                     "\tif t - _t_tick > _t_animAct then\n"
                     "\t\t_t_tick = t\n"
                     "\t\t_AnimationImgList("+name+"_bT,"+name+"_sT,{" + str(pos[0]) + "," + str(pos[1]) + "}," + str(boxMult) + ")\n"
                     "\tend\n"
                     "end\n")
    return (info,t_funcUse,t_colorTable,t_boxTable,t_setTable,t_act)
# python数组转txt的Lua文本
def outputTxt(file:str,cont:tuple):
    with open(file, mode='w', encoding='utf-8') as outputFile:
        outputFile.write(cont[0])
        outputFile.write('\n\n')
        for func in cont[1]:
            outputFile.write(func)
        outputFile.write(cont[2])
        outputFile.write('\n\n')
        outputFile.write(cont[3])
        outputFile.write('\n\n')
        outputFile.write(cont[4])
        outputFile.write('\n\n')
        for act in cont[5]:
            outputFile.write(act)
# 输出到txt
def outputTxtStr(file,cont):
    with open(file, mode='w', encoding='utf-8') as outputFile:
        outputFile.write(cont)
# endregion
