import os, shutil
import Data
from Data import Result


# 扫描文件
def scanFiles(scan_path):
    if Data.DEBUG:
        Result.info(f"开始扫描目录: {scan_path}")
    scan_files = list()
    scan_entrys = os.scandir(scan_path)
    for entry in scan_entrys:
        if entry.is_file():
            scan_files.append(prefixRemove(entry.name))
        elif entry.is_dir():
            jump = False
            for x in Data.SAFE_DIR:
                if x in entry.name:
                    if Data.DEBUG:
                        Result.info(f"子目录为排除文件,跳过: {entry.name}")
                    jump = True
                    break
            if jump:
                continue
            scan_path2 = os.path.join(scan_path, entry.name)
            if Data.DEBUG:
                Result.info(f"遇到子目录,开始扫描: {scan_path2}")
            scan_entrys2 = os.scandir(scan_path2)
            for entry2 in scan_entrys2:
                file = os.path.join(entry.name, prefixRemove(entry2.name))
                scan_files.append(file)

    scan_files.sort()
    Result.info(f"扫描完成，总计 {len(scan_files)} 项")
    if Data.DEBUG:
        Result.debug_list("文件列表:", scan_files)
    return scan_files.copy()


# 复制文件
# path -> path2
def copyFile(path, path2):
    if not os.path.exists(path):
        Result.error(f"文件不存在: {path}")
        return False
    if "." not in path2:
        if not os.path.exists(path2):
            os.makedirs(path2, exist_ok=True)
    else:
        dir_path = os.path.dirname(path2)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
    shutil.copy2(path, path2)
    return True


# 删除文件夹
def deleteDir(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            return True
        except PermissionError:
            Result.error(f"权限不足,文件夹删除失败: {path}")
        except Exception as e:
            Result.error(f"文件夹删除失败: \n{e}")
    else:
        return True


# 增加前缀
def prefixAdd(path):
    if path:
        if Data.LANG not in path:
            if "\\" in path:
                index = path.rfind("\\")
                processed_path = os.path.join(
                    path[:index:], Data.LANG + "_" + path[index + 1 : :]
                )
            else:
                processed_path = os.path.join(Data.LANG + "_" + path)
            return processed_path
        return path
    return False


# 删除前缀
def prefixRemove(path):
    if path:
        if Data.LANG in path:
            if "\\" in path:
                index = path.rfind("\\")
                processed_path = os.path.join(
                    Data.LANG_PATH, path[:index:], path[index + 4 : :]
                )
            else:
                processed_path = os.path.join(path[3::])
            return processed_path
        else:
            return path
    return False


# 获取文件名
def getFileName(path):
    if path:
        if Data.LANG in path:
            if "\\" in path:
                index = path.rfind("\\")
                file = path[index + 4 : :]
            else:
                file = path[3::]
            return file
        else:
            if "\\" in path:
                index = path.rfind("\\")
                file = path[index + 1 : :]
            else:
                file = path
            return file
    return False
