import asyncio
import os
from crawl4ai import *

async def main():
    # 确保输出目录存在
    output_dir = r"C:\Users\Administrator\Desktop\xiaoshuo_suoxie\perfect_world"
    os.makedirs(output_dir, exist_ok=True)
    
    async with AsyncWebCrawler() as crawler:
        for i in range(1,1592):  # 爬取1592到1601的页面
            url = f"https://www.beqege.cc/16750/22333{i}.html"
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