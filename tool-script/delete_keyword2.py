import os
from pathlib import Path

def process_files(folder_path):
    """处理文件夹中的所有文件，删除'（未完待续）'关键词"""
    # 转换为Path对象
    folder = Path(folder_path)
    
    # 记录包含关键词的文件
    files_with_mark = []
    
    # 遍历文件夹中的所有文件
    for file_path in folder.glob('*.txt'):
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含关键词
            if '（未完待续）' in content:
                # 记录文件名
                files_with_mark.append(file_path.name)
                
                # 删除关键词
                new_content = content.replace('（未完待续）', '')
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已处理文件: {file_path.name}")
                
        except Exception as e:
            print(f"处理文件 {file_path.name} 时出错: {str(e)}")
    
    # 输出结果
    if files_with_mark:
        print("\n以下文件包含'（未完待续）'并已处理：")
        for file_name in files_with_mark:
            print(f"- {file_name}")
    else:
        print("\n未找到包含'（未完待续）'的文件")

if __name__ == "__main__":
    # 指定要处理的文件夹路径
    folder_path = input("请输入要处理的文件夹路径: ")
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print("错误：指定的文件夹不存在！")
    else:
        process_files(folder_path)