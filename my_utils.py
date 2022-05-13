# 通用api
import random
import time
import win32ui
import os
import cv2
import win32gui
import win32api,win32con,win32com,pythoncom
from paddleocr import PaddleOCR
import ctypes
from PIL import ImageGrab
from win32com.client import Dispatch

def ch_OCR(img_path):
    """
    文字识别
    :param img_path: 待识别图像
    :return: 识别文字
    """
    ocr = PaddleOCR(enable_mkldnn=True,use_tensorrt=True,use_angle_cls=False,use_gpu= False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    str = ""
    for line in result:
        str = str + line[-1][0]
    return str

def generate_picpath_dict(path):
    """
    :param path: 图片文件夹路径
    :return: 路径名称字典
    """
    picpath_dict = {}  # 设置待生产的图像路径空字典
    img_files = os.listdir(path)  # 获得所有图片名称
    for file_name in img_files:
        name = file_name[:-4]
        picpath_dict[name] = os.path.join(path, file_name)
    return picpath_dict

def cv_show(img):
    """显示图片"""
    cv2.imshow('test',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def random_wait(a = 1.0,b = 2.0):
    """
    随机等待，a,b时间之间
    :param a:
    :param b:
    :return:
    """
    time.sleep(random.randint(a*10,b*10)/10)

def get_all_win_name():
    """获取所有打开窗口名称"""
    hwnd_list = []
    win32gui.EnumWindows(lambda hwnd,param:param.append(hwnd),hwnd_list)
    print(hwnd_list)
    name_lists = [win32gui.GetWindowText(hwnd) for hwnd in hwnd_list]
    lists = []
    dicts = list(zip(name_lists,hwnd_list))
    for data in dicts:
        if "动产融资统一登记公示系统" in data[0]:
            lists.append(data)
    return lists

def set_ForegroundWin(hwnd):
    """设置指定窗口为当前窗口"""
    pythoncom.CoInitialize()
    shell = Dispatch("WScript.Shell")
    shell.SendKeys('^')
    win32gui.SetForegroundWindow(hwnd)

def get_window_rect(hwnd):
    """
    获得窗口坐标
    :param hwnd: 窗口句柄
    :return: (x,y,w,h)
    """
    set_ForegroundWin(hwnd)
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right-rect.left, rect.bottom-rect.top

def get_task_pos(hwnd):
    """
    获得任务窗口坐标
    :param hwnd: 句柄
    :return: (x,y,w,h)
    """
    # 1、实际窗口
    (x, y, w, h) = get_window_rect(hwnd)
    print("模拟器窗口", (x, y, w, h))
    img1 = ImageGrab.grab((x, y, x + w, y + h))
    img1.show("模拟器窗口")
    # 2、游戏窗口
    h1 = h - 36
    w1 = int(960/540 * h1)
    x1 = 1 + x
    y1 = 36 + y
    print("游戏窗口",(x1,y1,w1,h1))
    img2 = ImageGrab.grab((x1,y1,x1+w1,y1+h1))
    img2.show("游戏窗口")
    # 3、任务窗口
    x2 = int(w1*(3/8))+x1
    y2 = int(h1/10)+y1
    w2 = int(w1*465/960)
    h2 = int(h1*190/540)
    print("游戏截图", (x2, y2, w2, h2))
    img3 = ImageGrab.grab((x2, y2, x2+w2, y2+h2))
    img3.show("游戏截图")
    img3.save("jietu.png")
    print(ch_OCR("jietu.png"))
    os.remove("jietu.png")

def windShot(hwnd):
    """
    指定窗口截图
    :param hwnd:句柄
    :return: 窗口截图+(x,y,w,h)
    """
    (x,y,w,h) = get_window_rect(hwnd)
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, "screenshot.png")
    img_out = cv2.imread("screenshot.png")
    os.remove("screenshot.png")
    return img_out,(x,y,w,h)

def windShots(hwnd,rect):
    """
    指定窗口截图,带参数
    :param (x,y,w,h):截取区域Rect
    :param hwnd:句柄
    :return: 窗口截图+(x,y,w,h)
    """
    (x,y,w,h) = rect
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, "shot.png")
    img_out = cv2.imread("shot.png")
    os.remove("shot.png")
    return img_out

def desize(img,h):
    """
    修改尺寸
    :param w: 游戏屏幕尺寸
    :param img: cv2的图像格式
    :return: 修改后的图片
    """
    rate = (h-36)/540
    if rate == 1.0:
        return img
    else:
        (h,w) = img.shape[:2]
        (w,h) = (int(w*rate),int(h*rate))
        return cv2.resize(img,(w,h))





if __name__ == "__main__":
    hwnd = win32gui.FindWindow(0,"雷电模拟器")
    time.clock()
    windShot(hwnd)
    print(time.clock())


