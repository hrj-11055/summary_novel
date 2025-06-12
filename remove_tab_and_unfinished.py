import os

folder_path = 'c:/Users/Administrator/Desktop/summary_novel/2_meinv'

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 修正点：使用双反斜杠匹配字面量\t
            new_content = content.replace('\\t', '').replace('（未完待续）', '')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

print('处理完成！')