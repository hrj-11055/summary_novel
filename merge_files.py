import os

def merge_txt_files():
    # 设置输入和输出目录路径
    input_dir = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\2_perfect_world_yuanwen"
    output_dir = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\3.5_merge_chapters"
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有1-2016.txt文件并按数字排序
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.txt') and f[:-4].isdigit() and 1 <= int(f[:-4]) <= 2015], 
                  key=lambda x: int(x[:-4]))

    # 每10个文件合并一次
    for i in range(0, len(files), 10):
        # 确定合并范围，根据示例，结束编号应该是起始编号加10（如果足够的话）
        start = int(files[i][:-4])
        end = start + 9 if i + 9 < len(files) else int(files[len(files) - 1][:-4])
        output_filename = f"{start}-{end}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # 合并文件
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for j in range(i, min(i + 10, len(files))):
                file_path = os.path.join(input_dir, files[j])
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")  # 添加分隔符
        
        print(f"已合并文件到: {output_path}")
        
        # 统计3_merge_chapters目录下的文件数并打印
        merged_files_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))])
        print(f"3_merge_chapters文件数: {merged_files_count}")

if __name__ == "__main__":
    merge_txt_files()