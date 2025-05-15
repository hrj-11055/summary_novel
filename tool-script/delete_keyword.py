import os
"""
 删除 "未完待续" 行，且包含 "起点" 的行  
 同时也可以检测并打印出哪些章节 是502 报错， 属于缺失章节
"""
def process_files(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 只处理txt文件
        if filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # 标记是否找到关键词
            found_keyword = False
            new_lines = []
            
            # 处理每一行
            for line in lines:
                if "未完待续" in line:
                    found_keyword = True
                    # 如果包含"起点"则跳过该行
                    if "起点" not in line:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # 如果没有找到关键词则打印文件名
            if not found_keyword:
                print(f"文件 {filename} 中未找到'未完待续'关键词")
            
            # 将处理后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(new_lines)

if __name__ == "__main__":
    # 指定要处理的文件夹路径
    folder_path = r"c:\Users\Administrator\Desktop\summary_novel\2_zhetian"
    process_files(folder_path)