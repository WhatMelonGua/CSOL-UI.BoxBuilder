# coding:utf-8
from os import path as Pa
import tkinter as tk
import time
import tkinter.messagebox as msg
import tkinter.filedialog as file
import App.Func_ImgDispose as Dispose
import App.Func_ImgShow as Show
import App.Func_ImgOut as Out
import App.threadHandle as threadHandle

'''app设置项目'''
#region
UpdateTime = 100
class ticker():
    def __init__(self):
        self.start = time.time()
    def getGap(self):
        return (time.time() - self.start)*1000
    def update(self):
        self.start = time.time()
    def destroy(self):
        del self
#计时器
def setUpdateTime():
        newWin = tk.Toplevel(mainWin)
        newWin.geometry("240x100+300+300")
        newWin.resizable(0, 0)
        newWin.title("软件设定")
        tip_label = tk.Label(newWin, text="设定图片更新速度 毫秒:",font=smFont)
        nVal_label = tk.Label(newWin, text="目前更新速率:"+str(int(UpdateTime)), font=smFont)
        num_Entry = tk.Entry(newWin, bd=1, width=18, font=textFont)
        def set():
            global UpdateTime
            if Out.exp(num_Entry.get()) == 'num':
                v = int(num_Entry.get())
                UpdateTime = v
                msg.showinfo("提示","更新速度已变更\n现在软件刷新速度为 "+str(v)+"ms 一次刷新\n（若设定时间过短导致电脑算力不足，则以您电脑的最快运行速度刷新）")
                newWin.destroy()
            else:
                msg.showerror("错误","请填写正确的数值格式，需为整数且大于0")
                return
        doBtn = tk.Button(newWin, width=12, text="设置更新项", font=smFont, command=set)
        tip_label.place(x=10, y=10)
        nVal_label.place(x=10, y=60)
        num_Entry.place(x=15, y=30)
        doBtn.place(x=140, y=60)
# 设置软件更新速率
def appShutDown():
    mainWin.destroy()
# 强制关闭软件
#endregion
'''窗口尺寸 及 字体预设'''
# region
title_mainWin = "UI.BoxBuilder - CSOL缔造者插件"
size_mainWin = "960x660+200+100"
size_canvas = (625,605)
bg_mainWin = "#efefef"
#基本UI参数
btnFont = ("",20,"")
titleFont = ("",10,"")
textFont = ("",16,"")
pathFont = ("",12,"")
smFont = ("",9,"")
setFont = ("",13,"")
#UI字体
# endregion
'''函数部分'''
# region
def selectBtn():
    global img_canvas
    imgPath = file.askopenfilename(title="请选择一个图像文件", filetypes=( [
        ("所有类型", "*.png"),("所有类型", "*.jpg"),("所有类型", "*.jpeg"),("所有类型", "*.bmp"),
        ("png图像文件", "*.png"),
        ("jpg图像文件", "*.jpg"),("jpg图像文件", "*.jpeg"),
        ("bmp位图", "*.bmp")] ) )
    if imgPath:
        size = Dispose.imgGet(imgPath)
        if size[0]*size[1] > 160000:
            msg.showwarning("警告","您选择的图片过大，若色彩复杂所创建的CSOL UI.Box将轻易超过1024导致游戏内绘制失效！")
        imgPath_tk.set(imgPath)
        width_tk.set(size[0])
        height_tk.set(size[1])
        Show.boxMult = 1
        boxMult_tk.set(1)
        comInit()
        Dispose.gifTicker = None
        selectInit()
        drawCode.set(True)
        drawActiveCode.set(True)
        mainWin.after(0, frameUpdate, None)
    else:
        msg.showerror("错误", "未选择图片")
    comInit()
# 打开img功能与tk直接绑定的上级函数
def grayBtn():
    Dispose.imgGray()
# 灰度图勾选变化时的绑定函数，包含imgShow的更新 和 简化
def comInit():
    Dispose.graySwitch = False
    c_gray.deselect()
# 还原灰度图和进度条
def selectInit():
    animateCode.set(False)
    drawCode.set(False)
    drawActiveCode.set(False)
    addDrawCode.set(False)
    fastAddCode.set(False)
# 导出设定初始化
def imgInit():
    sizeInit = Dispose.imgGetback()
    width_tk.set(sizeInit[0]), height_tk.set(sizeInit[1])
    Show.boxMult = 1
    boxMult_tk.set(1)
    comInit()
# 图像回退初始状态
def wheelSizeInit():
    Show.imgWheelSizeInit()
# 图像滚轮初始化，显示真实大小
def decreaseBox():
    if len(Dispose.imgShow) == 0:
        msg.showerror("错误", "未导入图片，无法进行优化！")
        return
    if threadHandle.outputTaskExit:
        msg.showerror("错误", "已有优化任务存在,若您执意停止，请重启软件")
    else:
        threadHandle.outputTaskExit = True
        simpleTask = threadHandle.threadCreate(Dispose.imgSimple, (Dispose.imgShow, ))
        simpleTask.setDaemon(True)
        simpleTask.start()
        answer = msg.askyesno("信息确认", "正在处理中，若有需要点 否 停止处理（优化完成前不建议点击 是）")
        if not answer:
            if threadHandle.outputTaskExit:
                threadHandle.threadKill(simpleTask.ident, SystemExit)
                threadHandle.outputTaskExit = False
                msg.showinfo("提醒", "已经停止本次优化")
            else:
                msg.showinfo("提醒","您上一次的图片优化已经完成，无需点击 否")
                pass
            return
        if answer:
            pass
# 优化减少box的按钮command绑定函数
def outputImg():
    fileTypes = [("Lua脚本",".lua"),("txt文件",".txt") ]
    outputPath = file.asksaveasfilename( filetypes=fileTypes, defaultextension=fileTypes )
    if outputPath == "":
        msg.showinfo("信息", "未命名文件，不导出代码")
        return
    else:
        pass
    varName = name_tk.get()
    pos = (x_tk.get(), y_tk.get())
    boxMult = boxMult_tk.get()
    typeList = (Out.exp(pos[0]), Out.exp(pos[1]), Out.exp(boxMult))
    if (varName == '' or Out.exp(varName) == 'var') and (typeList[0] != None) and (typeList[1] != None) and (typeList[2] != None):
        dataList = Out.boxAnalysis(Dispose.imgShow)
        outputContent = Out.boxData2UI( dataList, varName, pos, boxMult, (fastAddCode.get(), drawCode.get(), addDrawCode.get(), drawActiveCode.get(), animateCode.get()),Dispose.speed )
        Out.outputTxt(outputPath, outputContent)
        maxNum, boxNum = Out.boxCount(dataList)
        fileSize = Pa.getsize(outputPath)/1024
        msg.showinfo("提示", "数据代码已导出至以下路径：\n" + outputPath + "\n文件大小:" + str(round(fileSize,2)) + " Kb\n消耗Box数:" + str(boxNum) + "个\n最大消耗:" + str(maxNum) + "个 | 共消耗:"+str(sum(boxNum))+"个\n(CSOL中Box总数规定小于1024，若此数>1024，图片将在CSOL中失效)")
        if fileSize > 100:
            msg.showwarning("警告！","您的输出代码大小为："+str(round(fileSize,2))+" Kb\n已超出 CSOL允许的最大Lua脚本大小(100kb)，解决方案：\n1- 将数据分发至多个lua脚本中，CSOL允许导入最多10个，100kb以下的脚本\n2- 优化图像，减少色彩、Box用量或帧数\n3- 放弃导入")
    else:
        msg.showerror("错误", "请检查设定的[起始坐标、UI.Box变量名称前缀、Box整体放大倍数]三个输入框的内容\n "
                           "可能是由于以下几点原因引起：\n"
                           "·数值不规范\n 1- 起始坐标必须均为 整数 或 合法的变量名称\n2- UI.Box变量名称前缀 不符合Lua语言规范\n"
                           "3- Box整体放大倍数可为 小数 或 变量名称，若为数值则必须大于0\n\n"
                           "·变量名称 不符合Lua语言规范\n1- 应为 字母 或 _ 开头\n2- 除 _ 外不包含其他符号\n3- 非开头字符可以为数字、字母、_")
# 输出Lua脚本
# endregion
'''Gif批量操作函数'''
# region
def frameUpdate(e):
    global img_canvas, UpdateTime
    img_canvas = Show.imgUpdate(Dispose.imgShow[Dispose.frameVal], imgCanvas)
    if Dispose.gifTicker == None:
        pass
    else:
        add = int(Dispose.gifTicker.getGap() // Dispose.speed)
        if add > 0:
            Dispose.frameVal = (Dispose.frameVal+add) % Dispose.frameNum
            Dispose.gifTicker.update()
        else:
            pass
    mainWin.after(UpdateTime, frameUpdate, None)
# 图片动态显示更新函数
def gifImport():
    global img_canvas
    imgPath = file.askopenfilename(title="请选择一个gif图像文件", filetypes=([("动态图片", "*.gif")]))
    if imgPath:
        size, length = Dispose.gifGet(imgPath)
        if size[0] * size[1] > 160000:
            msg.showwarning("警告", "您选择的图片过大，若色彩复杂所创建的CSOL UI.Box将轻易超过1024导致游戏内绘制失效！")
        imgPath_tk.set(imgPath)
        width_tk.set(size[0])
        height_tk.set(size[1])
        Show.boxMult = 1
        boxMult_tk.set(1)
        comInit()
        Dispose.gifTicker = ticker()
        selectInit()
        animateCode.set(True)
        mainWin.after(0, frameUpdate, None)
    else:
        msg.showerror("错误", "未选择图片")
def imgsImport():
    global img_canvas
    imgPath = file.askopenfilenames(title="请选择一个gif图像文件", filetypes=([
        ("所有类型", "*.png"),("所有类型", "*.jpg"),("所有类型", "*.jpeg"),("所有类型", "*.bmp"),
        ("png图像文件", "*.png"),
        ("jpg图像文件", "*.jpg"),("jpg图像文件", "*.jpeg"),
        ("bmp位图", "*.bmp")]))
    if len(imgPath) > 0:
        size, length = Dispose.imgsGet(imgPath)
        if size[0] * size[1] > 160000:
            msg.showwarning("警告", "您选择的图片过大，若色彩复杂所创建的CSOL UI.Box将轻易超过1024导致游戏内绘制失效！")
        imgPath_tk.set(imgPath)
        width_tk.set(size[0])
        height_tk.set(size[1])
        Show.boxMult = 1
        boxMult_tk.set(1)
        comInit()
        Dispose.gifTicker = ticker()
        selectInit()
        addDrawCode.set(True)
        mainWin.after(0, frameUpdate, None)
    else:
        msg.showerror("错误", "未选择图片")
# 动图导入
def speedWin():
    global UpdateTime
    newWin = tk.Toplevel(mainWin)
    newWin.geometry("240x100+300+300")
    newWin.resizable(0, 0)
    newWin.title("动图播放速度")
    tip_label = tk.Label(newWin, text="设定播放速度 帧/秒:",font=smFont)
    nVal_label = tk.Label(newWin, text="目前播放速度:"+str(1000/Dispose.speed), font=smFont)
    num_Entry = tk.Entry(newWin, bd=1, width=18, font=textFont)
    def set():
        if Out.exp(num_Entry.get()) == 'num':
            v = 1000/float(num_Entry.get())
            Dispose.speedChange( v )
            msg.showinfo("提示","播放速度已变更")
            newWin.destroy()
        else:
            msg.showerror("错误","请填写正确的数值格式")
            return
    doBtn = tk.Button(newWin, width=12, text="设置播放速度", font=smFont, command=set)
    tip_label.place(x=10, y=10)
    nVal_label.place(x=10, y=60)
    num_Entry.place(x=15, y=30)
    doBtn.place(x=140, y=60)
# 通过Gif化来减少图片颜色
# endregion
'''外接窗口--设置'''
# region
def boxCreateF():
    global img_canvas
    newWin = tk.Toplevel(mainWin)
    newWin.geometry("260x110+300+300")
    newWin.resizable(0, 0)
    newWin.title("UI.Box快速创建")
    til_label = tk.Label(newWin, text="需要创建多少个Box？(请小于1024)", font=smFont)
    tip_label = tk.Label(newWin, text="[Box表导出名称为：变量前缀+_boxTable]", font=smFont)
    num_Entry = tk.Entry(newWin, bd=1, width=18, font=textFont)
    def create():
        fileTypes = [("Lua脚本", ".lua"), ("txt文件", ".txt")]
        outputPath = file.asksaveasfilename(filetypes=fileTypes, defaultextension=fileTypes)
        if outputPath == "":
            msg.showinfo("信息", "未命名文件，不导出代码")
            newWin.attributes("-topmost",1)
            return
        else:
            if Out.exp(num_Entry.get()) == 'num':
                boxNum = int(float(num_Entry.get()))
            else:
                msg.showerror("错误", "请填写正确的数值格式，需为整数")
                newWin.attributes("-topmost",1)
                return
            # 检查数字
            cont = str(name_tk.get()) + "_bT = {"
            for i in range(boxNum):
                t_sBox = ","
                if i == 0:
                    t_sBox = ""
                t_sBox += "UI.Box.Create()"
                cont += t_sBox
            cont += "}"
            # 创建box表
            Out.outputTxtStr(outputPath, cont)
            msg.showinfo("提示", "代码已导出至"+str(outputPath)+"！")
            newWin.destroy()
    doBtn = tk.Button(newWin, width=8, text="导出代码", font=smFont, command=create)
    til_label.place(x=10, y=10)
    tip_label.place(x=10, y=24)
    num_Entry.place(x=15, y=48)
    doBtn.place(x=180, y=80)
# 快捷创建UI.Box代码
def decreaseFrames():
    global img_canvas
    newWin = tk.Toplevel(mainWin)
    newWin.geometry("240x100+300+300")
    newWin.resizable(0, 0)
    newWin.title("颜色数目设定")
    tip_label = tk.Label(newWin, text="需要减少至多少帧？", font=smFont)
    val_label = tk.Label(newWin, text="目前帧数："+str(len(Dispose.imgShow)), font=smFont)
    num_Entry = tk.Entry(newWin, bd=1, width=18, font=textFont)
    def decrease():
        if Out.exp(num_Entry.get()) == 'num':
            frameNum = int(float(num_Entry.get()))
        else:
            msg.showerror("错误", "请填写正确的数值格式，需为整数")
            newWin.attributes("-topmost",1)
            return
        frameNumber = len(Dispose.imgShow)-1
        frameGap = frameNumber/(frameNum-1)
        newFrames = []
        for i in range(frameNum):
            newFrames.append(Dispose.imgShow[0+int(i*frameGap)])
        Dispose.imgShow = newFrames
        Dispose.frameNum = len(Dispose.imgShow)
        Dispose.frameVal = 0
        msg.showinfo("提示", "帧数已缩减")
        newWin.destroy()
    doBtn = tk.Button(newWin, width=8, text="减 帧", font=smFont, command=decrease)
    tip_label.place(x=10, y=10)
    val_label.place(x=10, y=60)
    num_Entry.place(x=15, y=30)
    doBtn.place(x=160, y=60)
# 动图减帧
def decreaseColor():
    global img_canvas
    newWin = tk.Toplevel(mainWin)
    newWin.geometry("240x100+300+300")
    newWin.resizable(0, 0)
    newWin.title("颜色数目设定")
    tip_label = tk.Label(newWin, text="需要保持颜色数目为[彩图推荐至少16]:",font=smFont)
    val_label = tk.Label(newWin, text="现有颜色:"+str(Out.colorCount(Dispose.imgShow)),font=smFont)
    num_Entry = tk.Entry(newWin, bd=1, width=18, font=textFont)
    def decrease():
        if Out.exp(num_Entry.get()) == 'num':
            colorNum = int(float(num_Entry.get()))
        else:
            msg.showerror("错误","请填写正确的数值格式，需为整数")
            newWin.attributes("-topmost",1)
            return
        Dispose.imgColorDecrease(colorNum)
        msg.showinfo("提示","减色已完成")
        newWin.destroy()
    doBtn = tk.Button(newWin, width=8, text="进行减色", font=smFont, command=decrease)
    tip_label.place(x=10, y=10)
    val_label.place(x=10, y=60)
    num_Entry.place(x=15, y=30)
    doBtn.place(x=160, y=60)
# 通过Gif化来减少图片颜色
def setSetter():
    newWin = tk.Toplevel(mainWin)
    newWin.geometry("360x280+300+300")
    newWin.resizable(0, 0)
    newWin.title("优化 阈值设置(处理像素的RGB最小相似度)")
    newWin.configure(bg=bg_mainWin)
    R_label = tk.Label(newWin, text="R|H 容 差", font=textFont)
    G_label = tk.Label(newWin, text="G|S  容 差", font=textFont)
    B_label = tk.Label(newWin, text="B|V  容 差", font=textFont)
    A_label = tk.Label(newWin, text="A  容 差", font=textFont)
    alpha_label = tk.Label(newWin, text="最小透明度", font=textFont)
    R_label.place(x=20, y=20)
    G_label.place(x=20, y=60)
    B_label.place(x=20, y=100)
    A_label.place(x=20, y=140)
    alpha_label.place(x=20, y=180)
    R_Entry = tk.Entry(newWin, bd=1, width=8, font=textFont)
    G_Entry = tk.Entry(newWin, bd=1, width=8, font=textFont)
    B_Entry = tk.Entry(newWin, bd=1, width=8, font=textFont)
    A_Entry = tk.Entry(newWin, bd=1, width=8, font=textFont)
    alpha_Entry = tk.Entry(newWin, bd=1, width=8, font=textFont)
    R_Entry.place(x=140, y=19)
    G_Entry.place(x=140, y=59)
    B_Entry.place(x=140, y=99)
    A_Entry.place(x=140, y=139)
    alpha_Entry.place(x=140, y=179)
    R_vArea = tk.Label(newWin, text="0 ~ 255", font=pathFont)
    G_vArea = tk.Label(newWin, text="0 ~ 255", font=pathFont)
    B_vArea = tk.Label(newWin, text="0 ~ 255", font=pathFont)
    A_vArea = tk.Label(newWin, text="0 ~ 255", font=pathFont)
    alpha_vArea = tk.Label(newWin, text="0 ~ 255", font=pathFont)
    R_vArea.place(x=240, y=18)
    G_vArea.place(x=240, y=58)
    B_vArea.place(x=240, y=99)
    A_vArea.place(x=240, y=139)
    alpha_vArea.place(x=240, y=179)
    def RGBAset():
        R, G, B, A, alpha, mode = Dispose.parmGet()
        if R_Entry.get():
            R =  int(R_Entry.get())
        if G_Entry.get():
            G = int(G_Entry.get())
        if B_Entry.get():
            B = int(B_Entry.get())
        if A_Entry.get():
            A = int(A_Entry.get())
        if alpha_Entry.get():
            alpha = int(alpha_Entry.get())
        Dispose.RGBAset(R, G, B, A, alpha)
        R, G, B, A, alpha, mode = Dispose.parmGet()
        if mode == 0:
            msg.showinfo("提示","阈值更改完毕，当前阈值\n"+"R:"+str(R)+"  G:"+str(G) + "  B:"+str(B) + "  A:"+str(A) + "\n"
                         + "最小透明度: " + str(alpha) + "（小于最小透明度的像素将直接清除）")
        elif mode == 1:
            msg.showinfo("提示", "阈值更改完毕，当前阈值\n" + "H:" + str(R) + "  S:" + str(G) + "  V:" + str(B) + "\n"
                         + "最小透明度: " + str(alpha) + "（小于最小透明度的像素将直接清除）")
        else:
            msg.showinfo("提示", "参数已设置，但目前您选择了不优化图像，点击 切换模式 按钮，至 RGB 或 HSV 模式方可生效")
        newWin.attributes("-topmost",1)
    def switchVector():
        switch = Dispose.switchVector()
        vector = "横向" if switch else "纵向"
        msg.showinfo("提示","Box优化方向已基于"+vector+"优化")
        newWin.attributes("-topmost",1)
    def switchMode():
        set = Dispose.switchMode()
        if set == 0:
            mode = 'RGB'
        elif set == 1:
            mode = 'HSV'
        else:
            mode = '取消近似色成块（不优化）'
        msg.showinfo("提示","优化模式已变成基于 "+mode+" 优化")
        newWin.attributes("-topmost",1)
    vSend = tk.Button(newWin, width=14, text="设置阈值", font=pathFont, command=RGBAset)
    modSet = tk.Button(newWin, width=10, text="切换模式", font=pathFont, command=switchMode)
    vecSet = tk.Button(newWin, width=10, text="切换方向", font=pathFont, command=switchVector)
    modSet.place(x=20,y=230)
    vecSet.place(x=120,y=230)
    vSend.place(x=220,y=230)
# RGBA与alpha优化设定窗口
def openIntro():
    global img_canvas
    newWin = tk.Toplevel(mainWin)
    newWin.geometry("320x100+300+300")
    newWin.resizable(0, 0)
    newWin.title("说明")
    global avatar
    avatar = tk.PhotoImage(file='./src/avatar.png')
    img_label = tk.Button(newWin, image=avatar)
    tip_label = tk.Label(newWin, text="欢迎关注B站 小受星", font=smFont)
    UID_Entry = tk.Entry(newWin, fg='red',width=16, font=pathFont)
    UID_Entry.insert(0,'UID:9539642')
    add_label = tk.Label(newWin, text="哔哩哔哩搜索输入框内容 查看教程视频", font=smFont)
    UID_Entry.configure(state='readonly')
    img_label.place(x=10, y=10)
    tip_label.place(x=86, y=10)
    UID_Entry.place(x=86, y=36)
    add_label.place(x=86, y=64)
    def trash():
        global avatar
        del avatar
        newWin.destroy()
    newWin.protocol("WM_DELETE_WINDOW", trash)
# endregion
'''事件绑定函数'''
# region
def resize(e):
    width_tk.set(int(width_tk.get())), height_tk.set(int(height_tk.get()))
    Dispose.imgResize(width_tk.get(), height_tk.get())
    comInit()
# 依据源图进行实际缩放
def boxMultSet(e):
    get = Entry_sizeBox.get()
    datatype = Out.exp(get)
    Show.multType = datatype
    if datatype == 'num':
        if float(get) < 0:
            boxMult_tk.set(1)
            Show.boxMult = float(boxMult_tk.get())
            msg.showerror("错误", "Box长宽至少不能小于0！")
        else:
            boxMult_tk.set( float(get) )
            Show.boxMult = float(boxMult_tk.get())
    elif datatype == 'var':
        boxMult_tk.set( str(get) )
        Show.boxMult = boxMult_tk.get()
    else:
        boxMult_tk.set(1)
        Show.boxMult = float(boxMult_tk.get())
        msg.showerror("错误", "设定的 变量名称 不符合Lua语言规范\n1- 应为 字母 或 _ 开头\n2- 除 _ 外不包含其他符号\n3- 非开头字符可以为数字、字母、_")
# Box倍数缩放设定
def wheelSize(e):
    global img_canvas
    Show.imgWheelSize(e.delta)
# 滚轮虚拟缩放图片
# endregion

# region
mainWin = tk.Tk()
mainWin.geometry(size_mainWin)
mainWin.resizable(0, 0)
mainWin.title(title_mainWin)
mainWin.iconbitmap('./src/UIBox.ico')
mainWin.configure(bg=bg_mainWin)
# endregion
# 主窗口声明
'''tk变换字串声明及初始化'''
# region
name_tk = tk.StringVar()                        # Lua数据变量前缀名称
boxMult_tk = tk.StringVar()                     # box的放大倍数
boxMult_tk.set(Show.boxMult)
imgPath_tk = tk.StringVar()                     # 图片的路径
width_tk = tk.StringVar()                       # 设置图片尺寸 宽
height_tk = tk.StringVar()                      # 设置图片尺寸 高
x_tk = tk.StringVar()                           # 在CSOL屏幕的 起始位置 x坐标
x_tk.set(0)
y_tk = tk.StringVar()                           # 在CSOL屏幕的 起始位置 y坐标
y_tk.set(0)
# endregion
# StringVar
# region
fastAddCode = tk.BooleanVar()
drawCode = tk.BooleanVar()
addDrawCode = tk.BooleanVar()
drawActiveCode = tk.BooleanVar()
animateCode = tk.BooleanVar()
# endregion
# 导出选项

# region
imgFrame = tk.Frame(mainWin, width=640, height=620, bg="#F6F6F6", bd=1, relief="groove")
sizeFrame = tk.Frame(mainWin, width=270, height=120, bd=1, relief="solid")
posFrame = tk.Frame(mainWin, width=270, height=120, bd=1, relief="solid")
# 块分区

inputBtn = tk.Button(mainWin, width=17, text="选 择 图 像", font=btnFont, command=selectBtn)
backBtn = tk.Button(mainWin, width=8, text="清除操作", font=smFont, command=imgInit)
info_Path = tk.Label(mainWin, text="文件路径：", font=pathFont)
imgPath = tk.Entry(mainWin, font=pathFont, width=30, textvariable=imgPath_tk)
imgCanvas = tk.Canvas(imgFrame, confine=False, width=size_canvas[0], height=size_canvas[1])
btn_trueSize = tk.Button(mainWin, width=8, text="实际尺寸", font=smFont, command=wheelSizeInit)

imgSizeTitle = tk.Label(sizeFrame, text="导出尺寸", font=titleFont, fg="#676767")
label_width = tk.Label(sizeFrame, text="图像宽度", font=textFont)
label_height = tk.Label(sizeFrame, text="图像高度", font=textFont)
label_pix1 = tk.Label(sizeFrame, text="像素", font=textFont)
label_pix2 = tk.Label(sizeFrame, text="像素", font=textFont)
Entry_width = tk.Entry(sizeFrame, bd=1, width=8, font=textFont, textvariable=width_tk)
Entry_height = tk.Entry(sizeFrame, bd=1, width=8, font=textFont, textvariable=height_tk)

posTitle = tk.Label(posFrame, text="起始坐标", font=titleFont, fg="#676767")
label_x = tk.Label(posFrame, text="x", font=textFont)
label_y = tk.Label(posFrame, text="y", font=textFont)
label_pix3 = tk.Label(posFrame, text="像素", font=textFont)
label_pix4 = tk.Label(posFrame, text="像素", font=textFont)
Entry_x = tk.Entry(posFrame, bd=1, width=8, font=textFont, textvariable=x_tk)
Entry_y = tk.Entry(posFrame, bd=1, width=8, font=textFont, textvariable=y_tk)

c_gray = tk.Checkbutton(mainWin, text="导出灰度图", font=textFont, command=grayBtn)

resampleBtn = tk.Button(mainWin, width=3, text="减\n色", font=setFont, command=decreaseColor)
correctBtn = tk.Button(mainWin, width=11, text="优 化 图 像", font=btnFont, command=decreaseBox)
setBtn = tk.Button(mainWin, width=3, text="设\n置", font=setFont, command=setSetter)
outputBtn = tk.Button(mainWin, width=17, text="导 出 代 码", font=btnFont, command=outputImg)


label_varName = tk.Label(mainWin, text="UI.Box变量前缀名称（防止重名）", font=titleFont)
Entry_varName = tk.Entry(mainWin, bd=1, width=8, font=textFont, textvariable=name_tk)

label_sizeBox = tk.Label(mainWin, text="Box整体放大倍数（整数或变量名称）", font=titleFont)
Entry_sizeBox = tk.Entry(mainWin, bd=1, width=8, font=textFont, textvariable=boxMult_tk)
# 功能组件

# endregion
# 组件声明

Entry_height.bind("<Return>", resize)
Entry_width.bind("<Return>", resize)
Entry_sizeBox.bind("<Return>", boxMultSet)
imgCanvas.bind("<MouseWheel>", wheelSize)
# 函数绑定

# region
imgFrame.place(x=10, y=10)
imgCanvas.place(x=5, y=5)
btn_trueSize.place(x=20,y=600)

inputBtn.place(x=680, y=10)
backBtn.place(x=870,y=68)
info_Path.place(x=678, y=70)
imgPath.place(x=680, y=100)
resampleBtn.place(x=680, y=510)
correctBtn.place(x=721, y=510)
setBtn.place(x=890,y=510)
outputBtn.place(x=680, y=570)

label_varName.place(x=680, y=400)
Entry_varName.place(x=680, y=420)
label_sizeBox.place(x=680, y=445)
Entry_sizeBox.place(x=680, y=465)
c_gray.place(x=800, y=460)

posFrame.place(x=670, y=130)
posTitle.place(x=5, y=5)
label_x.place(x=20, y=30)
label_y.place(x=20, y=80)
label_pix3.place(x=180, y=30)
label_pix4.place(x=180, y=80)
Entry_x.place(x=65, y=31)
Entry_y.place(x=65, y=81)

sizeFrame.place(x=670, y=270)
imgSizeTitle.place(x=5, y=5)
label_width.place(x=20, y=30)
label_height.place(x=20, y=80)
label_pix1.place(x=210, y=30)
label_pix2.place(x=210, y=80)
Entry_width.place(x=115, y=31)
Entry_height.place(x=115, y=81)
# endregion
# 组件放置
# region
menuBar = tk.Menu(mainWin, background='red',fg='white')
editMenu = tk.Menu(menuBar, tearoff=0)  # 第一菜单 软件设置
menuBar.add_cascade(label='设置', menu=editMenu)
editMenu.add_command(label='设置软件更新速率',command=setUpdateTime)
editMenu.add_separator()
editMenu.add_command(label='退出软件',command=appShutDown)
disposeMenu = tk.Menu(menuBar, tearoff=0)   # 第二菜单  图片批处理
menuBar.add_cascade(label='批处理', menu=disposeMenu)
disposeMenu.add_cascade(label='快捷代码(创建UI.Box)', command=boxCreateF)
disposeMenu.add_command(label='多图导入', command=imgsImport)
disposeMenu.add_command(label='动图导入', command=gifImport)
disposeMenu.add_separator()
disposeMenu.add_command(label="播放设置", command=speedWin)
disposeMenu.add_command(label="减帧", command=decreaseFrames)
exportMenu = tk.Menu(menuBar,tearoff=0)
menuBar.add_cascade(label='导出设置',menu=exportMenu)
exportMenu.add_checkbutton(label='支持色彩偏移计算方法', variable=fastAddCode)
exportMenu.add_checkbutton(label='添加便捷绘制函数', variable=drawCode)
exportMenu.add_checkbutton(label='添加色彩进阶绘制函数', variable=addDrawCode)
exportMenu.add_checkbutton(label='首图绘制激活', variable=drawActiveCode)
exportMenu.add_checkbutton(label='添加动画激活', variable=animateCode)
menuBar.add_cascade(label='说明文档', command=openIntro)
mainWin.configure(menu=menuBar)
# endregion
# Menu
# region
img_canvas = Show.showInit('./src/Nil.png', imgCanvas)
# endregion
# 初始化
mainWin.mainloop()