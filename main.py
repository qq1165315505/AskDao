# 操作问道游戏
from script.zhuxian import *

# class AskDao():
#     def __init__(self):



if __name__ == "__main__":
    Win_names = [
        '13152601989水',
        '18577338397金',
        '18878718654木',
        '18101825720木',
        '19121277181火',
    ]
    lock = threading.Lock()
    funcs = []
    tds = []
    for name in Win_names:
        funcs.append(ZX(name, lock))
    for func in funcs:
        td = threading.Thread(target=func.run)
        tds.append(td)
    for td in tds:
        td.start()
    for td in tds:
        td.join()