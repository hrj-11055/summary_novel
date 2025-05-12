import os
from openai import OpenAI
import datetime  # 新增导入

def check_api_availability(client):
    """检查API是否可用"""
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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

# 新增函数：记录API token使用情况
def log_token_usage(filename, usage, log_file="api_token_usage.log"):
    """
    记录API调用的token使用情况
    
    参数:
    filename (str): 处理的文件名
    usage (object): 包含prompt_tokens, completion_tokens和total_tokens的对象
    log_file (str): 日志文件路径，默认为api_token_usage.log
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] {filename}\n"
        f"Prompt tokens: {usage.prompt_tokens}\n"
        f"Completion tokens: {usage.completion_tokens}\n"
        f"Total tokens: {usage.total_tokens}\n\n"
    )
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"写入token使用日志失败: {e}")

def summarize_novel():
    # 初始化Openai客户端
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="b38b2f1e-0477-4472-9c01-d6cc58c0cfdd",
    )
    
    # 检测API可用性
    if not check_api_availability(client):
        print("API服务不可用，请检查网络连接或API密钥")
        return

    # 读取prompt内容
    prompt_content = read_file_content(r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\prompt.txt")
    if not prompt_content:
        print("无法读取prompt内容，请检查prompt.txt文件")
        return

    # 定义输入文件夹和输出文件夹路径
    input_folder = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\3_merge_chapters_part2"
    output_folder = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\4_summaries"

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            # 读取文件内容
            file_content = read_file_content(file_path)
            if not file_content:
                print(f"无法读取 {filename} 的内容，请检查文件路径和权限")
                continue

            print(f"----- 处理文件 {filename} 的请求 -----")
            try:
                completion = client.chat.completions.create(
                    model="doubao-1-5-pro-32k-250115",
                    messages=[
                        {
                            "role": "system", 
                            "content": prompt_content
                        },
                        {
                            "role": "user", 
                            "content": file_content
                        }
                    ]
                )
                
                # 新增：记录token使用情况
                log_token_usage(filename, completion.usage)
                print(f"Token使用情况 - 提示词: {completion.usage.prompt_tokens}, "
                      f"生成内容: {completion.usage.completion_tokens}, "
                      f"总计: {completion.usage.total_tokens}")
                
                summary = completion.choices[0].message.content

                # 定义输出文件路径
                output_file_path = os.path.join(output_folder, filename)
                # 将总结结果写入输出文件
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(summary)

                print(f"已将 {filename} 的总结结果保存到 {output_file_path}")
            except Exception as e:
                print(f"处理 {filename} 时出错: {e}")

if __name__ == "__main__":
    summarize_novel()