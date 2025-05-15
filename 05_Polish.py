"""
使用豆包大模型API对4_summary_good文件夹中的摘要进行润色处理
"""
import os
import datetime
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

def check_api_availability(client):
    try:
        test_response = client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return test_response.choices[0].message.content is not None
    except Exception as e:
        print(f"API检测失败: {e}")
        return False

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def log_api_usage(filename, usage, model, file_path="api_polish_usage.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = (
        f"[{timestamp}] {filename} Model: {model} Token usage: "
        f"Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}, "
        f"Total: {usage.total_tokens}\n"
    )
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(log_message)

def ensure_output_folder_exists(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def process_single_file(client, prompt_content, filename, input_folder, output_folder):
    file_path = os.path.join(input_folder, filename)
    file_content = read_file_content(file_path)
    if not file_content:
        print(f"无法读取 {filename} 的内容")
        return

    print(f"----- 润色文件 {filename} -----")
    try:
        resp = client.chat.completions.create(
            # model="ep-20250514185643-2g997", doubao1.5pro thinking 32K 250115  适合生成解说文案的标题 
            model="doubao-1-5-pro-32k-250115",
            messages=[
                {"role": "system", "content": prompt_content},
                {"role": "user", "content": f"请对以下小说摘要进行润色:\n{file_content}"}
            ],
            extra_headers={'x-is-encrypted': 'true'},
            temperature=0.5,
            top_p=0.7,
            max_tokens=2048
        )
        
        log_api_usage(filename, resp.usage, resp.model)
        print(f"Token使用 - 提示词: {resp.usage.prompt_tokens}, 生成: {resp.usage.completion_tokens}")

        polished_content = resp.choices[0].message.content
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(polished_content)
        print(f"已保存润色结果到 {output_path}")
    except Exception as e:
        print(f"处理 {filename} 时出错: {e}")

def polish_summaries():
    load_dotenv()
    client = Ark(api_key=os.environ.get("ARK_API_KEY"))
    
    if not check_api_availability(client):
        print("API服务不可用")
        return

    prompt_content = """
    - Role: 网文小说文案润色专家
- Background: 用户需要将网文小说的情节概要转化为适合口语化表达的网文解说文案，以便吸引听众并增强故事的吸引力。
- Profile: 你是一位在网文小说领域深耕多年、深谙文案魅力的润色大师，对小说情节的把握和语言的转化有着独到的见解，能够将枯燥的情节描述转化为生动、引人入胜的口语化表达。
- Skills: 你拥有丰富的文学创作经验、敏锐的语言感知能力以及出色的文案润色技巧，能够精准地捕捉情节的亮点，并运用连贯的词汇和口语化的表达方式，让文案更具吸引力和感染力。
- Goals: 将用户提供的网文小说情节概要进行润色，使其内容保持不变，但语言更加流畅、生动，便于口语化表达，适合网文解说博主使用。
- Constrains: 保持原文的核心情节和内容不变，避免过度夸张或偏离主题，确保文案的准确性和真实性。
- OutputFormat: 口语化的文案，使用生动的词汇和连贯的表达，适合网文解说博主的风格。
- Workflow:
  1. 仔细阅读并理解用户提供的网文小说情节概要。
  2. 提炼情节的关键点，确定需要重点表达的部分。
  3. 运用连贯的词汇和口语化的表达方式，对情节进行重新组织和润色。
  4.不要说开场白，例如，嘿，各位听好了啊   
    """
    
    input_folder = r"C:\Users\Administrator\Desktop\summary_novel\4_summaries_10"
    output_folder = r"C:\Users\Administrator\Desktop\summary_novel\5_polish"
    ensure_output_folder_exists(output_folder)

    # 获取文件列表
    file_list = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    
    # 使用线程池批量处理(每次5个)
    from concurrent.futures import ThreadPoolExecutor
    BATCH_SIZE = 5
    
    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
        for i in range(0, len(file_list), BATCH_SIZE):
            batch = file_list[i:i+BATCH_SIZE]
            print(f"\n=== 正在处理批次 {i//BATCH_SIZE+1} (共{len(batch)}个文件) ===")
            
            # 提交批处理任务
            futures = [
                executor.submit(
                    process_single_file, 
                    client, 
                    prompt_content, 
                    filename, 
                    input_folder, 
                    output_folder
                ) for filename in batch
            ]
            
            # 等待当前批次完成
            for future in futures:
                future.result()

if __name__ == "__main__":
    polish_summaries()