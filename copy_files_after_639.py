import os
import shutil
import glob

def copy_files_after_639():
    # 创建目标文件夹
    target_dir = "3_merge_aoshi_639"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # 获取源文件夹中的所有文件
    source_dir = "3_merge_aoshi"
    files = glob.glob(os.path.join(source_dir, "*.txt"))
    
    # 按数字排序
    files.sort(key=lambda x: int(os.path.basename(x).split('-')[0]))
    
    # 找到"637-639"之后的位置
    start_index = 0
    for i, file in enumerate(files):
        if "637-639" in file:
            start_index = i + 1
            break
    
    # 复制接下来的100个文件
    for file in files[start_index:start_index + 100]:
        shutil.copy2(file, os.path.join(target_dir, os.path.basename(file)))
        print(f"已复制文件: {os.path.basename(file)}")

if __name__ == "__main__":
    copy_files_after_639() 