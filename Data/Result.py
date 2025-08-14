import time
import Data

# 报错用
def error(text):
    print(f"\n[{getTime()}]Error: {text}\n")


# 反馈用
def log(text):
    print(f"[{getTime()}]LOG: {text}")

def info(text):
    print(f"[{getTime()}]INFO: {text}")


# DEBUG用
def debug(text):
        print(f"[{getTime()}]DEBUG: {text}")


def debug_list(text, input_list):
        print(f"[{getTime()}]DEBUG: {text}")
        print(str(input_list[: Data.LIST_DISPLAY_COUNT :]))


# 获取时间戳
def getTime():
    return time.strftime("%H:%M:%S", time.localtime())
