import os
import glob

def merge_files():
    # 创建目标文件夹
    target_dir = "3_merge_aoshi"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # 获取所有txt文件并按数字排序
    source_dir = "2_aoshijiutian"
    files = glob.glob(os.path.join(source_dir, "*.txt"))
    files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    
    # 每3个文件合并成一个
    for i in range(0, len(files), 3):
        group = files[i:i+3]
        if len(group) == 3:
            # 获取第一个和最后一个文件名（不含扩展名）
            first_file = os.path.basename(group[0]).split('.')[0]
            last_file = os.path.basename(group[2]).split('.')[0]
            
            # 创建新文件名
            new_filename = f"{first_file}-{last_file}.txt"
            new_filepath = os.path.join(target_dir, new_filename)
            
            # 合并文件内容
            with open(new_filepath, 'w', encoding='utf-8') as outfile:
                for fname in group:
                    with open(fname, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n\n')  # 添加分隔符
            print(f"已创建合并文件: {new_filename}")

if __name__ == "__main__":
    merge_files() 