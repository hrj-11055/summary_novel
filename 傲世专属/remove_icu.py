import os

def process_file(file_path):
    """
    处理单个文件，删除包含".icu"的行和"*****"后面的内容
    
    参数:
        file_path (str): 文件路径
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 过滤掉包含".icu"的行
        filtered_lines = [line for line in lines if ".icu" not in line]
        
        # 处理"*****"后面的内容
        processed_lines = []
        for line in filtered_lines:
            if "*****" in line:
                # 只保留"*****"之前的内容
                line = line.split("*****")[0] + "\n"
            processed_lines.append(line)
        
        # 重写文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)
        
        # 计算删除的行数
        removed_lines = len(lines) - len(processed_lines)
        if removed_lines > 0:
            print(f"成功处理文件: {file_path}, 删除了 {removed_lines} 行")
        else:
            print(f"文件无需处理: {file_path}")
            
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
    directory = "/Users/macbookair/project_cursor/summary_novel/2_aoshijiutian"
    
    print("开始处理文件...")
    process_directory(directory)
    print("处理完成！")

if __name__ == "__main__":
    main() 