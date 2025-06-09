import os
import glob

def merge_all_files():
    # 源文件夹路径
    source_dir = "/Users/macbookair/project_cursor/summary_novel/3_merge_aoshi_639"
    # 目标文件路径
    target_file = "/Users/macbookair/project_cursor/summary_novel/3_merge_aoshi_639/639-999.txt"
    
    # 获取所有txt文件并按数字排序
    files = glob.glob(os.path.join(source_dir, "*.txt"))
    files.sort(key=lambda x: int(os.path.basename(x).split('-')[0]))
    
    # 合并文件内容
    with open(target_file, 'w', encoding='utf-8') as outfile:
        for file in files:
            filename = os.path.basename(file)
            with open(file, 'r', encoding='utf-8') as infile:
                # 写入文件名作为分隔符
                outfile.write(f"\n\n{'='*50}\n")
                outfile.write(f"文件名: {filename}\n")
                outfile.write(f"{'='*50}\n\n")
                # 写入文件内容
                outfile.write(infile.read())
    
    print(f"所有文件已合并到: {target_file}")

if __name__ == "__main__":
    merge_all_files() 