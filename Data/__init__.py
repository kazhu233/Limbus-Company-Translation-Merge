from .config import DEBUG,LANG,LIST_COUNT,SAFE_DIR
GAME_NAME = "Limbus Company"
TRANSLATION_NAME = "LLC_zh-CN"

CURRENT_PATH = ""
GAME_PATH = ""
LANG_PATH = ""
TRANSLATION_PATH = ""
CACHE_PATH = ""

# 报错用
def error(text):
    print("\nError: " + text + "\n")

# DEBUG用
def debug(text):
    print("DEBUG: " + text)

# 反馈用
def log(text):
    print("LOG: " + text)