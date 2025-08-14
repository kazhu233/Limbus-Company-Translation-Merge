import os, json
import Data
from Data import Result, FileUtils


def loadJson(path):
    if not path.endswith(".json"):
        if Data.DEBUG:
            Result.debug(f"读取文件失败,后缀不包含json! {path}")
        return False
    if not os.path.exists(path):
        if Data.DEBUG:
            Result.debug(f"读取文件失败,文件不存在! {path}")
        return False
    json_data = ""
    with open(path, "r", encoding="utf-8-sig") as f:
        json_data = json.load(f)
    return json_data


def saveJson(path, json_data):
    if Data.DEBUG:
        Result.debug(f"正在保存json文件: {path}")
    with open(path, "w", encoding="utf-8-sig") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def mergeJson(file, data):
    path = os.path.join(Data.MERGE_PATH, file)
    if Data.DEBUG:
        Result.debug(f"正在合并json数据: {path}")
    if not os.path.exists(path):
        path2 = os.path.join(Data.TRANSLATION_PATH, file)
        path3 = os.path.join(Data.CACHE_PATH, "Translation", file)
        FileUtils.copyFile(path2, path)
        FileUtils.copyFile(path2, path3)
    json_data = loadJson(path)
    exists = any(data == data["id"] for data in json_data["dataList"])
    if exists:
        Result.debug("ID已存在,跳过")
        return False
    json_data["dataList"].append(data)
    saveJson(path, json_data)
    return True


# 第一个path为遍历体，第二个path为比较体
def dataCompare(path, path2):
    # 获取数据
    file_name = FileUtils.getFileName(path)
    if Data.DEBUG:
        Result.debug(f"正在比较json文件: {file_name}")
    json_data = loadJson(path)
    json_data2 = loadJson(path2)

    # 判空
    if not json_data:
        Data.empty_files.append(file_name)
        return (-1, "比较失败")
    if not json_data2:
        Data.empty_files.append(file_name)
        return (-1, "比较失败")
    # 循环判断
    key = "dataList"
    if key in json_data:
        json_data_length = len(json_data[key])
        json_data2_length = len(json_data2[key])
        if json_data_length != json_data2_length:
            equal_count = 0
            for x in json_data[key]:
                if "id" in x:
                    id = x["id"]
                    exists = any(id == data["id"] for data in json_data2[key])
                    if exists:
                        equal_count += 1
                        Data.compare_files.append(file_name)
                    else:
                        Data.mismatch_data.append((file_name, x))
                else:
                    if json_data[key]:
                        # 如果json_data不是空的
                        if json_data[key][0]:
                            json_data_length -= 1
                            continue
                            # 如果json_data[key]不是空的
                    # 不匹配的加入不匹配表，
                    Data.empty_files.append(file_name)
            # 循环体结束
            return (json_data_length, equal_count, "比较完成")
        return (1, "长度相等")
    else:
        # 无dataList, 加入未处理文件
        if Data.DEBUG:
            Result.debug(f"json无DataList: {file_name}")
        Data.unprocessed_files.append(file_name)
        return (0, "不比较")
