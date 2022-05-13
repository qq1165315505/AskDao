# 问道常用功能键坐标

import pyautogui as auto
import numpy as np
from my_utils import *

class GeneralPos():
    def __init__(self,hwnd,random = True,rel = False):
        self.hwmd = hwnd
        (self.x,self.y,self.w,self.h) = get_window_rect(hwnd)
        (self.game_x,self.game_y,self.game_w,self.game_h) = self.get_game_rect()
        self.pos_dict = {
            # 游戏窗口顶端
            "map":(10,10,42,42),   # 地图
            "mapMin":(70,20,70,20),   # 小地图
            "line": (70, 45, 70, 15),  # 换线
            "winTopFun01":(176,6,48,48),  # 游戏界面顶部第一个按钮
            "xunLuo_qmx":(134,470,50,22),  # 巡逻-驱魔香
            "xunLuo_double": (266, 470, 50, 22),  # 巡逻-驱魔香
            "winTopFun02": (234, 6, 48, 48),  # 游戏界面顶部第二个按钮（刷道）
            "winTopFun03": (292, 6, 48, 48),  # 游戏界面顶部第三个按钮（活动）
            "huoDong_rw11": (466, 108, 60, 30),  # 巡逻-驱魔香
            "winTopFun04": (408, 6, 48, 48),  # 游戏界面顶部第四个按钮（待提升项目）
            # 宠物框
            "pet": (754, 2, 46, 46),  # 宠物
            "pet_cz": (384, 288, 94, 32),  # 宠物-参战
            # 角色选项
            "role":(856,2,52,52),  # 角色
            "role_sx": (842, 72, 32, 60),  # 属性
            "role_jd": (842, 162, 32, 60),  # 加点
            "role_jn": (842, 251, 32, 60),  # 技能
            "role_jn_leverUp1": (534, 470, 112, 34),  # 技能升1次
            "role_jn_leverUp10": (668, 470, 112, 34),  # 技能升10次
            "role_close":(796, 12, 32, 32),  # 角色界面退出
            # 游戏窗口左侧
            "winLeftFun04": (8, 236, 48, 48),  # 游戏界面左侧第4个按钮（more）

            # 游戏窗口右侧
            # 任务
            "task": (790, 84, 78, 28),  # 任务
            "team": (877, 84, 78, 28),  # 组队
            "team_create": (134, 460, 136, 36),  # 组队-创建队伍
            # 背包
            "package": (905, 410, 48, 48),  # 背包
            "package_zl": (700, 468, 112, 36),  # 整理背包
            # 背包-1层
            "package_11": (505, 112, 52, 52),  # 背包-格子11
            "package_12": (568, 112, 52, 52),  # 背包-格子12
            "package_13": (631, 112, 52, 52),  # 背包-格子13
            "package_14": (696, 112, 52, 52),  # 背包-格子14
            "package_15": (760, 112, 52, 52),  # 背包-格子15
            # 背包-2层
            "package_21": (505, 180, 52, 52),  # 背包-格子21
            "package_22": (568, 180, 52, 52),  # 背包-格子22
            "package_23": (631, 180, 52, 52),  # 背包-格子23
            "package_24": (696, 180, 52, 52),  # 背包-格子24
            "package_25": (760, 180, 52, 52),  # 背包-格子25
            # 背包-3层
            "package_31": (505, 248, 52, 52),  # 背包-格子31
            "package_32": (568, 248, 52, 52),  # 背包-格子32
            "package_33": (631, 248, 52, 52),  # 背包-格子33
            "package_34": (696, 248, 52, 52),  # 背包-格子34
            "package_35": (760, 248, 52, 52),  # 背包-格子35
            # 背包-4层
            "package_41": (505, 316, 52, 52),  # 背包-格子41
            "package_42": (568, 316, 52, 52),  # 背包-格子42
            "package_43": (631, 316, 52, 52),  # 背包-格子43
            "package_44": (696, 316, 52, 52),  # 背包-格子44
            "package_45": (760, 316, 52, 52),  # 背包-格子45
            # 背包-5层
            "package_51": (505, 384, 52, 52),  # 背包-格子51
            "package_52": (568, 384, 52, 52),  # 背包-格子52
            "package_53": (631, 384, 52, 52),  # 背包-格子53
            "package_54": (696, 384, 52, 52),  # 背包-格子54
            "package_55": (760, 384, 52, 52),  # 背包-格子55


            "more": (905, 472, 48, 48),  # 更多or展开
            "bangPai": (845, 472, 48, 48),  # 帮派
            # 打造分支
            "daZhao": (784, 472, 48, 48),  # 打造
            # 打造分支-装备
            "daZhao_zb": (784, 342, 48, 48),  # 打造-装备
            # 打造分支-首饰
            "daZhao_ss": (784, 404, 48, 48),  # 打造-首饰
            "daZhao_ss_yp": (130, 50, 140, 32),  # 打造-首饰-玉佩
            "daZhao_ss_yp35": (130, 100, 140, 32),  # 打造-首饰-玉佩-35级
            "daZhao_ss_xl": (130, 105, 140, 32),  # 打造-首饰-项链
            "daZhao_ss_xl35": (130, 155, 140, 32),  # 打造-首饰-项链-35级
            "daZhao_ss_sz": (130, 160, 140, 32),  # 打造-首饰-手镯
            "daZhao_ss_sz35": (130, 210, 140, 32),  # 打造-首饰-手镯-35级
            "daZhao_ss_hc": (648, 468, 118, 34),  # 打造-首饰-合成
            # 打造分支-装备拆分
            "daZhao_zb_cf": (840, 70, 36, 66),  # 打造-装备-拆分
            "daZhao_zb_lh": (840, 157, 36, 66),  # 打造-装备-炼化
            "daZhao_zb_lh_cz": (130, 56, 50, 50),  # 打造-装备-炼化-重组
            "daZhao_zb_lh_cz_zb": (566, 62, 50, 50),  # 打造-装备-炼化-重组-装备
            "daZhao_zb_lh_cz_zb_1": (387, 76, 50, 50),  # 打造-装备-炼化-重组-装备
            "daZhao_zb_lh_cz_hs1": (435, 188, 50, 50),  # 打造-装备-炼化-重组-黑水1
            "daZhao_zb_lh_cz_hs2": (571, 188, 50, 50),  # 打造-装备-炼化-重组-黑水2
            "daZhao_zb_lh_cz_hs3": (707, 188, 50, 50),  # 打造-装备-炼化-重组-黑水3
            "daZhao_zb_gz": (840, 245, 36, 66),  # 打造-装备-改造
            "daZhao_zb_gz_qd": (530, 466, 124, 40),  # 打造-装备-改造-确定
            # 好友栏
            "friend": (10, 388, 60, 36),  # 好友
            "friend_qunzhu": (10, 176, 58, 36),  # 好友-群主
            # 弹出提示装备
            "tipsBR":(786,418,82,30),  # 右下角提示
            # 守护召唤

            "tipsBR_sh": (706, 468, 114, 36),  # 右下角提示-守护召唤-召唤
            "tipsBR_sh_yes":(506, 302, 110, 34),  # 右下角提示-守护召唤-召唤-确定
            # 战斗
            "zd_tg11": (370, 102, 52, 52),  # 战斗-目标
            "zd_tg12": (308, 148, 52, 52),  # 战斗-目标
            "zd_tg13":(238,176,52,52),  # 战斗-目标
            "zd_tg14": (170, 232, 52, 52),  # 战斗-目标
            "zd_tg15": (104, 274, 52, 52),  # 战斗-目标
            "zd_tg23": (238, 210, 52, 52),  # 战斗-目标
            "zd_faShu": (895, 314, 45, 45),  # 战斗-法术
            # 战斗-低级法术
            # 前期法术
            "zd_faShu_l1_org": (671, 351, 50, 50),  # 战斗-力破-1阶
            # 法
            "zd_faShu_f1": (604, 282, 50, 50),  # 战斗-法术-1阶
            "zd_faShu_f2": (671, 282, 50, 50),  # 战斗-法术-2阶
            "zd_faShu_f3": (739, 282, 50, 50),  # 战斗-法术-3阶
            "zd_faShu_f4": (807, 282, 50, 50),  # 战斗-法术-4阶
            "zd_faShu_f5": (874, 282, 50, 50),  # 战斗-法术-5阶
            # 力
            "zd_faShu_l1": (604, 358, 50, 50),  # 战斗-力破-1阶
            "zd_faShu_l2": (671, 358, 50, 50),  # 战斗-力破-2阶
            "zd_faShu_l3": (739, 358, 50, 50),  # 战斗-力破-3阶
            "zd_faShu_l4": (807, 358, 50, 50),  # 战斗-力破-4阶
            "zd_faShu_l5": (874, 358, 50, 50),  # 战斗-力破-5阶
            # 战斗-道具
            "zd_daoJu": (895, 390, 45, 45),  # 战斗-道具
            # 战斗-自动
            "zd_zd": (895, 472, 45, 45),  # 战斗-自动
            # 任务窗口位置
            "task_win": (140, 200, 100, 60),  # 战斗-自动

        }
        self.random = random
        self.rel = rel


    def draw_rect(self):
        print("模拟器窗口坐标：", self.x, self.y, self.w, self.h)
        print("游戏窗口坐标：",self.game_x,self.game_y,self.game_w,self.game_h)
        safe_path = "game_shot.png"
        (x1, y1, w1, h1) = self.get_pos_model("task_win")
        print("相对坐标为：",(x1, y1, w1, h1))
        # 游戏窗口截屏
        set_ForegroundWin(self.hwmd)
        img_game = ImageGrab.grab((self.game_x,
                               self.game_y,
                               self.game_x + self.game_w,
                               self.game_y + self.game_h))
        # img_game.show("游戏窗口截屏")
        img_game.save(safe_path)
        img_cv = cv2.imread(safe_path)
        os.remove(safe_path)
        # 指定区域截图
        img_cv1 = img_cv.copy()
        img_cv1 = cv2.rectangle(img_cv1,(x1,y1),(x1+w1,y1+h1),255,1)
        cv_show(img_cv1)

    def get_game_rect(self):
        """
        获得游戏界面Rect
        :return: 游戏界面顶点绝对坐标，游戏界面长、宽：（x1,y1,w1,h1）
        """
        #游戏窗口
        h1 = self.h - 36
        w1 = int(960 / 540 * h1)
        x1 = 1 + self.x
        y1 = 36 + self.y
        return (x1,y1,w1,h1)

    def get_pos_model(self,Totem):
        """
        获得坐标"
        :param Totem:目标坐标key
        :param rect: 相对坐标，及w,h
        :param random: 是否随机坐标，True为随机,False为中间点坐标
        :param rel: True为相对坐标，False为绝对坐标
        :return: 地图绝对坐标or相对坐标
        """""
        (x,y,w,h) = self.pos_dict[Totem]
        # 绝对坐标
        if self.rel:
            x0 = 0
            y0 = 0
        # 相对坐标
        else:
            x0 = self.game_x
            y0 = self.game_y

        x1 = int(x/960*self.game_w + x0)
        y1 = int(y/540*self.game_h + y0)
        w1 = int(w/960*self.game_w)
        h1 = int(h/540*self.game_h)

        return (x1,y1,w1,h1)

    def click_pos(self,Totem):
        """
        获得点击坐标
        :param rect: 点击目标框
        :param rel: 是否为相对坐标
        :param random: 是否随机
        :return: 返回点击目标点
        """
        # 目标点Rect
        (x1,y1,w1,h1) = self.get_pos_model(Totem)
        if self.random:
            x = np.random.randint(x1+4,x1+w1-4)
            y = np.random.randint(y1+4,y1+h1-4)
        else:
            x = int(x1+w1/2)
            y = int(y1+h1/2)
        return (x,y)

if __name__ == "__main__":
    hwnd = win32gui.FindWindow(0,"18878718654木")
    Pos = GeneralPos(hwnd,rel=True)
    Pos.draw_rect()
