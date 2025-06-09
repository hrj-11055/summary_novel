import os

def process_file(file_path):
    """
    处理单个文件，提取第24行内容并重写文件
    
    参数:
        file_path (str): 文件路径
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 检查文件是否有24行
        if len(lines) >= 24:
            # 获取第24行内容（索引为23）
            target_line = lines[23].strip()
            
            # 重写文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(target_line)
            
            print(f"成功处理文件: {file_path}")
        else:
            print(f"文件行数不足24行: {file_path}")
            
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def process_directory(directory):
    """
    处理目录中的所有txt文件
    
    参数:
        directory (str): 目录路径
    """
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    print(f"找到 {len(txt_files)} 个txt文件需要处理")
    
    # 处理每个文件
    for filename in txt_files:
        file_path = os.path.join(directory, filename)
        process_file(file_path)

def main():
    # 设置目录路径
    directory = "/Users/macbookair/project_cursor/summary_novel/1_aoshijiutian"
    
    print("开始处理文件...")
    process_directory(directory)
    print("处理完成！")

if __name__ == "__main__":
    main() 