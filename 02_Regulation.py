import re
import os
import argparse
from pathlib import Path

def extract_zw_content(text):
    """提取zw443sx标记之间的内容"""
    pattern = r'zw443sx(.*?)zw443sx'
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
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="小说文本规范化处理器")
    parser.add_argument("--input_dir", type=str, required=True, help="输入目录路径，例如：1_perfect_world")
    parser.add_argument("--output_dir", type=str, help="输出目录路径，默认为2_小说名_yuanwen")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 处理输入目录路径
    input_directory = args.input_dir
    if not os.path.isabs(input_directory):
        # 如果是相对路径，转换为绝对路径
        input_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_directory)
    
    # 处理输出目录路径
    if args.output_dir:
        output_directory = args.output_dir
        if not os.path.isabs(output_directory):
            output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_directory)
    else:
        # 如果未指定输出目录，则根据输入目录名自动生成
        input_name = os.path.basename(input_directory)
        if input_name.startswith("1_"):
            novel_name = input_name[2:]  # 去掉"1_"前缀
            output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"2_{novel_name}_yuanwen")
        else:
            output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"2_{input_name}_yuanwen")
    
    print(f"输入目录: {input_directory}")
    print(f"输出目录: {output_directory}")
    
    # 处理文件
    process_files(input_directory, output_directory)
    print("处理完成！")