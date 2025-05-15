import os
import time
from concurrent.futures import ThreadPoolExecutor

def search_keyword_in_file(file_path, keyword):
    """在单个文件中搜索关键词"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if keyword in content:
                return file_path
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    return None

def find_files_with_keyword(folder_path, keyword, max_workers=5):
    """使用多线程快速查找包含关键词的文件"""
    start_time = time.time()
    matching_files = []
    
    # 获取所有文本文件
    file_list = [
        os.path.join(folder_path, f) 
        for f in os.listdir(folder_path) 
        if f.endswith('.txt')
    ]
    
    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(search_keyword_in_file, file_path, keyword)
            for file_path in file_list
        ]
        
        for future in futures:
            result = future.result()
            if result:
                matching_files.append(result)
    
    end_time = time.time()
    print(f"\n搜索完成，耗时: {end_time - start_time:.2f}秒")
    return matching_files

if __name__ == "__main__":
    # 配置参数
    search_folder = r"C:\Users\Administrator\Desktop\summary_novel\2_xianni_yuanwen"
    search_keyword = input("请输入要查找的关键词: ")
    
    # 执行搜索
    found_files = find_files_with_keyword(search_folder, search_keyword)
    
    # 输出结果
    if found_files:
        print("\n找到以下包含关键词的文件:")
        for file in found_files:
            print(f"- {os.path.basename(file)}")
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    index = content.find(search_keyword)
                    if index != -1:
                        start = max(0, index - 10)
                        end = min(len(content), index + len(search_keyword) + 10)
                        context = content[start:end]
                        print(f"  上下文: ...{context}...")
            except Exception as e:
                print(f"  读取文件上下文时出错: {e}")
    else:
        print("\n未找到包含该关键词的文件")