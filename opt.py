# 游戏控制器
import random
import pyperclip
from general_pos import *
from my_utils import *

class Opt():
    def __init__(self,monitor):
        # 窗口句柄
        auto.FAILSAFE = False
        self.hwnd = self.get_handle(monitor)

    # 1、鼠标操作底层***********************************************************
    def get_handle(self, game_name):
        """得到窗口句柄,若无则raise错误"""

        handle = win32gui.FindWindow(0, game_name)
        if handle:
            return handle
        else:
            raise ValueError('查无次窗口,请检查窗口名称是否正确!')

    def click(self,pos):
        """
        点击
        :param pos:绝对坐标
        :return: True or False
        """
        set_ForegroundWin(self.hwnd)
        auto.leftClick(pos)
        auto.moveTo(0,0)

    def clickPos(self,posKey):
        """
        获得点击坐标
        :return: 点击坐标点（默认随机）
        """
        # 坐标生成器实例化
        Pos = GeneralPos(self.hwnd)
        return Pos.click_pos(posKey)

    def swipe(self, loc, distance=200, direction="v"):
        """
        拖住滑动
        :param loc: 起始点
        :param distance: 滑动距离，正为向下滑动，负为向上滑动
        :param direction:
        :return: None
        """
        # 获得绝对坐标
        (x, y, _, _) = get_window_rect(self.hwnd)
        wind_pos = (x,y)
        TG_loc = (wind_pos[0] + loc[0], wind_pos[1] + loc[1])
        auto.moveTo(TG_loc)
        if direction == "V" or direction == "v":
            # 竖直方向拖拽
            auto.dragRel(0, -distance,
                         duration=random.randint(3, 5) / 10)  # 第一个参数是左右移动像素值，第二个是上下
            auto.moveTo(0, 0)

        elif direction == "H" or direction == "h":
            # 水方向拖拽
            auto.dragRel(-distance, 0,
                         duration=random.randint(3, 5) / 10)  # 第一个参数是左右移动像素值，第二个是上下
            auto.moveTo(0, 0)

    def input(self,text):
        """
        输入内容
        :param text:
        :return:None
        """
        # 复制粘贴
        pyperclip.copy(text)
        pyperclip.paste()

    # 2、鼠标操作中间层***********************************************************

    def posKeyTouch(self,poskey):
        """点击posKey"""
        pos = self.clickPos(poskey)
        self.click(pos)
        return pos

    def clickRel(self,pos):
        """
        点击
        :param pos:相对坐标
        :return: True or False
        """
        (x,y,_,_) = get_window_rect(self.hwnd)
        absPos = (x+pos[0],y+pos[1])
        self.click(absPos)

    def posInput(self,pos,text):
        """
        指定点输入数据
        :param pos: 数据输入点,相对坐标
        :param text: 输入内容
        :return:
        """
        self.clickRel(pos)
        self.input(text)

    # 3、图像识别底层***********************************************************
    def winShot(self):
        """
        背景截图
        :return: cv2格式图片
        """
        for i in range(10):
            img,(x,y,w,h) = windShot(self.hwnd)
            # 把图片转换为单通道的灰度图
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 获取灰度图矩阵的行数和列数
            r, c = gray_img.shape[:2]
            piexs_sum = r * c  # 整个弧度图的像素个数为r*c

            # 获取偏暗的像素(表示0~19的灰度值为暗) 此处阈值可以修改
            dark_points = (gray_img < 5)
            target_array = gray_img[dark_points]
            dark_sum = target_array.size
            # 判断灰度值为暗的百分比
            dark_prop = dark_sum / (piexs_sum)
            if dark_prop >= 0.5:
                continue
            else:
                return img,(x,y,w,h)
        raise Exception("图像为黑色")

    def findPos(self,tempPath,threshold = 0.8):
        """
        找到图片坐标
        :return: True + Pos + (temp_w,temp_h) or False + None + None
        """


        # 循环找图，确保成功
        for i in range(10):
            # 1、获得背景图
            backImg, (_, _, _, h) = self.winShot()
            # 读取待匹配图片
            temp = cv2.imread(tempPath)
            temp = desize(temp, h)
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            (temp_h,temp_w) = temp.shape[:2]
            backImg = cv2.cvtColor(backImg,cv2.COLOR_BGR2GRAY)
            # 2.执行模板匹配
            result = cv2.matchTemplate(temp, backImg, cv2.TM_CCOEFF_NORMED)
            # 3.获得最佳匹配值
            _, ratio, _, pos = cv2.minMaxLoc(result)
            # 4.退出条件
            if ratio > threshold:
                # 找到最佳匹配点
                return [True, pos,(temp_w,temp_h)]
        # 失败匹配
        print('匹配失败，当前最佳相似度为：', ratio)
        return [False, None, None]

    def findPoses(self,tempPath,threshold = 0.8):
        """
        匹配单个图像，返回满足要求所有值
        :param tempPath:待匹配图片路径
        :param threshold:匹配阈值
        :return: 判断依据TRUE or False 以及 图片位置顶点坐标集合，Y轴为第一优先级，X轴为第二优先级
        """
        # 循环找图，确保成功
        for i in range(10):
            # 1、获得背景图
            backImg, (_, _, _, h) = self.winShot()
            # 读取待匹配图片
            temp = cv2.imread(tempPath)
            temp = desize(temp, h)
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            (temp_h, temp_w) = temp.shape[:2]
            backImg = cv2.cvtColor(backImg, cv2.COLOR_BGR2GRAY)
            # 2.执行模板匹配
            result = cv2.matchTemplate(temp, backImg, cv2.TM_CCOEFF_NORMED)
            # 3.获取模板匹配结果
            loc = np.where(result >= threshold)
            # 4.排序：从上到下
            loc_list = list(sorted(zip(*loc[::-1]), key=lambda a: a[1], reverse=False))
            lenth = len(loc_list)
            locs = loc_list.copy()
            if lenth >= 1:
                if lenth > 1:
                    # 删除重复区域
                    for i in range(lenth):
                        for j in range(i + 1, lenth):
                            if i != j:
                                distance = ((loc_list[i][0] - loc_list[j][0]) ** 2 +
                                            (loc_list[i][1] - loc_list[j][1]) ** 2) ** 0.5
                                if distance < 4:
                                    try:
                                        locs.remove(loc_list[i])
                                    except:
                                        continue
                print("点集合：", locs)
                return [True, locs, (temp_w,temp_h)]
            else:
                continue
        print("无匹配点，返回False")
        return [False, None, None]

    def findImgs(self, paths, threshold=0.8):
        """
                匹配多个图片，返回最佳匹配图片信息
                :param paths: 多个待匹配图路径
                :param threshold: 阈值
                :return: True+name+temp(w,h)+pos
                """
        # 循环找图，确保成功

        for i in range(10):
            # 图像匹配标识符
            FindFlag = False
            # 阈值
            max_ratio = threshold
            # 获得背景图
            backImg, (_, _, _, h) = self.winShot()
            backImg = cv2.cvtColor(backImg, cv2.COLOR_BGR2GRAY)
            for path in paths:
                # 1.读取待匹配图片
                temp = cv2.imread(path)
                temp = desize(temp, h)
                (temp_h,temp_w) = temp.shape[:2]
                temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
                # 2.执行模板匹配
                result = cv2.matchTemplate(temp, backImg, cv2.TM_CCOEFF_NORMED)
                # 3.获得最佳匹配值
                _, ratio, _, pos = cv2.minMaxLoc(result)
                # 4.退出条件
                if ratio > max_ratio:
                    FindFlag = True
                    max_ratio = ratio
                    max_name = os.path.basename(path)[:-4]
                    max_temp_wh = (temp_w, temp_h)
                    max_pos = pos
            if FindFlag:
                return [True,max_name,max_temp_wh,max_pos]
        # 10次任然没有找到，则复活False
        return [False, None, None, None]

    # 4、应用层底层***********************************************************
    def getNeedPos(self,pos,doa,temp_w,temp_h):
        """
        获得temp区域内指定位置坐标点
        :param pos: 顶点位置
        :param doa: 方位。分10个维度：
                            0，1，2
                            3，4，5
                            6，7，8（矩阵位置）
        参数9为随机位置
        :param temp_w: 图片宽度
        :param temp_h: 图片高度
        :return: doa所指定的点的坐标
        """
        if doa == 0:
            return pos

        elif doa == 1:
            return (pos[0]+int(temp_w/2),pos[1])

        elif doa == 2:
            return (pos[0] + temp_w, pos[1])

        elif doa == 3:
            return (pos[0], pos[1]+int(temp_h/2))

        elif doa == 4:
            return (pos[0]+int(temp_w/2), pos[1] + int(temp_h / 2))

        elif doa == 5:
            return (pos[0] + temp_w, pos[1] + int(temp_h / 2))

        elif doa == 6:
            return (pos[0], pos[1]+temp_h)

        elif doa == 7:
            return (pos[0]+int(temp_w/2), pos[1]+temp_h)

        elif doa == 8:
            return (pos[0] + temp_w, pos[1]+temp_h)

        else:
            # 随机位置
            x = pos[0] + random.randint(2,temp_w-2)
            y = pos[1] + random.randint(2, temp_h-2)
            return (x,y)

    # 5、应用层***********************************************************

    def wait(self, path, doa=9, t=300, threshold=0.8):
        """
        等待图片出现，有，返回True + pos,无，则返回False + pos
        :param path: 图片路径
        :param doa: 方位。分10个维度：
                            0，1，2
                            3，4，5
                            6，7，8（矩阵位置）
        :param threshold: 阈值
        :return: 有，返回True + pos + temp(w,h),无，则返回False + None + None
        """
        for i in range(t):
            res = self.findPos(path, threshold)
            # 2找到则点击并返回True+pos，未到找到则返False+None
            if res[0]:
                temp_w, temp_h = res[2]
                res[1] = self.getNeedPos(res[1], doa, temp_w, temp_h)
                return res
        return res

    def waits(self,paths, doa=9, t=300, threshold=0.8):
        """
               等待图片出现，有，返回True + pos,无，则返回False + pos
               :param paths: 图片路径集合
               :param doa: 方位。分10个维度：
                                   0，1，2
                                   3，4，5
                                   6，7，8（矩阵位置）
               :param threshold: 阈值
               :return: True+name+temp(w,h)+pos
               """
        # 图片处理与匹配
        for i in range(t):
            res = self.findImgs(paths, threshold)
            # 找到则点击并返回True+pos，未到找到则返False+None
            if res[0]:
                (temp_w, temp_h) = res[2]
                res[3] = self.getNeedPos(res[3], doa, temp_w, temp_h)
                return res
        return res

    def multiWait(self, path, doa=9, t=300, threshold=0.8,option = 0):
        """
        多选项等待
        :param path: 待匹配选项
        :param doa: 点击方位
        :param t: 查找次数
        :param threshold: 阈值
        :param Option:需要的选项
        :return: True + pos or False + None
        """
        for i in range(t):
            res = self.findPoses(path, threshold)
            # 2找到则点击并返回True+pos，未到找到则返False+None
            if res[0]:
                # option为从上到下选项，默认为第一个选项既0
                if option <= len(res[1])-1:
                    index = option
                else:
                    index = 0
                temp_w, temp_h = res[2]
                pos = self.getNeedPos(res[1][index], doa, temp_w, temp_h)
                return True,pos
        return False,None

    def taskVCR(self):
        """
        任务识别,返回任务内容
        :return: 任务内容
        """
        # 1、实际窗口
        (x, y, w, h) = get_window_rect(self.hwnd)
        # 2、游戏窗口
        h1 = h - 36
        w1 = int(960 / 540 * h1)
        x1 = 1
        y1 = 36
        # 3、任务窗口
        x2 = int(w1 * (3 / 8)) + x1
        y2 = int(h1 / 10) + y1
        w2 = int(w1 * 465 / 960)
        h2 = int(h1 * 190 / 540)
        # 4、截图
        imgRIO = windShots(self.hwnd,(x2,y2,w2,h2))
        # 5、文字识别
        test = ch_OCR(imgRIO)
        return test

if __name__ == "__main__":
    opt = Opt("雷电模拟器")
    opt.taskVCR()



