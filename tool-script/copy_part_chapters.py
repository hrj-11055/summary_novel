import os
import shutil
import re
"""
 复制用于测试 的 50章
"""
def extract_first_100_files():
    # 源文件夹路径
    source_folder = "/Users/macbookair/project_cursor/summary_novel/3_merge_aoshijiutian"
    # 新文件夹路径
    target_folder = "/Users/macbookair/project_cursor/summary_novel/4_summaries_10"
    
    # 创建目标文件夹
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # 获取源文件夹中的所有文件并按数字排序
    files = os.listdir(source_folder)
    
    # 提取文件名中的数字用于排序
    def get_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0
    
    # 按数字排序文件
    sorted_files = sorted(files, key=get_number)
    
    # 提取前50个文件
    for i, filename in enumerate(sorted_files[:30]):
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)
        
        # 复制文件
        shutil.copy2(source_path, target_path)
        print(f"已复制文件 {i+1}/50: {filename}")

if __name__ == "__main__":
    extract_first_100_files()