import os

def count_characters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 计算中文字符数（去除空格和换行符）
            char_count = len([char for char in content if char.strip()])
            return char_count
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return 0

def process_directory(directory):
    total_chars = 0
    file_count = 0
    file_stats = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                char_count = count_characters(file_path)
                total_chars += char_count
                file_count += 1
                file_stats.append((file, char_count))
    
    # 按字数排序
    file_stats.sort(key=lambda x: x[1], reverse=True)
    
    # 打印统计信息
    print(f"\n总文件数: {file_count}")
    print(f"总字数: {total_chars}")
    print(f"平均每文件字数: {total_chars/file_count:.2f}")
    print("\n字数最多的前10个文件:")
    for file, count in file_stats[:10]:
        print(f"{file}: {count}字")
    
    print("\n字数最少的前10个文件:")
    for file, count in file_stats[-10:]:
        print(f"{file}: {count}字")

if __name__ == "__main__":
    # 处理summary_novel目录下的所有文件
    base_dir = "/Users/macbookair/project_cursor/summary_novel/3_merge_aoshijiutian"
    process_directory(base_dir)