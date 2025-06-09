import os
import re

def split_sentences(text):
    """
    智能分割句子，避免分割引号内的内容
    
    参数:
        text (str): 原始文本
        
    返回:
        list: 分割后的句子列表
    """
    # 先找出所有引号内的内容
    quoted_texts = []
    def replace_quoted(match):
        quoted_texts.append(match.group(0))
        return f"QUOTED_TEXT_{len(quoted_texts)-1}"
    
    # 替换引号内的内容
    text = re.sub(r'[""](.*?)[""]', replace_quoted, text)
    
    # 按句号、问号、感叹号分割
    sentences = []
    current = ""
    
    for char in text:
        current += char
        if char in "。！？" and not current.endswith("QUOTED_TEXT_"):
            sentences.append(current)
            current = ""
    
    if current:
        sentences.append(current)
    
    # 还原引号内的内容
    for i, sentence in enumerate(sentences):
        for j, quoted in enumerate(quoted_texts):
            sentences[i] = sentences[i].replace(f"QUOTED_TEXT_{j}", quoted)
    
    return sentences

def format_paragraph(content):
    """
    将文本内容格式化为段落形式
    
    参数:
        content (str): 原始文本内容
        
    返回:
        str: 格式化后的文本
    """
    # 智能分割句子
    sentences = split_sentences(content)
    
    # 重新组合句子
    formatted_sentences = []
    current_sentence = ""
    
    for sentence in sentences:
        # 如果当前句子加上新句子不超过50个字，就合并
        if len(current_sentence) + len(sentence) <= 50:
            current_sentence += sentence
        else:
            if current_sentence:
                formatted_sentences.append(current_sentence)
            current_sentence = sentence
    
    # 添加最后一个句子
    if current_sentence:
        formatted_sentences.append(current_sentence)
    
    # 将句子组合成段落，每个段落之间用换行符分隔
    return '\n'.join(formatted_sentences)

def process_file(input_file, output_file):
    """
    处理单个文件，重新格式化内容并保存
    
    参数:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    try:
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 删除多余的空白字符
        content = re.sub(r'\s+', '', content)
        
        # 格式化内容
        formatted_content = format_paragraph(content)
        
        # 保存处理后的内容
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
            
        print(f"成功处理文件: {input_file}")
        
    except Exception as e:
        print(f"处理文件 {input_file} 时出错: {e}")

def process_directory(input_dir, output_dir):
    """
    处理目录中的所有txt文件
    
    参数:
        input_dir (str): 输入目录路径
        output_dir (str): 输出目录路径
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    print(f"找到 {len(txt_files)} 个txt文件需要处理")
    
    # 处理每个文件
    for filename in txt_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        process_file(input_path, output_path)

def main():
    # 设置输入输出目录
    input_dir = "/Users/macbookair/project_cursor/summary_novel/1_aoshijiutian"
    output_dir = "/Users/macbookair/project_cursor/summary_novel/2_aoshijiutian"
    
    print("开始处理文件...")
    process_directory(input_dir, output_dir)
    print("处理完成！")

if __name__ == "__main__":
    main() 