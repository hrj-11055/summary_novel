import os
from openai import OpenAI

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

    # 获取文件内容 - 修改为正确的路径
    file_content = read_file_content(r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\3.5_merge_chapters\1-10.txt")
    prompt_content = read_file_content(r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\prompt.txt")
    
    if not file_content:
        print("无法读取小说内容，请检查文件路径和权限")
        return
        
    if not prompt_content:
        print("无法读取prompt内容，请检查prompt.txt文件")
        return

    print("----- standard request -----")
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
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    summarize_novel()