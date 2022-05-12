# 操作问道游戏
from script.zhuxian import *

# class AskDao():
#     def __init__(self):



if __name__ == "__main__":
    lock = threading.Lock()
    func = ZX("雷电模拟器",lock)
    func.startRole()
    func.run()
    # func.actions(20)