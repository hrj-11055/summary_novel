import re

def extract_and_save_chapters(input_file, output_file):
    """
    从JSON文件中提取章节内容并保存到文本文件 
    提取章节名称，保存到dict.txt文件
    
    参数:
        input_file: 输入JSON文件路径
        output_file: 输出文本文件路径
    """
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式提取正文内容
    pattern = r'《完美世界》正文(.*?)作者_辰东_其他书'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        extracted_content = match.group(1).strip()
        # 按/n分割内容
        chapters = extracted_content.split('\n')
        # 保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for chapter in chapters:
                if chapter.strip():  # 跳过空行
                    f.write(chapter + '\n')
        print(f"内容已成功保存到{output_file}")
        return True
    else:
        print("未找到匹配内容")
        return False

if __name__ == "__main__":
    # 使用示例
    extract_and_save_chapters('chapters_dict.json', 'dict.txt')
else:
    print("未找到匹配内容")