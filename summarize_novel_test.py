"""
用的上下文缓存模型， 效果反而不好：调用会满32Ktoken，导致输出为1token

用于测试 小量文件的 模型整体输出结果是否稳定 

"""
import os
import datetime
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

def check_api_availability(client):
    """
    检查API是否可用。

    此函数通过向指定模型发送一个简单的测试请求，来验证API服务是否正常工作。

    参数:
    client (Ark): Ark客户端实例，用于与API进行交互。

    返回:
    bool: 如果API返回有效响应，则返回True；否则返回False。
    """
    try:
        # 发送一个简单的测试请求
        test_response = client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return test_response.choices[0].message.content is not None
    except Exception as e:
        print(f"API检测失败: {e}")
        return False

# 读取文件内容作为用户输入
def read_file_content(file_path):
    """
    读取指定文件的内容。

    此函数尝试以UTF-8编码打开指定路径的文件，并读取其全部内容。

    参数:
    file_path (str): 要读取的文件的路径。

    返回:
    str: 如果文件读取成功，则返回文件内容；否则返回None。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def log_api_usage(filename, usage, model, file_path="api_usage.log"):
    """
    记录API调用的token使用情况到日志文件中。

    此函数将每次API调用的token使用情况，包括模型名称、提示词token数、完成内容token数、
    总token数和缓存token数，记录到指定的日志文件中，并添加时间戳。

    参数:
    filename (str): 正在处理的文件名。
    usage (object): 包含token使用信息的对象，需有prompt_tokens、completion_tokens和total_tokens属性。
    model (str): 使用的模型名称。
    cached_tokens (int, 可选): 缓存的token数，默认为0。
    file_path (str, 可选): 日志文件的路径，默认为"api_usage.log"。
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = (
        f"[{timestamp}] {filename} Model: {model} Token usage: "
        f"Prompt: {usage.prompt_tokens}, "
        f"Completion: {usage.completion_tokens}, "
        f"Total: {usage.total_tokens}\n"
    )
    with open(file_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_message)

def ensure_output_folder_exists(output_folder):
    """
    确保指定的输出文件夹存在。

    如果输出文件夹不存在，则创建该文件夹。

    参数:
    output_folder (str): 输出文件夹的路径。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def process_single_file(client, prompt_content, filename, input_folder, output_folder):
    """
    处理单个文件，生成总结并保存结果。

    此函数读取输入文件的内容，调用API生成总结，记录token使用情况，并将总结结果保存到输出文件中。

    参数:
    client (Ark): Ark客户端实例，用于与API进行交互。
    prompt_content (str): 提示词的内容。
    filename (str): 要处理的文件名。
    input_folder (str): 输入文件夹的路径。
    output_folder (str): 输出文件夹的路径。
    """
    file_path = os.path.join(input_folder, filename)
    # 读取文件内容
    file_content = read_file_content(file_path)
    if not file_content:
        print(f"无法读取 {filename} 的内容，请检查文件路径和权限")
        return

    print(f"----- 处理文件 {filename} 的请求 -----")
    try:
        resp = client.chat.completions.create(
            model="doubao-1-5-pro-32k",# doubao1.5pro 32k 250115，  直接填入模型名称会导致模型没有上下文缓存，好处是token消耗少10000每次
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
            
            temperature=0.6,
            top_p=0.5,
            max_tokens=1024,
            
        )
        
        # 记录API调用token使用情况
        
        log_api_usage(filename, resp.usage, resp.model)
        print(f"Model: {resp.model}")
        print(f"Token usage - Prompt: {resp.usage.prompt_tokens}, "
              f"Completion: {resp.usage.completion_tokens}, "
              f"Total: {resp.usage.total_tokens}, ")

        summary = resp.choices[0].message.content

        # 定义输出文件路径
        output_file_path = os.path.join(output_folder, filename)
        # 将总结结果写入输出文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(summary)

        print(f"已将 {filename} 的总结结果保存到 {output_file_path}")
    except Exception as e:
        print(f"处理 {filename} 时出错: {e}")

def summarize_novel():
    """
    对小说文件进行总结处理。

    此函数加载环境变量，初始化API客户端，检查API可用性，读取提示词内容，
    遍历输入文件夹中的所有文件，调用API生成总结，并将结果保存到输出文件夹中。
    """
    # 加载.env文件中的环境变量
    load_dotenv()
    
    # 初始化客户端
    client = Ark(api_key=os.environ.get("ARK_API_KEY"))
    
    # 检测API可用性
    if not check_api_availability(client):
        print("API服务不可用，请检查网络连接或API密钥")
        return

    # 读取prompt内容
    prompt_content = read_file_content(r"C:\Users\Administrator\Desktop\summary_novel\prompt_good.txt")
    if not prompt_content:
        print("无法读取prompt内容，请检查prompt.txt文件")
        return

    # 定义输入文件夹和输出文件夹路径
    input_folder = r"C:\Users\Administrator\Desktop\summary_novel\3_merge_chapters_10"
    # 第二次 使用不同prompt，测试结果 output_folder = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\4_merge_chapters"
    output_folder = r"C:\Users\Administrator\Desktop\summary_novel\4_summaries_good"

    # 确保输出文件夹存在
    ensure_output_folder_exists(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        process_single_file(client, prompt_content, filename, input_folder, output_folder)

if __name__ == "__main__":
    summarize_novel()