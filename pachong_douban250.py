# 导入必要的库
import requests  # 用于发送HTTP请求
from bs4 import BeautifulSoup  # 用于解析HTML内容

def get_douban_top250():
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',  # 浏览器标识
        'Accept-Language': 'zh-CN,zh;q=0.9'  # 语言偏好设置
    }
    all_movies = []  # 初始化空列表，用于存储所有电影名称
    
    # 分页爬取逻辑（豆瓣每页显示25部电影，共10页）
    for start in range(0, 250, 25):  # start参数从0开始，每次增加25
        # 构造带分页参数的URL
        url = f'https://movie.douban.com/top250?start={start}&filter='
        # 发送GET请求
        resp = requests.get(url, headers=headers)
        
        # 检查请求是否成功（HTTP状态码200表示成功）
        if resp.status_code == 200:
            # 使用BeautifulSoup解析HTML内容，指定解析器为html.parser
            soup = BeautifulSoup(resp.text, 'html.parser')
            # 遍历每个电影条目（CSS选择器选择class为item的元素）
            for item in soup.select('.item'):
                # 提取电影标题（选择class为title的元素，去除前后空格）
                title = item.select_one('.title').text.strip()
                # 将电影标题添加到列表中
                all_movies.append(title)
            # 打印当前页数（start//25 + 1计算当前页码）
            print(f'已获取第{start//25 + 1}页数据')
        else:
            # 如果请求失败，打印错误信息
            print(f'第{start//25 + 1}页请求失败')
    
    # 将结果保存到文件
    with open('douban_top250.txt', 'w', encoding='utf-8') as f:
        # 将电影列表用换行符连接并写入文件
        f.write('\n'.join(all_movies))
    # 打印最终结果统计
    print(f'成功爬取{len(all_movies)}部电影')

# 主程序入口
if __name__ == '__main__':
    # 调用爬虫函数
    get_douban_top250()