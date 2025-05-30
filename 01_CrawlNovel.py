import asyncio
import os
from crawl4ai import *
"""使用crawl4AI爬取小说
你需要修改的地方：
1. 小说的url
2. 小说的章节数 查看最后一章的url 的数字是多少
3. 小说的输出目录 output_dir 
"""
async def main():
    # 确保输出目录存在
    output_dir = r"C:\Users\Administrator\Desktop\summary_novel\1_douluo2"  # 不要有汉字 路径中不能有汉字
    os.makedirs(output_dir, exist_ok=True)
    
    async with AsyncWebCrawler() as crawler:
        for i in range(1,625):  # 爬取第1章到第1818章的页面    直接复制你小说网站的url，然后把后面的数字替换成{i}
            # url = f"https://www.beqege.cc/16750/22333{i}.html" # 完美世界
            # url = f"https://www.beqege.cc/16746/22328{i}.html" # 仙逆
            # url = f"https://www.beqege.cc/16749/22332{i}.html" # 遮天
            url = f"https://www.beqege.cc/16754/22338{i}.html" # 斗罗大陆2绝世唐门
            try:
                result = await crawler.arun(url=url)
                # 保存到文件
                file_path = os.path.join(output_dir, f"{i}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(result.markdown)
                print(f"成功保存第{i+1}页到: {file_path}")
            except Exception as e:
                print(f"爬取第{i+1}页失败: {str(e)}")




if __name__ == "__main__":
    asyncio.run(main())