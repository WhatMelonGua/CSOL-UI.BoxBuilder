# coding:utf-8
import threading
import inspect
import ctypes

outputTaskExit = False
tLock = threading.Lock()

# 清除线程
def threadKill(tid,exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def threadCreate(function,parm=()):
    return threading.Thread(target=function, args=parm)
