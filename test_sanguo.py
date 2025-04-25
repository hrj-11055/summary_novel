import requests
import re
from bs4 import BeautifulSoup

url = "https://www.beqege.cc/16750/223331.html"

# 设置中文请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'  # 添加中文语言首选项
}

req = requests.get(url=url, headers=headers)
req.encoding = 'utf-8'  # 显式设置编码

# 使用更健壮的HTML解析方法
soup = BeautifulSoup(req.text, 'html.parser')
name = soup.find('h1', class_='title').text.strip() if soup.find('h1', class_='title') else "未找到标题"
print(req.text)
print(name)

"""
问题： lang=“en-US”  导致解析出 just a moment 内容
使用headers设置中文请求头 也不行

"""