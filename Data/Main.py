# 系统函数
import os, msvcrt

# 自函数
import Data
from Data import FileUtils, JsonUtils, Result


def run():
    # 清空合并缓存文件夹
    FileUtils.deleteDir(Data.MERGE_PATH)
    if not os.path.exists(Data.MERGE_PATH):
        os.makedirs(Data.MERGE_PATH, exist_ok=True)

    # 开始运行
    Result.info("程序开始运行...")
    Data.lang_files = FileUtils.scanFiles(Data.LANG_PATH)
    Data.translation_flies = FileUtils.scanFiles(Data.TRANSLATION_PATH)
    Result.info("已扫描语言文件夹...")
    for f1 in Data.lang_files:
        if f1 in Data.translation_flies:
            Data.each_files.append(f1)
        else:
            Data.missing_files.append(f1)
    if Data.missing_files:
        count = len(Data.missing_files)
        over_count = 0
        if count:
            Result.info(f"缺少的文件(总计 {count} 项):\n {Data.missing_files}")
            for i in range(count - 1, -1, -1):
                file = Data.missing_files[i]
                path = os.path.join(Data.LANG_PATH, FileUtils.prefixAdd(file))
                path2 = os.path.join(Data.MERGE_PATH, file)
                if FileUtils.copyFile(path, path2):
                    Data.missing_files.remove(file)
                    over_count += 1
            Result.info(f"正在处理, 总计 {count} 项, 已处理 {over_count} 项。")
        if Data.missing_files:
            print(f"  未处理文件: {Data.missing_files}")

    Result.info("开始遍历文件...")
    for file in Data.each_files:
        lang_file = FileUtils.prefixAdd(file)
        path = os.path.join(Data.LANG_PATH, lang_file)
        path2 = os.path.join(Data.TRANSLATION_PATH, file)
        if Data.DEBUG:
            Result.debug(f"开始对比文件: {lang_file} & {file}")
        JsonUtils.dataCompare(path, path2)
        if Data.DEBUG:
            Result.debug(f"文件比较完成: {lang_file} & {file}")
    for file in Data.error_files:
        if file in Data.mismatch_data:
            Data.error_files.remove(file)
    Result.info("遍历文件完成...")

    # 暂时没啥用
    # # 转移空文件
    # if Data.empty_files:
    #     count = len(Data.empty_files)
    #     over_count = 0
    #     if count > 0:
    #         Result.info(f"空文件(总计 {count} 项): \n{Data.empty_files}")
    #         for i in range(count - 1, -1, -1):
    #             file = FileUtils.prefixAdd(Data.empty_files[i])
    #             path = os.path.join(Data.LANG_PATH, file)
    #             path2 = os.path.join(Data.MERGE_PATH, file)
    #             if FileUtils.copyFile(path, path2):
    #                 Data.empty_files.remove(file)
    #                 over_count += 1
    #         Result.info(f"正在处理, 总计 {count} 项, 已处理 {over_count} 项。")
    #         if Data.empty_files:
    #             print(f"  未处理文件: {Data.empty_files}")

    if Data.error_files:
        count = len(Data.error_files)
        over_count = 0
        if count > 0:
            Result.info(f"处理失败的文件(总计 {count} 项): {Data.error_files}")
            for i in range(count - 1, -1, -1):
                file = Data.error_files[i]
                path = os.path.join(Data.LANG_PATH, FileUtils.prefixAdd(file))
                path2 = os.path.join(Data.MERGE_PATH, file)
                if FileUtils.copyFile(path, path2):
                    Data.error_files.remove(file)
                    over_count += 1
            Result.info(f"正在处理, 总计 {count} 项, 已处理 {over_count} 项。")
            if Data.error_files:
                print(f"  未处理文件: {Data.error_files}")

    if Data.mismatch_data:
        count = len(Data.mismatch_data)
        over_count = 0
        jump_count = 0
        if count > 0:
            Result.info(f"缺失的数据(总计 {count} 条)")
            temp_path = os.path.join(Data.CURRENT_PATH, "缺失的数据.txt")
            with open(temp_path, "w", encoding="utf-8-sig") as f:
                for x in Data.mismatch_data:
                    f.write(f"文件: {x[0]} - 数据: {x[1]}\n\n")
            for x in Data.mismatch_data:
                if JsonUtils.mergeJson(x[0], x[1]):
                    over_count += 1
                else:
                    jump_count += 1
            Result.info(
                f"正在处理, 总计 {count} 项, 已处理 {over_count} 项, 已跳过 {jump_count} 项"
            )

    # 转移文件
    Data.transfer_files = FileUtils.scanFiles(Data.MERGE_PATH)
    count = len(Data.transfer_files)
    over_count = 0
    Result.info(f"需要转移的文件(总计 {count} 项):\n{Data.transfer_files}")
    for file in Data.transfer_files:
        path = os.path.join(Data.MERGE_PATH, file)
        path2 = os.path.join(Data.TRANSLATION_PATH, file)
        if FileUtils.copyFile(path, path2):
            over_count += 1
    Result.info(f"正在处理, 总计 {count} 项, 已处理 {over_count} 项。")

    # 结束
    print("按下Enter键关闭此窗口...")
    msvcrt.getch()
