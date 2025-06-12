import os
import concurrent.futures
from openai import OpenAI
import time
from dotenv import load_dotenv

# 配置API参数
# 新增在文件开头
load_dotenv()  # 加载.env文件

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def polish_text(content):
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "我要将小说情节精讲给观众听，请你将小说情节进行润色。只需要给出精讲后的内容(纯文本格式)，不需要其他解释。"},
                {"role": "user", "content": f"请润色以下内容：\n{content}"}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"处理失败: {e}")
        return content

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    polished = polish_text(content)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(polished)

if __name__ == "__main__":
    input_dir = r"C:\Users\Administrator\Desktop\summary_novel\4_summaries_10"
    output_dir = r"C:\Users\Administrator\Desktop\summary_novel\5_polish"
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    # 使用线程池（建议4-8个线程）
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for file in files:
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file)
            futures.append(executor.submit(process_file, input_path, output_path))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"文件处理异常: {e}")

    print("全部文件处理完成！")
