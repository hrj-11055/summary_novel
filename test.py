import asyncio
import re
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.beqege.cc/16750/",
        )
        # 使用正则表达式提取章节标题和链接
        pattern = r'<a href="(/16750/\d+\.html)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, result.markdown)
        
        # 写入dict.txt文件
        with open('dict.txt', 'w', encoding='utf-8') as f:
            for link, title in matches:
                full_link = f"https://www.beqege.cc{link}"
                f.write(f"[{title}]( `{full_link}`)\n")
        
        print("章节链接已保存到dict.txt文件")

if __name__ == "__main__":
    asyncio.run(main())
