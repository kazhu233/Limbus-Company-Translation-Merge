import os, json, shutil
import Data

lang_files = []
translation_files = []
merge_files = []
out_lang_files = []
out_translation_files = []


def ScanFiles(scanPath, target_list):
    target_list.clear()
    scan_lang_files = os.scandir(scanPath)
    for entry in scan_lang_files:
        if entry.is_file():
            if Data.LANG in entry.name:
                target_list.append(entry.name[3::])
            else:
                target_list.append(entry.name)
        elif entry.is_dir():
            scan_dir_files = os.scandir(entry.path)
            for entry2 in scan_dir_files:
                if Data.LANG in entry2.name:
                    target_list.append(os.path.join(entry.name, entry2.name[3::]))
                else:
                    target_list.append(os.path.join(entry.name, entry2.name))
    for i in range(len(target_list) - 1, -1, -1):
        for x in Data.SAFE_DIR:
            if x in target_list[i]:
                del target_list[i]


# 合并文件
def MergeFiles():
    CACHE_MERGE_PATH = os.path.join(Data.CACHE_PATH, "lang")
    if not os.path.exists(CACHE_MERGE_PATH):
        if Data.DEBUG:
            Data.debug("合并缓存目录不存在,自动创建... " + CACHE_MERGE_PATH)
        os.makedirs(CACHE_MERGE_PATH, exist_ok=True)
    # 遍历原文文件并合并入汉化文件中
    for file in lang_files:
        if file.endswith(".json"):
            lang_json = ""
            merge_json = ""
            lang_path = ""
            if "\\" in file:
                index = file.rfind("\\")
                lang_path = os.path.join(
                    Data.LANG_PATH, file[:index:], Data.LANG + "_" + file[index + 1 : :]
                )
            else:
                lang_path = os.path.join(Data.LANG_PATH, Data.LANG + "_" + file)
            merge_path = os.path.join(CACHE_MERGE_PATH, file)
            merge_dir = os.path.join(merge_path[: merge_path.rfind("\\") :])
            if not os.path.exists(merge_dir):
                if Data.DEBUG:
                    Data.debug("合并缓存目录不存在,自动创建... " + CACHE_MERGE_PATH)
                os.makedirs(merge_dir, exist_ok=True)
            if Data.DEBUG:
                Data.debug("开始处理文件: " + file)
            # 从原文获取数据
            with open(lang_path, "r", encoding="utf-8-sig") as f:
                lang_json = json.load(f)
            # 判断该文件是否拥有对应的翻译文件
            if lang_json:
                if file in translation_files:
                    # 如果有则获取对应的翻译文件并将新增原文添加进去
                    translation_path = os.path.join(Data.TRANSLATION_PATH, file)
                    with open(translation_path, "r", encoding="utf-8-sig") as f:
                        merge_json = json.load(f)
                    id_list = list()
                    if "dataList" in merge_json:
                        if lang_json["dataList"]:
                            if lang_json["dataList"][0]:
                                for item in merge_json["dataList"]:
                                    if "id" in item:
                                        id_list.append(item["id"])
                                for item in lang_json["dataList"]:
                                    if "id" in item:
                                        if item["id"] not in id_list:
                                            merge_json["dataList"].append(item)
                                            if Data.DEBUG:
                                                Data.debug(
                                                    "当前原文物品: "
                                                    + str(item)
                                                    + " 不存在，合并!"
                                                )
                                    else:
                                        if Data.DEBUG:
                                            Data.debug("id不存在,不管")
                            else:
                                if Data.DEBUG:
                                    Data.debug("无数据,跳过")
                        else:
                            if Data.DEBUG:
                                Data.debug("无数据,跳过")

                    else:
                        if lang_json:
                            if lang_json[0]:
                                for item in merge_json:
                                    if "id" in item:
                                        id_list.append(item["id"])
                                for item in lang_json:
                                    if "id" in item:
                                        if item["id"] not in id_list:
                                            merge_json.append(item)
                                    else:
                                        if Data.DEBUG:
                                            Data.debug("id不存在,不管")
                    if Data.DEBUG:
                        Data.debug("合并完成")
                else:
                    # 如果没有则直接复制原文
                    merge_json = lang_json
                    if Data.DEBUG:
                        Data.debug("无对应翻译文件,使用原文")
                with open(merge_path, "w", encoding="utf-8-sig") as f:
                    json.dump(merge_json, f, ensure_ascii=False, indent=4)
                merge_files.append(file)
                if Data.DEBUG:
                    Data.debug("结束处理文件: " + file)
            else:
                if Data.DEBUG:
                    Data.debug("空文件,不管")
                    Data.debug("结束处理文件: " + file)

    Data.log("合并文件迁移中...")
    Data.log("语言文件数量: " + str(len(lang_files)))
    Data.log("翻译文件数量: " + str(len(translation_files)))
    Data.log("迁移文件数量: " + str(len(merge_files)))
    # 遍历汉化文件，查询出未迁移文件
    for i in translation_files:
        if i in merge_files:
            continue
        else:
            out_translation_files.append(i)

    # 遍历原文件，查询出未迁移文件
    for i in lang_files:
        if i in merge_files:
            continue
        else:
            out_lang_files.append(i)

    if Data.DEBUG:
        Data.debug("未迁移语言文件: \n" + str(out_lang_files[: Data.LIST_COUNT]))
        Data.debug("未迁移汉化文件: \n" + str(out_translation_files[: Data.LIST_COUNT]))

    continue_files = list()
    out_second_files = list()

    # 后续迁移翻译文件
    for file in out_translation_files:
        original_path = os.path.join(Data.TRANSLATION_PATH, file)
        target_dir = os.path.join(CACHE_MERGE_PATH, file, "..")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        shutil.copy2(
            original_path,
            target_dir,
        )
        continue_files.append(file)
        merge_files.append(file)

    # 后续迁移语言文件
    for file in out_lang_files:
        if file not in continue_files:
            if "\\" in file:
                index = file.rfind("\\")
                original_path = os.path.join(
                    Data.LANG_PATH, file[:index:], Data.LANG + "_" + file[index + 1 : :]
                )
            else:
                original_path = os.path.join(Data.LANG_PATH, Data.LANG + "_" + file)
            target_path = os.path.join(CACHE_MERGE_PATH, file)
            target_dir = os.path.join(target_path, "..")
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            shutil.copy2(
                original_path,
                target_path,
            )
            continue_files.append(file)
            merge_files.append(file)

    if Data.DEBUG:
        Data.debug("二次迁移中...")
    for file in out_lang_files:
        if file not in continue_files:
            out_second_files.append(file)
    for file in continue_files:
        if file not in continue_files:
            out_second_files.append(file)
    if Data.DEBUG:
        Data.debug("后续迁移文件: \n" + str(continue_files[: Data.LIST_COUNT]))
        Data.debug("后续迁移文件: \n" + str(continue_files[: Data.LIST_COUNT]))
        Data.debug("未迁移文件: \n" + str(out_second_files[: Data.LIST_COUNT]))


def MoveFile():
    CACHE_MERGE_PATH = os.path.join(Data.CACHE_PATH, "lang")
    for file in merge_files:
        original_path = os.path.join(CACHE_MERGE_PATH, file)
        target_path = os.path.join(Data.TRANSLATION_PATH, file)
        target_dir = os.path.join(target_path, "..")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        shutil.copy2(
            original_path,
            target_path,
        )


def Merge():
    Data.log("扫描文件中...")
    # 扫描语言文件
    ScanFiles(Data.LANG_PATH, lang_files)
    if lang_files.__len__() < 1:
        Data.error("扫描语言文件失败! + \n" + Data.LANG_PATH + "\n" + str(lang_files))
        return False
    if Data.DEBUG:
        Data.debug("语言文件列表: \n" + str(lang_files[: Data.LIST_COUNT]))
    # 扫描翻译文件
    ScanFiles(Data.TRANSLATION_PATH, translation_files)
    if translation_files.__len__() < 1:
        Data.error(
            "扫描语言文件失败! + \n"
            + Data.TRANSLATION_PATH
            + "\n"
            + str(translation_files)
        )
        return False
    if Data.DEBUG:
        Data.debug("翻译文件列表: \n" + str(translation_files[: Data.LIST_COUNT]))

    # 合并翻译
    Data.log("合并翻译中...")
    MergeFiles()

    # 迁移文件
    Data.log("迁移文件中...")
    MoveFile()
    Data.log("迁移完成!")
    Data.log("语言文件数量: " + str(len(lang_files)))
    Data.log("翻译文件数量: " + str(len(translation_files)))
    Data.log("迁移文件数量: " + str(len(merge_files)))
