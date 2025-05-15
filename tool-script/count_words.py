import os

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
    """统计目录下所有txt文件的字数"""
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return
    
    print(f"正在统计目录: {directory}")
    print("-" * 40)
    
    total_words = 0
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            word_count = count_words_in_file(file_path)
            print(f"{filename}: {word_count} 字")
            total_words += word_count
    
    print("-" * 40)
    print(f"总字数: {total_words} 字")

if __name__ == "__main__":
    # 指定要统计的目录路径
    #target_dir = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\3.5_merge_chapters"
    target_dir = r"C:\Users\Administrator\Desktop\summary_novel\3_merge_chapters_zhetian"
    count_words_in_directory(target_dir)