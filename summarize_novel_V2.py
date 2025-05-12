"""
怎么会这样：token占满，但没有使用上下文缓存啊, 

因为尽管删除了content_ID没用上下文缓存API ，但有使用modelID 是固定某个有上下文对话的模型

modelID：ep-20250427214610-2tdd2  豆包pro32K
"""
import os
import datetime
from dotenv import load_dotenv
from openai import responses
from volcenginesdkarkruntime import Ark

def read_file_content(file_path):
    """
    读取指定文件的内容
    
    参数:
        file_path (str): 要读取的文件路径
        
    返回:
        str: 文件内容字符串，如果读取失败则返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def log_api_usage(filename, usage, model, file_path="api_usage.log"):
    """
    记录API调用的token使用情况到日志文件
    
    参数:
        filename (str): 处理的文件名
        usage (object): 包含token使用信息的对象
        model (str): 使用的模型名称
        file_path (str): 日志文件路径，默认为"api_usage.log"
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = (f"[{timestamp}] {filename} Token usage:"
    f"Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}, "
    f"Total: {usage.total_tokens}, Model: {model}\n"
    )
    with open(file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_message)

def ensure_output_folder_exists(output_file):
    """
    确保输出目录存在，如果不存在则创建
    
    参数:
        output_file (str): 要检查/创建的目录路径
    """
    if not os.path.exists(output_file):
        os.makedirs(output_file)

def process_single_file(client, filename, input_folder, output_folder, prompt_content):
    """
    处理单个文件，调用API生成总结并保存结果
    
    参数:
        client (Ark): API客户端实例
        filename (str): 要处理的文件名
        input_folder (str): 输入文件目录
        output_folder (str): 输出文件目录
        prompt_content (str): 系统提示词内容
    """
    file_path = os.path.join(input_folder, filename)

    file_content = read_file_content(file_path)
    if not file_content:
        print(f"无法读取 {filename} 的内容，请检查文件路径和权限")
        return

    print(f"----- 处理文件 {filename} ------")

    try:
        response = client.chat.completions.create(
            model="ep-20250427230855-gfc8x",# doubao1.5pro 32k 250115，  直接填入模型名称会导致模型没有上下文缓存，好处是token消耗少10000每次
            #context_id="ctx-20250428004144-r7qss",
            messages=[
                {
                    "role": "system",
                    "content": prompt_content
                },
                {
                    "role": "user",
                    "content": file_content
                }
            
            ],
            extra_headers={'x-is-encrypted': 'true'},
            temperature=0.6,
            top_p=0.5,
            max_tokens=1024,
            frequency_penalty=0.002,
        )

        # 记录APItoken使用情况
        log_api_usage(filename, response.usage, response.model)
        print(f"Model: {response.model}"
              f"Token usage - Prompt: {response.usage.prompt_tokens}, "
              f"Completion: {response.usage.completion_tokens}, "
              f"Total: {response.usage.total_tokens}")
        
        summary = response.choices[0].message.content
        output_file_path = os.path.join(output_folder, filename)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(summary)
        print(f"已将 {filename} 的总结结果保存到 {output_file_path}")
    except Exception as e:
        print(f"处理 {filename} 时出错: {e}")

def summarize_novel():
    """
    主函数，加载配置并处理所有输入文件
    
    流程:
    1. 加载环境变量
    2. 初始化API客户端
    3. 读取提示词内容
    4. 确保输出目录存在
    5. 使用线程池批量处理文件(每次5个)
    """
    load_dotenv()

    client = Ark(api_key=os.environ.get("ARK_API_KEY"))

    prompt_content = read_file_content("prompt.txt")
    if not prompt_content:
        print("无法读取提示词内容，请检查文件路径和权限")
        return

    #input_folder = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\3_merge_chapters_first_100"
    input_folder = r"C:\Users\Administrator\Desktop\summary_novel\3_merge_chapters_10"
    output_folder = r"C:\Users\Administrator\Desktop\summary_novel\4_summaries_10"
    ensure_output_folder_exists(output_folder)

    # 获取文件列表
    file_list = os.listdir(input_folder)
    
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
                    filename, 
                    input_folder, 
                    output_folder, 
                    prompt_content
                ) for filename in batch
            ]
            
            # 等待当前批次完成
            for future in futures:
                future.result()

if __name__ == "__main__":
    summarize_novel()