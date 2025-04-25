import re
import os
from pathlib import Path

def extract_zw_content(text):
    """提取zw443sx标记之间的内容"""
    pattern = r'zw443sx(.*?)（未完待续）'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if matches else None

def process_files(input_dir, output_dir):
    """处理目录中的所有文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 确保输出目录存在
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 遍历输入目录中的所有文件
    for input_file in input_path.glob('*'):
        if input_file.is_file():
            try:
                # 读取文件内容
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取内容
                extracted = extract_zw_content(content)
                
                if extracted:
                    # 构建输出文件路径
                    output_file = output_path / input_file.name
                    
                    # 写入提取的内容
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(extracted)
                    print(f"成功处理文件: {input_file.name}")
                else:
                    print(f"警告: 文件中未找到zw443sx标记 - {input_file.name}")
                    
            except Exception as e:
                print(f"处理文件 {input_file.name} 时出错: {str(e)}")

if __name__ == "__main__":
    # 输入和输出目录
    input_directory = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\1_perfect_world"
    output_directory = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\2_perfect_world_yuanwen"
    
    # 处理文件
    process_files(input_directory, output_directory)
    print("处理完成！")