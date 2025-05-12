# 网络小说智能摘要系统

## 项目简介

这是一个自动化处理网络小说的工具，主要功能包括：

1. 爬取网络小说内容
2. 调用大模型API对小说章节进行智能摘要
3. 生成精简的情节概要

## 功能特点

- 支持批量处理小说章节文件
- 使用火山引擎Doubao大模型进行文本摘要
- 自动记录API调用情况和token消耗
- 支持自定义prompt模板

## 文件结构

```
summary_novel/
├── summarize_novel.py        # 主程序，处理小说摘要
├── tool-script/              # 辅助工具脚本
│   └── extract_first_100_files.py  # 文件提取工具
├── 3_merge_chapters_part/    # 输入文件夹(原始小说章节)
└── 4_summaries_good/         # 输出文件夹(生成摘要)
```

## 使用说明

1. 准备环境：

```bash
pip install -r requirements.txt
```

2. 配置API密钥：
   在 `.env`文件中设置：

```
ARK_API_KEY=your_api_key_here
```

3. 运行主程序：

```bash
python summarize_novel.py
```

## 注意事项

- 确保输入文件为UTF-8编码
- 大模型API调用需要网络连接
- 建议先在小批量文件上测试

## 示例输出

生成的摘要文件将保存在 `4_summaries_good`文件夹中，保持与原文件相同的文件名。

## 依赖项

- Python 3.7+
- volcenginesdkarkruntime
- python-dotenv



根据我查看的项目文件结构，这是一个小说摘要处理项目，主要包含以下文件和目录：

1. *1_xianni\* 目录

- 包含大量.txt文件（1.txt到267.txt等）
- 这些是原始小说章节文件，由爬虫从网站抓取

2. ** 2_xianni_yuanwen ** 目录

- 包含处理后的完整小说文本文件
- 由regulation.py处理原始文件生成

3. **3_merge_chapters_10\** 目录

- 包含合并后的章节文件
- 由merge_files.py将10个章节合并为一个文件生成

4. **4_summaries_10\** 目录

- 存放小说章节的AI摘要结果
- 由summarize_novel.py或summarize_novel_V2.py生成

主要代码文件功能：

<mcfile name="regulation.py" path="c:\Users\Administrator\Desktop\summary_novel\regulation.py"></mcfile>
- 从原始文件中提取zw443sx标记之间的正文内容
- 处理1_xianni目录中的文件，输出到2_xianni_yuanwen目录

<mcfile name="merge_files.py" path="c:\Users\Administrator\Desktop\summary_novel\merge_files.py"></mcfile>
- 将多个章节文件合并为单个文件（每10章合并）
- 处理2_xianni_yuanwen目录中的文件，输出到3_merge_chapters_10目录

<mcfile name="summarize_novel.py" path="c:\Users\Administrator\Desktop\summary_novel\summarize_novel.py"></mcfile>
- 使用AI API生成小说章节摘要
- 主要功能包括：
  - 检查API可用性
  - 读取文件内容
  - 记录API使用情况
  - 处理单个文件生成摘要

<mcfile name="summarize_novel_V2.py" path="c:\Users\Administrator\Desktop\summary_novel\summarize_novel_V2.py"></mcfile>
- summarize_novel.py的改进版本
- 添加了多线程批量处理功能
- 优化了API调用和日志记录

<mcfile name="crawl4.py" path="c:\Users\Administrator\Desktop\summary_novel\crawl4.py"></mcfile>
- 网络爬虫脚本
- 从特定网站抓取小说章节内容
- 保存到1_xianni目录

工具脚本（tool-script目录）：

- count_words.py - 统计文件字数
- extract_first_100_files.py - 提取前100个文件
- pachong_douban250.py - 豆瓣电影Top250爬虫
- test*.py - 各种测试脚本

其他文件：

- prompt.txt - AI提示词模板
- api_usage.log - API使用日志
- .env - 环境变量文件（存储API密钥等）
