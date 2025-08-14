# 系统函数
import msvcrt;
# 自函数
from Data import utils,merge;

def run():
    if utils.CheckMainDir():
        if utils.CheckTranslationDir():
            merge.Merge()
    print("按下Enter键关闭此窗口...")
    msvcrt.getch()
