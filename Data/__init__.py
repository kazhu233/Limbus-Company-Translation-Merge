import os
from configparser import ConfigParser

CURRENT_PATH = os.getcwd()
conf = ConfigParser()
config_path = os.path.join(CURRENT_PATH, "config.conf")
conf.read(config_path, encoding="utf-8-sig")


# 获取游戏路径
need_game_path = True
if conf["PATH"]["GAME_PATH"].strip().strip('"'):
    GAME_PATH = conf.get("PATH", "GAME_PATH").strip().strip('"')
    if not os.path.exists(os.path.join(GAME_PATH, "LimbusCompany.exe")):
        need_game_path = False
if need_game_path:
    index = CURRENT_PATH.rfind("\\")
    check_path = os.path.join(CURRENT_PATH[:index:], "LimbusCompany.exe")
    if os.path.exists(check_path):
        GAME_PATH = CURRENT_PATH[:index:]
    else:
        input_flag = False
        while input_flag:
            input_path = input("请输入游戏根目录路径:").strip().strip('"')
            if input_path:
                normalized_path = os.path.normpath(input_path)
                if os.path.isabs(normalized_path):
                    check_path = os.path.join(normalized_path, "LimbusCompany.exe")
                    if os.path.exists(check_path):
                        GAME_PATH = normalized_path
                        input_flag = True
                        continue
                    else:
                        print('Error: 该目标目录下无法找到文件 "LimbusCompany.exe"\n\n')
                else:
                    print("\nError: 路径输入错误!\n")
            else:
                print("\nError: 路径不能为空!\n")
    conf.set("PATH", "GAME_PATH", f'"{GAME_PATH}"')
    with open(
        config_path,
        "w",
        encoding="utf-8-sig",
    ) as f:
        conf.write(f)

# 路径配置
if conf["CONF"]["LANG"]:
    LANG = conf.get("CONF", "LANG").strip('"').upper()
else:
    LANG = "JP"
if conf["CONF"]["TRANSLATION_NAME"]:
    TRANSLATION_NAME = conf.get("CONF", "TRANSLATION_NAME").strip('"')
else:
    TRANSLATION_NAME = "LLC_zh-CN"
if conf["CONF"]["SAFE_DIR"]:
    temp = conf.get("CONF", "SAFE_DIR").strip('"').strip().strip(",")
    SAFE_DIR = temp.split(",")
else:
    SAFE_DIR = ("Font", "Info")
LANG_PATH = os.path.join(
    GAME_PATH,
    "LimbusCompany_Data",
    "Assets",
    "Resources_moved",
    "Localize",
    LANG.lower(),
)
TRANSLATION_PATH = os.path.join(
    GAME_PATH, "LimbusCompany_Data", "Lang", TRANSLATION_NAME
)
CACHE_PATH = os.path.join(CURRENT_PATH, "Cache")
MERGE_PATH = os.path.join(CACHE_PATH, "merge")

# DEBUG配置
if conf["DEBUG"]["DEBUG"]:
    DEBUG = conf.getboolean("DEBUG", "DEBUG")
    LIST_DISPLAY_COUNT = conf.getint("DEBUG", "LIST_DISPLAY_COUNT")
else:
    DEBUG = False

# 包含参数
# DEBUG - DEBUG模式
# LIST_DISPLAY_COUNT - DEBUG模式下列表显示数量
# CURRENT_PATH - 工具运行路径
# GAME_PATH - 游戏根目录
# LANG_PATH - 语言文件路径
# TRANSLATION_PATH - 翻译文件路径
# CACHE_PATH - 缓存路径
# MERGE_PATH - 合并后文件缓存位置
# SAFE_DIR - 排除目录

# 扫描期
lang_files = list()  # 原文文件
translation_flies = list()  # 翻译文件
each_files = list()  # 需要遍历的文件
missing_files = list()  # 缺少文件
compare_files = list()  # 完全文件
mismatch_data = list()  # 不匹配的数据
unprocessed_files = list()  # 未处理文件
empty_files = list()  # 空文件
error_files = list()  # 失败文件

# 转移期
transfer_files = list()
