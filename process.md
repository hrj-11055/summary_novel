graph TD
    A[crawl4.py爬取网络小说] --> B[保存到1_perfect_world目录]
    B --> C[正则化.py处理文本]
    C --> D[保存到2_perfect_world_yuanwen目录]
    D --> E[merge_files.py合并章节]
    E --> F[保存到3_merge_charter目录]
    F --> G[summarize_novel.py总结内容]
    G --> H[保存到4_summaries目录]
    G --> I[测试不同prompt总结能力]
