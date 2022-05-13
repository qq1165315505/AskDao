# 完成主线任务
import threading

from data.taskdict import *
from opt import *

class ZX():
    def __init__(self,monitor,lock):
        self.times_qmx = 1
        self.times = 1
        self.__lock = lock  # 线程锁
        self.__opt = Opt(monitor)  # 装入模拟器
        self.guideDict = generate_picpath_dict("img\\guide")  # 指引图库
        self.generalDict = generate_picpath_dict("img\\general")  # 通用图像对应地址字典
        self.taskDictZX = get_taskDict_ZX()  # 主线任务字典
        self.taskDictYMD = get_taskDict_YMD()  # 妖魔道字典
    """
    1、操作层-底层：**************************************************************************
        """
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
        with self.__lock:
            return self.__opt.wait(path,doa,t,threshold)

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
        with self.__lock:
            return self.__opt.waits(paths,doa,t,threshold)

    def click(self,pos):
        """绝对坐标点击"""
        with self.__lock:
            return self.__opt.click(pos)

    def clickRel(self,pos):
        """
        点击,相对坐标
        :param pos:相对坐标
        :return: True or False
        """
        with self.__lock:
            return self.__opt.clickRel(pos)

    def multiWait(self, path, doa=9, t=300, threshold=0.8,option = 0):
        """
            多选项等待
            :param path: 待匹配选项
            :param doa: 点击方位
            :param t: 查找次数
            :param threshold: 阈值
            :param option:需要的选项
            :return: True + pos or False + None
            """
        with self.__lock:
            return self.__opt.multiWait(path, doa, t, threshold, option)

    def swipe(self, loc, distance=200, direction="v"):
        """
            拖住滑动
            :param loc: 起始点
            :param distance: 滑动距离，正为向下滑动，负为向上滑动
            :param direction:
            :return: None
            """
        with self.__lock:
            self.__opt.swipe(loc,distance,direction)

    def clickPos(self,posKey):
        """
            获得点击坐标
            :return: 点击坐标点（默认随机）
            """
        with self.__lock:
            return self.__opt.clickPos(posKey)

    def taskVCR(self):
        """
        任务识别,返回任务编号
        :return: True + 任务编号，False + None
        """
        with self.__lock:
            text = self.__opt.taskVCR()
            print(text)
            for key,item in self.taskDict.items():
                if key in text:
                    for keyIn,textIn in item.items():
                        if textIn in text:
                            return keyIn
            return False



    """
    2、操作层：**************************************************************************
        """
    def waitTouch(self, path, doa=9, t=300, threshold=0.8):
        """
        等待图片出现并点击
        :param path: 图片路径
        :param doa: 方位。分10个维度：
                            0，1，2
                            3，4，5
                            6，7，8（矩阵位置）
        :param threshold: 阈值
        :return: True or False
        """
        with self.__lock:
            res = self.__opt.wait(path, doa, t, threshold)
            if res[0]:
                self.__opt.clickRel(res[1])
                return True
            return False

    def mWaitTouch(self, path, doa=9, t=300, threshold=0.8,option = 0):
        """
            多选项等待，找到最佳匹配点并点击
            :param path: 待匹配选项
            :param doa: 点击方位
            :param t: 查找次数
            :param threshold: 阈值
            :param option:需要的选项
            :return: True + pos or False + None
            """
        with self.__lock:
            res = self.__opt.multiWait(path, doa, t, threshold, option)
            if res[0]:
                self.__opt.clickRel(res[1])

    def taskFindClick(self, path,distance=200, threshold=0.8, doa=9, t=300, direction="v"):
        """
        任务查找并点击，找不到自动下滑查找
        :param loc: 起始点
        :param distance: 滑动距离，正为向下滑动，负为向上滑动
        :param direction:
        :param path: 图片路径
        :param doa: 方位。分10个维度：
                            0，1，2
                            3，4，5
                            6，7，8（矩阵位置）
        :param threshold: 阈值
        :return:True,Flase
        """
        Flag = False
        res = self.wait(path,doa,t,threshold)
        # 判断是否找到
        if res[0]:
            Flag = True
        else:
            pos = self.clickPos("task_win")
            self.swipe(pos,distance,direction)
            random_wait()
            res = self.wait(path, doa, t, threshold)
            # 判断是否找到
            if res[0]:
                Flag = True
        if Flag:
            self.clickRel(res[1])
            return True
        return False



    def posKeyTouch(self,posKey):
        """点击posKey"""
        with self.__lock:
            return self.__opt.posKeyTouch(posKey)

    def posInput(self,pos,text):
        """
            指定点输入数据
            :param pos: 数据输入点,相对坐标
            :param text: 输入内容
            :return:
            """
        with self.__lock:
            self.__opt.posInput(pos,text)
    """
    3、控制层-辅助：**************************************************************************
        """
    def close(self):
        """退出"""
        self.waitTouch(self.generalDict["close"])

    def yes(self):
        """确定"""
        self.waitTouch(self.generalDict["yes"])

    def jump(self,t = 300):
        """
        实现跳过
        :return:None
        """
        with self.__lock:
            res = self.__opt.wait(self.generalDict["jump"],t = t)
            if res[0]:
                time.sleep(1)
                res = self.__opt.wait(self.generalDict["jump"],t = t)
                self.__opt.clickRel(res[1])
                return True
            return False

    def waitZD(self):
        """
        等待战斗结束
        :return:
        """
        i = 1
        k = 30.0
        t = k
        while 1:
            time.sleep(int(t))
            res = self.wait(self.generalDict["zd"], t=2)
            if not res[0]:
                break
            i += 1
            t = ((k * i) ** (1 / i))
            print("再等待%d秒" % (int(t)))

    def randomWait(self,a = 1,b = 2):
        """随机等待，有战斗则延长"""
        random_wait(a, b)
        while 1:
            res = self.wait(self.generalDict["zd"], t=2)
            if not res[0]:
                return True
            time.sleep(3)

    """
    4、应用层-通用任务类：**************************************************************************
        """
    def action_shzh(self):
        """
        守护召唤
        :return:
        """
        res = self.wait(self.generalDict["shzh"],t=2)
        if res[0]:
            self.clickRel(res[1])
            self.randomWait(1,3)
            self.posKeyTouch("tipsBR_sh")
            self.yes()
            self.close()

    def action_qmx(self):
        """判断并打开驱魔香"""
        # 驱魔香判断
        self.posKeyTouch("winTopFun01")  # 打开巡逻
        # 判断是否打开，关闭则点击打开
        res = self.wait(self.generalDict["qmx_close"],t=2)
        if res[0]:
            self.posKeyTouch("xunLuo_qmx")  # 打开驱魔香
        self.close()  # 退出

    def action_1xslb(self):
        """
        新手礼包操作，第一次
        :return:
        """
        print("第一次新手礼包")
        res = self.wait(self.guideDict["xslb"])
        if res[0]:
            print("打开新手礼包")
            random_wait(3,5)
            self.posKeyTouch("tipsBR")
            random_wait(0.5,1)
            self.waitTouch(self.guideDict["xslb_lq"])
            random_wait(2, 3)
            self.posKeyTouch("tipsBR")
            random_wait(2,3)
            self.posKeyTouch("package")
            random_wait(2,3)
            self.posKeyTouch("package_11")
            # 判断第一个是否弹出装备，若无则点击第二个
            res1 = self.wait(self.guideDict["xslb_zb2"],t=2)
            if not res1[0]:
                self.posKeyTouch("package_12")
                res2 = self.wait(self.guideDict["xslb_zb2"], t=2)
                if not res2[0]:
                    self.posKeyTouch("package_13")
            # 穿装备
            for i in range(4):
                self.waitTouch(self.guideDict["xslb_zb2"])
                time.sleep(1)
            self.close()

    def action_1shzh(self):
        """
        守护召唤
        :return:
        """
        res = self.wait(self.guideDict["shzh"])
        if res[0]:
            self.clickRel(res[1])
            random_wait(2,3)
            self.posKeyTouch("tipsBR_sh")
            random_wait(2, 3)
            self.posKeyTouch("tipsBR_sh_yes")
            self.close()

    def action_1shimen(self):
        """
        执行第一次师门任务，到达20级
        :return:
        """
        times = 1
        while 1:
            # 0 判断是否有确定按钮，有则点击，无则继续（规避驱魔香）
            if times == 1:
                self.waitTouch(self.generalDict["yes"], t=2)
                times += 1
            # 1、判断是否有新手礼包，有则退出
            res1 = self.wait(self.generalDict["xslb"], t=2)
            if res1[0]:
                print("到达20级")
                # 点击领取新手礼包
                self.posKeyTouch("tipsBR")
                random_wait(4,6)
                self.waitTouch(self.guideDict["xslb_lq"])
                # 守护召唤
                self.action_shzh()
                # 关闭角色提示
                self.posKeyTouch("role")
                self.close()
                # 开始装备武器
                self.randomWait(2, 3)
                self.posKeyTouch("package")
                random_wait()
                self.posKeyTouch("package_12")
                for i in range(7):
                    self.waitTouch(self.guideDict["xslb_zb2"])  # 装备
                    time.sleep(1)
                # 手镯左右手装备
                self.waitTouch(self.guideDict["xslb_zb2_left"])  # 装备
                random_wait()
                self.posKeyTouch("package_23")
                self.waitTouch(self.guideDict["xslb_zb2"])  # 装备
                self.waitTouch(self.guideDict["xslb_zb2_right"])  # 装备
                random_wait()
                self.posKeyTouch("package_zl")
                random_wait()
                self.close()
                return True
            # 2、判断是否有师门任务，无则退出
            self.randomWait()
            # 2-1、点击任务
            self.waitTouch(self.generalDict["renwu"])
            # 2-2、判断是否有师门，有则点击，无则退出
            res2 = self.waitTouch(self.generalDict["sm"], t=5)
            if not res2:
                print("师门任务已完成，退出程序")
                return True
            # 2-3、有师门，点击前往，并等待情况出现
            self.waitTouch(self.generalDict["renwu_qianwang"])
            # 等待巡航
            self.randomWait(10, 15)
            # 3、情况出现，任务判单，跳or对话框
            res3 = self.waits([self.generalDict["jump"],
                                    self.generalDict["dialog_sm"]], t=40)
            # 3-1、是否有情况，有则分类判断，无则结束，返回主循环
            if res3[0]:
                # 3-1-1、情况为等待跳过
                if res3[1] == "jump":
                    self.jump()
                    # 判断是否有战斗
                    res3_1_1 = self.wait(self.generalDict["zd"], t=2)
                    if res3_1_1[0]:
                        # 有战斗,则等待跳过
                        self.waitZD()
                        # 3-1_1_1、判断是否出现跳过或者直接出现游戏界面（任务）
                        res3_1_1_1 = self.waits([self.generalDict["jump"],
                                                      self.generalDict["renwu"]])
                        if res3_1_1_1[0]:
                            # 有情况
                            # 3-1-1-1-1为跳过
                            if res3_1_1_1[1] == "jump":
                                self.jump()
                            # 3-1-1-1-2无跳过
                            elif res3_1_1_1[1] == "renwu":
                                continue

                # 3-1-2、情况为对话框
                elif res3[1] == "dialog_sm":
                    self.waitTouch(self.generalDict["dialog_sm"])
                    # 3-1-2-1判断是否有战斗or跳过or结束
                    res3_1_2_1 = self.waits([self.generalDict["jump"],
                                                  self.generalDict["zd"],
                                                  self.generalDict["renwu"]])
                    if res3_1_2_1[0]:
                        # 有情况，分类判断
                        # 为跳过
                        if res3_1_2_1[1] == "jump":
                            self.jump()
                        # 为战斗
                        elif res3_1_2_1[1] == "zd":
                            # 有战斗,则等待跳过
                            self.waitZD()
                            # 判断是否出现跳过或者直接出现游戏界面（任务）
                            res3_1_2_1_1 = self.waits([self.generalDict["jump"],
                                                            self.generalDict["renwu"]])
                            if res3_1_2_1_1[0]:
                                # 有情况
                                # 3-1-1-1-1为跳过
                                if res3_1_2_1_1[1] == "jump":
                                    self.jump()
                                # 3-1-1-1-2无跳过
                                elif res3_1_2_1_1[1] == "renwu":
                                    continue
                        # 若无则重新进入循环
                        elif res3_1_2_1[1] == "renwu":
                            continue

    def action_ex000_23(self):
        """基础操作：任务-前往-判断是否有跳过,有则返回True,无则返回False"""
        random_wait(2,3)
        self.waitTouch(self.generalDict["renwu"])
        self.waitTouch(self.generalDict["renwu_qianwang"])
        return self.jump(4)

    def action_ex23(self):
        """任务20-29,23的恶作剧部分"""
        self.posKeyTouch("map")
        self.waitTouch(self.generalDict["ditu_xym"])  # 前往轩辕庙
        times_1 = 0  # 外循环次数
        times_2 = 0  # 内循环次数
        times_3 = 0  # 全局循环次数
        while times_3 < 12:
            ret = self.action_ex000_23()
            times_1 += 1
            # 如果找到跳过则返回TRUE，表示完成
            if ret:
                return True
            # 如果呼叫3次仍然未完成任务则准备切换地图，进入第二层循环
            if times_1 > 3:
                while times_3 < 12:
                    times_2 += 1
                    self.posKeyTouch("map")
                    self.waitTouch(self.generalDict["ditu_tyc"])  # 前往天墉城
                    ret = self.action_ex000_23()
                    # 如果找到跳过则返回TRUE，表示完成
                    if ret:
                        return True
                    if times_2 > 3:
                        # 若无则重新进入轩辕庙
                        times_1 = 0
                        times_2 = 0
                        break
            times_3 += 1
        print('程序循环失败，请手动操作，操作时间180秒')
        time.sleep(30)

    # 任务指引类
    def zy20(self):
        """20级除暴指引"""
        # 第一次
        self.waitTouch(self.generalDict["renwu"])
        res = self.waitTouch(self.guideDict["chubao"], t=10)
        if not res:
            self.close()
            return False
        self.waitTouch(self.generalDict["renwu_qianwang"])
        random_wait(5, 8)
        self.mWaitTouch(self.guideDict["dialog"])
        self.jump()
        # 指引
        random_wait(2, 3)
        # 点击巡逻
        self.posKeyTouch("winTopFun01")
        # 点击开双
        random_wait()
        self.posKeyTouch("xunLuo_double")
        # 点击关闭
        random_wait()
        self.close()
        # 第二次
        self.waitTouch(self.generalDict["renwu"])
        self.waitTouch(self.generalDict["renwu_qianwang"])
        random_wait(5, 8)
        self.mWaitTouch(self.generalDict["dialog_chubao"])

    """
    副本1：妖魔道任务**************************************************************************
    """

    def run_ymd(self):
        """完成妖魔道任务"""
        # todo 妖魔道


    """
    5、应用层-动作集：**************************************************************************
        action000:任务-主线
        action001:前往-跳过
        action002:前往-【对话框】-跳过
        action003:前往-跳过-战斗-跳过
        action004:前往-【对话框】-跳过-战斗-跳过
        action005:前往-跳过-【对话框】-战斗-跳过
    """
    def action000(self,taskKey = "zhuxian"):
        """
        任务-主线or妖魔道识别
        :return:
        """
        self.randomWait(3,5)
        # 1、点击任务
        self.wait(self.generalDict["renwu"])
        self.posKeyTouch("task")
        # 2、寻找并点击任务
        if self.times == 1:
            self.taskFindClick(self.generalDict[taskKey])
            self.times += 1
        # 3、图像识别，判断任务
        for i in range(10):
            res = self.taskVCR()
            if res:
                break
            else:
                raise Exception("图像识别失败，请检查错误原因！代码行474")
        if taskKey == "zhuxian":
            return 1,res
        else:
            return 2,res

    def action001(self):
        """
        前往-跳过
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5,8)
        self.jump()

    def action002(self):
        """
        前往-【对话框】-跳过
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5,10)
        self.mWaitTouch(self.generalDict["dialog_zhuxian"])
        self.jump()

    def action003(self):
        """
        前往-跳过-战斗-跳过
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5,10)
        self.jump()
        self.waitZD()
        self.jump()

    def action004(self):
        """
        前往-【对话框】-跳过-战斗-跳过
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5, 10)
        self.mWaitTouch(self.generalDict["dialog_zhuxian"])
        self.jump()
        self.waitZD()
        self.jump()

    def action005(self):
        """
        前往-跳过-【对话框】-战斗-跳过
        :return:
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5, 10)
        self.jump()
        self.mWaitTouch(self.generalDict["dialog_zhuxian"])
        self.waitZD()
        self.jump()

    def action006(self):
        """
        前往-【对话框】
        :return:
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5, 10)
        self.mWaitTouch(self.generalDict["dialog_zhuxian"])

    def action007(self):
        """
        基础操作：前往-【对话框】-战斗-跳过
        :return:
        """
        self.waitTouch(self.generalDict["renwu_qianwang"])
        self.randomWait(5, 10)
        self.mWaitTouch(self.generalDict["dialog_zhuxian"])
        self.waitZD()
        self.jump()  # 跳过


    """
    6、行动层：**************************************************************************
        action000:任务-主线
        action001:前往-跳过
        action002:前往-【对话框】-跳过
        action003:前往-跳过-战斗-跳过
        action004:前往-【对话框】-跳过-战斗-跳过
        action005:前往-跳过-【对话框】-战斗-跳过
    """
    def actions_zx(self,res):
        """
        任务识别并执行-主线
        :param res: 任务编号或者False
        :return: 执行任务返回True
        """
        if res:
            print("当前识别主线任务编号为：", res)
            if res > 33:
                self.action_shzh()
            # 通用任务动作
            if res in [7,12,16,17,18,25,27,30,40,43,64,66,67,]:
                print('正在执行任务***********************：', res)
                self.action001()
                print('任务完成***************************：', res)
            elif res in [5,6,8,9,10,13,14,19,21,24,26,29,31,32,34,36,38,44,45,48,
                         51,52,53,54,55,58,60,61,63,70,71,75,76,77,78,79,80,81,62,
                         ]:
                print('正在执行任务***********************：', res)
                self.action002()
                if res in [70,71]:
                    random_wait(4,6)

                print('任务完成***************************：', res)
            elif res in [11,15,28,41,42,47,35,
                         56,57,59,65,68,69,73,]:
                print('正在执行任务***********************：', res)
                self.action003()
                print('任务完成***************************：', res)
            elif res in [39,74]:
                print('正在执行任务***********************：', res)
                self.action004()
                print('任务完成***************************：', res)
            elif res in [54]:
                print('正在执行任务***********************：', res)
                self.action005()
                print('任务完成***************************：', res)
            elif res in [46]:
                print('正在执行任务***********************：', res)
                self.action006()
                print('任务完成***************************：', res)
            elif res in []:
                print('正在执行任务***********************：', res)
                self.action007()
                print('任务完成***************************：', res)
            # 特殊任务动作***************************************************
            elif res in [1]:
                print('正在执行任务***********************：', res)
                self.action002()
                random_wait()
                self.posKeyTouch("tipsBR")
                return True
                print('任务完成***************************：', res)
            elif res in [2]:
                print('正在执行任务***********************：', res)
                self.action002()
                random_wait(2,3)
                self.posKeyTouch("tipsBR")
                random_wait(2,3)
                self.posKeyTouch("tipsBR")
                print('任务完成***************************：', res)
            elif res in [3]:
                print('正在执行任务***********************：', res)
                self.action002()
                random_wait()
                self.waitTouch(self.generalDict["lingqu"])
                print('任务完成***************************：', res)
            elif res in [4]:
                print('正在执行任务***********************：', res)
                self.action002()
                random_wait(1, 3)
                self.posKeyTouch("zd_tg23")
                random_wait(1, 3)
                self.posKeyTouch("zd_tg23")
                random_wait(8, 12)
                self.posKeyTouch("zd_zd")
                random_wait(1, 3)
                self.jump()
                print('任务完成***************************：', res)
            elif res in [20]:
                print('正在执行任务***********************：', res)
                self.action001()
                self.action_1xslb()
                print('任务完成***************************：', res)
            elif res in [22]:
                print('正在执行任务***********************：', res)
                self.action002()
                # 加点学习
                self.waitTouch(self.guideDict["jiadian_gws"])
                self.waitTouch(self.guideDict["jiadian_gws_yes"])
                self.jump()
                random_wait()
                self.posKeyTouch("role")
                random_wait()
                self.posKeyTouch("role_jn")
                random_wait()
                self.posKeyTouch("role_jn_leverUp10")
                random_wait()
                self.posKeyTouch("role_jn_leverUp10")
                random_wait()
                self.posKeyTouch("role_close")
                print('任务完成***************************：', res)
            elif res in [23]:
                print('正在执行任务***********************：', res)
                self.action002()
                # 战斗指引
                random_wait()
                self.posKeyTouch("zd_faShu")
                random_wait()
                self.posKeyTouch("zd_faShu_l1_org")
                random_wait()
                self.posKeyTouch("zd_tg23")
                random_wait()
                self.posKeyTouch("zd_tg23")
                random_wait(10,15)
                self.posKeyTouch("zd_zd")
                # 等待完毕
                print('任务完成***************************：', res)
            elif res in [33]:
                print('正在执行任务***********************：', res)
                self.action002()
                self.action_1shzh()
                print('任务完成***************************：', res)
            elif res in [37]:
                print('正在执行任务***********************：', res)
                self.action002()
                # 师门指引
                random_wait(2, 3)
                self.posKeyTouch("winTopFun01")
                random_wait()
                self.posKeyTouch("huoDong_rw11")
                self.waitTouch(self.generalDict["dialog_shimen"])
                self.jump()
                print('任务完成***************************：', res)
            elif res in [50]:
                print('正在执行任务***********************：', res)
                self.action002()
                # 领取宠物
                self.waitTouch(self.generalDict["lingqu"])
                self.jump()
                self.yes()
                random_wait()
                self.posKeyTouch("pet_cz")
                self.close()
                print('任务完成***************************：', res)
            elif res in [72]:
                print('正在执行任务***********************：', res)
                self.close()
                random_wait()
                self.action_ex23()
                random_wait(4, 5)
                print('任务完成***************************：', res)
            # 跳出去进行其他任务！
            elif res in [49]:
                print('正在执行任务***********************：', res)
                self.close()
                self.action_1shimen()
                print('任务完成***************************：', res)
            elif res in [82]:
                print('正在执行任务***********************：', res)
                self.close()
                self.zy20()
                self.run_ymd()
                print('任务完成***************************：', res)
            else:
                print("不是可识别任务！")
                return False
            if res > 50 and self.times_qmx == 1:
                self.action_qmx()
                self.times_qmx = 0
            return True
        print("不是可识别任务！")
        return False

    def actions_ymd(self,res):
        """
        任务识别并执行-妖魔道
        :param res: 任务编号或者False
        :return: 执行任务返回True
        """
        if res:
            self.action_shzh()
            # 通用任务动作
            if res in [2]:
                print('正在执行任务***********************：', res)
                self.action001()
                print('任务完成***************************：', res)
            elif res in [1,4]:
                print('正在执行任务***********************：', res)
                self.action002()
                print('任务完成***************************：', res)
            elif res in [3]:
                print('正在执行任务***********************：', res)
                self.action003()
                print('任务完成***************************：', res)
            elif res in []:
                print('正在执行任务***********************：', res)
                self.action004()
                print('任务完成***************************：', res)
            elif res in []:
                print('正在执行任务***********************：', res)
                self.action005()
                print('任务完成***************************：', res)
            elif res in []:
                print('正在执行任务***********************：', res)
                self.action006()
                print('任务完成***************************：', res)
            elif res in []:
                print('正在执行任务***********************：', res)
                self.action007()
                print('任务完成***************************：', res)
            else:
                print("该任务未编译")
            return True

    def run(self):
        Flag = True
        resStart = self.wait(self.generalDict["startRole"],t=5)
        if resStart[0]:
            self.startRole()
        while Flag:
            res = self.action000()
            if res[0] == 1:
                "主线任务"
                Flag = self.actions_zx(res[1])
            elif res[0] == 2:
                "妖魔道"
                Flag = self.actions_ymd(res[1])
        self.close()
        print("任务完成")

    def startRole(self):
        """启号"""
        self.posKeyTouch("role")
        self.posKeyTouch("role")
        self.posKeyTouch("role")
        self.posKeyTouch("role")
        random_wait()
        self.posKeyTouch("zd_faShu")
        random_wait()
        self.posKeyTouch("zd_faShu_f5")
        random_wait()
        self.posKeyTouch("zd_tg13")
        random_wait(20,25)
        self.posKeyTouch("zd_faShu")
        random_wait()
        self.posKeyTouch("zd_faShu_l1")
        random_wait()
        self.posKeyTouch("zd_tg13")
        random_wait(20,25)
        self.posKeyTouch("zd_faShu")
        random_wait()
        self.posKeyTouch("zd_faShu_f4")
        random_wait()
        self.posKeyTouch("zd_tg13")
        random_wait(15,20)
        self.posKeyTouch("zd_tg13")
        random_wait(15,20)
        self.jump()

if __name__ == "__main__":
    lock = threading.Lock()
    func = ZX("雷电模拟器",lock)
    func.run()







