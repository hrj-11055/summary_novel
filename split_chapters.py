import re

# 输入文件路径
input_file_path = 'c:/Users/Administrator/Desktop/summary_novel/2_aoshi/1501-2000.txt'

# 读取文件内容
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正则表达式匹配章节
chapter_pattern = re.compile(r'第[一二三四五六七八九十百千]+章 .*?\n')
chapters = chapter_pattern.split(content)[1:]
chapter_titles = chapter_pattern.findall(content)

# 每5个章节写入一个文件
for i in range(0, len(chapters), 5):
    start_index = i + 1
    end_index = min(i + 5, len(chapters))
    output_file_name = f'{start_index}-{end_index}.txt'
    output_file_path = 'c:/Users/Administrator/Desktop/summary_novel/2_aoshi_split/' + output_file_name

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for j in range(start_index - 1, end_index):
            output_file.write(chapter_titles[j])
            output_file.write(chapters[j])

print('章节拆分完成！')