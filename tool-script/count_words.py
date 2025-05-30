import os
"""
用于统计小说章节字数和缺失章节
您只需修改target_dir
"""
def count_words_in_file(file_path):
    """统计单个文件的字数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return len(content)
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return 0

def count_words_in_directory(directory):
    """统计目录下所有txt文件的字数，并打印 缺失的章节"""
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return
    
    print(f"正在统计目录: {directory}")
    print("-" * 40)
    print("缺失的章节:")
    print("-" * 40)
    
    total_words = 0
    short_files = []  # 用于存储字数少于100的文件
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            word_count = count_words_in_file(file_path)
            total_words += word_count
            
            # 如果字数少于100，记录文件名
            if word_count < 100:
                short_files.append((filename, word_count))
    
    # 按字数排序并打印少于100字的文件
    if short_files:
        for filename, count in sorted(short_files, key=lambda x: x[1]):
            print(f"{filename}: {count} 字")
    else:
        print("没有找到字数少于100的文件")
    
    print("-" * 40)
    print(f"目录总字数: {total_words} 字")

if __name__ == "__main__":
    # 指定要统计的目录路径
    target_dir = r"C:\Users\Administrator\Desktop\summary_novel\2_douluo2_yuanwen"
    count_words_in_directory(target_dir)