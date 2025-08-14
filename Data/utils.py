import os,shutil
import Data


# 检查主目录
def CheckMainDir():
    Data.CURRENT_PATH = os.getcwd()
    if Data.GAME_NAME in Data.CURRENT_PATH:
        index = len(Data.GAME_NAME) + Data.CURRENT_PATH.find(Data.GAME_NAME)
        Data.GAME_PATH = Data.CURRENT_PATH[0:index]
        # 拼接语言目录
        Data.LANG_PATH = os.path.join(
            Data.GAME_PATH,
            "LimbusCompany_Data",
            "Assets",
            "Resources_moved",
            "Localize",
            Data.LANG.lower()
        )
        Data.LANG = Data.LANG.upper()
        # 拼接翻译目录
        Data.TRANSLATION_PATH = os.path.join(
            Data.GAME_PATH, "LimbusCompany_Data", 
            "Lang", 
            Data.TRANSLATION_NAME
        )
        # 拼接缓存目录
        Data.CACHE_PATH = os.path.join(
            Data.CURRENT_PATH,
            "Data",
            "Cache"
        )

        if Data.DEBUG:
            Data.debug("游戏目录: " + Data.GAME_PATH)
            Data.debug("语言目录: " + Data.LANG_PATH)
            Data.debug("翻译目录: " + Data.TRANSLATION_PATH)
            Data.debug("缓存目录: " + Data.CACHE_PATH)
        return True
    Data.error("工具未置于游戏目录下。")
    return False


# 检查翻译目录
def CheckTranslationDir():
    if os.path.exists(Data.LANG_PATH):
        if Data.DEBUG:
            Data.debug("语言目录存在")
        if os.path.exists(Data.TRANSLATION_PATH):
            if Data.DEBUG:
                Data.debug("翻译目录存在")
            return True
        print()
        Data.error("目标翻译目录不存在")
        return False
    Data.error("目标语言目录不存在")
    return False
