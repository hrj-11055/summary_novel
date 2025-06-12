import os

def merge_txt_files():
    # 设置输入和输出目录路径
    input_dir = r"C:\Users\Administrator\Desktop\summary_novel\2_meinv"
    output_dir = r"C:\Users\Administrator\Desktop\summary_novel\3_merge_meinv"
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(input_dir) 
                   if f.endswith('.txt') and f[:-4].isdigit() and 1 <= int(f[:-4]) <= 2045],
                   key=lambda x: int(x[:-4]))

    # 修改点1：将步长10改为5
    for i in range(0, len(files), 5):
        start = int(files[i][:-4])
        # 修改点2：结束编号计算从+9改为+4
        end = start + 4 if i + 4 < len(files) else int(files[-1][:-4])
        output_filename = f"{start}-{end}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # 合并文件
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # 修改点3：合并范围从10改为5
            for j in range(i, min(i + 5, len(files))):
                file_path = os.path.join(input_dir, files[j])
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read() + "\n\n")

        print(f"已合并文件到: {output_path}")
        
        # 统计3_merge_chapters目录下的文件数并打印
        merged_files_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))])
        print(f"3_merge_chapters文件数: {merged_files_count}")

if __name__ == "__main__":
    merge_txt_files()