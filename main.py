import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                           QStackedWidget, QLineEdit, QSpinBox, QMessageBox,
                           QFileDialog, QComboBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import asyncio
import edge_tts
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

# 爬虫工作线程
class CrawlerWorker(QThread):
    progress = pyqtSignal(str)  # 用于发送进度信息
    finished = pyqtSignal()     # 用于发送完成信号
    error = pyqtSignal(str)     # 用于发送错误信息
    
    def __init__(self, url_template, chapter_count, output_dir):
        super().__init__()
        self.url_template = url_template
        self.chapter_count = chapter_count
        self.output_dir = output_dir
        
    def run(self):
        try:
            from crawl4ai import AsyncWebCrawler
            
            async def crawl():
                os.makedirs(self.output_dir, exist_ok=True)
                
                async with AsyncWebCrawler() as crawler:
                    for i in range(1, self.chapter_count + 1):
                        try:
                            url = self.url_template.format(i=i)
                            result = await crawler.arun(url=url)
                            
                            file_path = os.path.join(self.output_dir, f"{i}.txt")
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(result.markdown)
                                
                            self.progress.emit(f"成功保存第{i}章到: {file_path}")
                        except Exception as e:
                            self.error.emit(f"爬取第{i}章失败: {str(e)}")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(crawl())
            loop.close()
        except Exception as e:
            self.error.emit(f"爬虫初始化失败: {str(e)}")
        
        self.finished.emit()

# 文本处理工作线程
class TextProcessWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_dir):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    def run(self):
        try:
            import re
            from pathlib import Path
            
            def extract_zw_content(text):
                pattern = r'zw443sx(.*?)zw443sx'
                matches = re.findall(pattern, text, re.DOTALL)
                return matches[0].strip() if matches else None
            
            input_path = Path(self.input_dir)
            output_path = Path(self.output_dir)
            
            # 确保输出目录存在
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 遍历输入目录中的所有文件
            for input_file in input_path.glob('*'):
                if input_file.is_file():
                    try:
                        # 读取文件内容
                        with open(input_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取内容
                        extracted = extract_zw_content(content)
                        
                        if extracted:
                            # 构建输出文件路径
                            output_file = output_path / input_file.name
                            
                            # 写入提取的内容
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(extracted)
                            self.progress.emit(f"成功处理文件: {input_file.name}")
                        else:
                            self.progress.emit(f"警告: 文件中未找到zw443sx标记 - {input_file.name}")
                            
                    except Exception as e:
                        self.error.emit(f"处理文件 {input_file.name} 时出错: {str(e)}")
        except Exception as e:
            self.error.emit(f"文本处理初始化失败: {str(e)}")
        
        self.finished.emit()

# 章节合并工作线程
class MergeWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_dir, chunk_size):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.chunk_size = chunk_size
    
    def run(self):
        try:
            # 创建输出目录（如果不存在）
            os.makedirs(self.output_dir, exist_ok=True)
            
            # 获取所有txt文件并按数字排序
            files = sorted([f for f in os.listdir(self.input_dir) if f.endswith('.txt') and f[:-4].isdigit()], 
                          key=lambda x: int(x[:-4]))

            # 每chunk_size个文件合并一次
            for i in range(0, len(files), self.chunk_size):
                # 确定合并范围
                start = int(files[i][:-4])
                end = start + self.chunk_size - 1 if i + self.chunk_size - 1 < len(files) else int(files[len(files) - 1][:-4])
                output_filename = f"{start}-{end}.txt"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # 合并文件
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    for j in range(i, min(i + self.chunk_size, len(files))):
                        file_path = os.path.join(self.input_dir, files[j])
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                            outfile.write("\n\n")  # 添加分隔符
                
                self.progress.emit(f"已合并文件到: {output_path}")
            
            # 统计输出目录下的文件数并打印
            merged_files_count = len([f for f in os.listdir(self.output_dir) if os.path.isfile(os.path.join(self.output_dir, f))])
            self.progress.emit(f"合并后文件数: {merged_files_count}")
        except Exception as e:
            self.error.emit(f"合并文件时出错: {str(e)}")
        
        self.finished.emit()

# 摘要生成工作线程
class SummaryWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_dir, api_key):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.api_key = api_key
    
    def run(self):
        try:
            # 确保输出目录存在
            os.makedirs(self.output_dir, exist_ok=True)
            
            # 读取提示词
            prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt.txt")
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
            
            # 初始化API客户端
            client = Ark(api_key=self.api_key)
            
            # 获取所有txt文件
            files = [f for f in os.listdir(self.input_dir) if f.endswith('.txt')]
            
            for filename in files:
                file_path = os.path.join(self.input_dir, filename)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                self.progress.emit(f"----- 处理文件 {filename} ------")
                
                try:
                    # 调用API生成摘要
                    response = client.chat.completions.create(
                        model="doubao-1-5-pro-32k-250115",
                        messages=[
                            {"role": "system", "content": prompt_content},
                            {"role": "user", "content": file_content}
                        ],
                        extra_headers={'x-is-encrypted': 'true'},
                        temperature=0.6,
                        top_p=0.5,
                        max_tokens=1024,
                    )
                    
                    # 保存摘要结果
                    summary_content = response.choices[0].message.content
                    output_path = os.path.join(self.output_dir, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(summary_content)
                    
                    self.progress.emit(f"已保存摘要到 {output_path}")
                    self.progress.emit(f"Token使用 - 提示词: {response.usage.prompt_tokens}, 生成: {response.usage.completion_tokens}")
                except Exception as e:
                    self.error.emit(f"处理 {filename} 时出错: {str(e)}")
        except Exception as e:
            self.error.emit(f"摘要生成初始化失败: {str(e)}")
        
        self.finished.emit()

# 文案润色工作线程
class PolishWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_dir, api_key):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.api_key = api_key
    
    def run(self):
        try:
            # 确保输出目录存在
            os.makedirs(self.output_dir, exist_ok=True)
            
            # 初始化API客户端
            client = Ark(api_key=self.api_key)
            
            # 润色提示词
            prompt_content = """
            - Role: 网文小说文案润色专家
            - Background: 用户需要将网文小说的情节概要转化为适合口语化表达的网文解说文案，以便吸引听众并增强故事的吸引力。
            - Profile: 你是一位在网文小说领域深耕多年、深谙文案魅力的润色大师，对小说情节的把握和语言的转化有着独到的见解，能够将枯燥的情节描述转化为生动、引人入胜的口语化表达。
            - Skills: 你拥有丰富的文学创作经验、敏锐的语言感知能力以及出色的文案润色技巧，能够精准地捕捉情节的亮点，并运用连贯的词汇和口语化的表达方式，让文案更具吸引力和感染力。
            - Goals: 将用户提供的网文小说情节概要进行润色，使其内容保持不变，但语言更加流畅、生动，便于口语化表达，适合网文解说博主使用。
            - Constrains: 保持原文的核心情节和内容不变，避免过度夸张或偏离主题，确保文案的准确性和真实性。
            - OutputFormat: 口语化的文案，使用生动的词汇和连贯的表达，适合网文解说博主的风格。
            - Workflow:
              1. 仔细阅读并理解用户提供的网文小说情节概要。
              2. 提炼情节的关键点，确定需要重点表达的部分。
              3. 运用连贯的词汇和口语化的表达方式，对情节进行重新组织和润色。
              4.不要说开场白，例如，嘿，各位听好了啊   
            """
            
            # 获取所有txt文件
            files = [f for f in os.listdir(self.input_dir) if f.endswith('.txt')]
            
            for filename in files:
                file_path = os.path.join(self.input_dir, filename)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                self.progress.emit(f"----- 润色文件 {filename} -----")
                
                try:
                    # 调用API润色文案
                    resp = client.chat.completions.create(
                        model="doubao-1-5-pro-32k-250115",
                        messages=[
                            {"role": "system", "content": prompt_content},
                            {"role": "user", "content": f"请对以下小说摘要进行润色:\n{file_content}"}
                        ],
                        extra_headers={'x-is-encrypted': 'true'},
                        temperature=0.5,
                        top_p=0.7,
                        max_tokens=2048
                    )
                    
                    # 保存润色结果
                    polished_content = resp.choices[0].message.content
                    output_path = os.path.join(self.output_dir, filename)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(polished_content)
                    
                    self.progress.emit(f"已保存润色结果到 {output_path}")
                    self.progress.emit(f"Token使用 - 提示词: {resp.usage.prompt_tokens}, 生成: {resp.usage.completion_tokens}")
                except Exception as e:
                    self.error.emit(f"处理 {filename} 时出错: {str(e)}")
        except Exception as e:
            self.error.emit(f"文案润色初始化失败: {str(e)}")
        
        self.finished.emit()

# TTS语音合成工作线程
class TTSWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, input_dir, output_dir, voice):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.voice = voice
    
    def run(self):
        try:
            # 确保输出目录存在
            os.makedirs(self.output_dir, exist_ok=True)
            
            async def convert_text_to_speech(text, output_path):
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(output_path)
            
            async def process_files():
                for filename in os.listdir(self.input_dir):
                    if filename.endswith('.txt'):
                        input_path = os.path.join(self.input_dir, filename)
                        output_filename = filename.replace('.txt', '.mp3')
                        output_path = os.path.join(self.output_dir, output_filename)
                        
                        try:
                            with open(input_path, 'r', encoding='utf-8') as f:
                                text = f.read()
                                self.progress.emit(f"正在处理: {filename}")
                                await convert_text_to_speech(text, output_path)
                                self.progress.emit(f"已生成: {output_path}")
                        except Exception as e:
                            self.error.emit(f"处理文件 {filename} 时出错: {str(e)}")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(process_files())
            loop.close()
        except Exception as e:
            self.error.emit(f"TTS初始化失败: {str(e)}")
        
        self.finished.emit()

# 主应用窗口
class NovelProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("网络小说智能摘要系统")
        self.setMinimumSize(1000, 600)
        
        # 创建主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # 左侧导航栏
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_widget.setMaximumWidth(200)
        
        # 创建功能按钮
        self.btn_crawl = QPushButton("小说爬取")
        self.btn_clean = QPushButton("文本清洗")
        self.btn_merge = QPushButton("章节合并")
        self.btn_summary = QPushButton("生成摘要")
        self.btn_polish = QPushButton("文案润色")
        self.btn_tts = QPushButton("语音合成")
        
        # 添加按钮到导航栏
        nav_layout.addWidget(self.btn_crawl)
        nav_layout.addWidget(self.btn_clean)
        nav_layout.addWidget(self.btn_merge)
        nav_layout.addWidget(self.btn_summary)
        nav_layout.addWidget(self.btn_polish)
        nav_layout.addWidget(self.btn_tts)
        nav_layout.addStretch()
        
        # 右侧内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # 创建堆叠窗口用于切换不同功能页面
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)
        
        # 创建各功能页面
        self.create_crawl_page()
        self.create_clean_page()
        self.create_merge_page()
        self.create_summary_page()
        self.create_polish_page()
        self.create_tts_page()
        
        # 将导航栏和内容区域添加到主布局
        layout.addWidget(nav_widget)
        layout.addWidget(content_widget, 1)  # 内容区域占据更多空间
        
        # 连接信号和槽
        self.connect_signals()
        
        # 加载环境变量
        load_dotenv()
        self.api_key = os.environ.get("ARK_API_KEY", "")
    
    def create_crawl_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加输入控件
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("小说URL模板:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("例如: https://www.beqege.cc/16750/22333{i}.html")
        url_layout.addWidget(self.url_input)
        
        chapter_layout = QHBoxLayout()
        chapter_layout.addWidget(QLabel("章节数量:"))
        self.chapter_spin = QSpinBox()
        self.chapter_spin.setRange(1, 10000)
        self.chapter_spin.setValue(100)
        chapter_layout.addWidget(self.chapter_spin)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.crawl_output_dir = QLineEdit()
        self.crawl_output_dir.setText(os.path.join(os.path.dirname(os.path.abspath(__file__)), "1_novel"))
        output_layout.addWidget(self.crawl_output_dir)
        self.btn_browse_crawl = QPushButton("浏览...")
        output_layout.addWidget(self.btn_browse_crawl)
        
        # 添加开始按钮
        self.start_crawl_btn = QPushButton("开始爬取")
        
        # 添加进度条
        self.crawl_progress = QProgressBar()
        self.crawl_progress.setRange(0, 1000)  # 不确定进度模式
        self.crawl_progress.setVisible(False)
        
        # 添加日志显示区域
        self.crawl_log = QTextEdit()
        self.crawl_log.setReadOnly(True)
        
        # 将所有控件添加到布局
        layout.addLayout(url_layout)
        layout.addLayout(chapter_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.start_crawl_btn)
        layout.addWidget(self.crawl_progress)
        layout.addWidget(self.crawl_log)
        
        self.content_stack.addWidget(page)
    
    def create_clean_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加输入控件
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入目录:"))
        self.clean_input_dir = QLineEdit()
        input_layout.addWidget(self.clean_input_dir)
        self.btn_browse_clean_input = QPushButton("浏览...")
        input_layout.addWidget(self.btn_browse_clean_input)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.clean_output_dir = QLineEdit()
        output_layout.addWidget(self.clean_output_dir)
        self.btn_browse_clean_output = QPushButton("浏览...")
        output_layout.addWidget(self.btn_browse_clean_output)
        
        # 添加开始按钮
        self.start_clean_btn = QPushButton("开始清洗")
        
        # 添加进度条
        self.clean_progress = QProgressBar()
        self.clean_progress.setRange(0, 0)  # 不确定进度模式
        self.clean_progress.setVisible(False)
        
        # 添加日志显示区域
        self.clean_log = QTextEdit()
        self.clean_log.setReadOnly(True)
        
        # 将所有控件添加到布局
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.start_clean_btn)
        layout.addWidget(self.clean_progress)
        layout.addWidget(self.clean_log)
        
        self.content_stack.addWidget(page)
    
    def create_merge_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加输入控件
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入目录:"))
        self.merge_input_dir = QLineEdit()
        input_layout.addWidget(self.merge_input_dir)
        self.btn_browse_merge_input = QPushButton("浏览...")
        input_layout.addWidget(self.btn_browse_merge_input)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.merge_output_dir = QLineEdit()
        output_layout.addWidget(self.merge_output_dir)
        self.btn_browse_merge_output = QPushButton("浏览...")
        output_layout.addWidget(self.btn_browse_merge_output)
        
        chunk_layout = QHBoxLayout()
        chunk_layout.addWidget(QLabel("合并章节数:"))
        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(1, 100)
        self.chunk_spin.setValue(10)
        chunk_layout.addWidget(self.chunk_spin)
        
        # 添加开始按钮
        self.start_merge_btn = QPushButton("开始合并")
        
        # 添加进度条
        self.merge_progress = QProgressBar()
        self.merge_progress.setRange(0, 0)  # 不确定进度模式
        self.merge_progress.setVisible(False)
        
        # 添加日志显示区域
        self.merge_log = QTextEdit()
        self.merge_log.setReadOnly(True)
        
        # 将所有控件添加到布局
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addLayout(chunk_layout)
        layout.addWidget(self.start_merge_btn)
        layout.addWidget(self.merge_progress)
        layout.addWidget(self.merge_log)
        
        self.content_stack.addWidget(page)
    
    def create_summary_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加输入控件
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入目录:"))
        self.summary_input_dir = QLineEdit()
        input_layout.addWidget(self.summary_input_dir)
        self.btn_browse_summary_input = QPushButton("浏览...")
        input_layout.addWidget(self.btn_browse_summary_input)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.summary_output_dir = QLineEdit()
        output_layout.addWidget(self.summary_output_dir)
        self.btn_browse_summary_output = QPushButton("浏览...")
        output_layout.addWidget(self.btn_browse_summary_output)
        
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API密钥:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 添加开始按钮
        self.start_summary_btn = QPushButton("开始合并")
        
        # 添加进度条
        self.summary_progress = QProgressBar()
        self.summary_progress.setRange(0, 0)  # 不确定进度模式
        self.summary_progress.setVisible(False)
        
        # 添加日志显示区域
        self.summary_log = QTextEdit()
        self.summary_log.setReadOnly(True)
        
        # 将所有控件添加到布局
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.start_summary_btn)
        layout.addWidget(self.summary_progress)
        layout.addWidget(self.summary_log)
        
        self.content_stack.addWidget(page)
    
    def create_polish_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加输入控件
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入目录:"))
        self.polish_input_dir = QLineEdit()
        input_layout.addWidget(self.polish_input_dir)
        self.btn_browse_polish_input = QPushButton("浏览...")
        input_layout.addWidget(self.btn_browse_polish_input)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.polish_output_dir = QLineEdit()
        output_layout.addWidget(self.polish_output_dir)
        self.btn_browse_polish_output = QPushButton("浏览...")
        output_layout.addWidget(self.btn_browse_polish_output)
        
        # 添加开始按钮
        self.start_polish_btn = QPushButton("开始清洗")
        
        # 添加进度条
        self.polish_progress = QProgressBar()
        self.polish_progress.setRange(0, 0)  # 不确定进度模式
        self.polish_progress.setVisible(False)
        
        # 添加日志显示区域
        self.polish_log = QTextEdit()
        self.polish_log.setReadOnly(True)
        
        # 将所有控件添加到布局
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.start_polish_btn)
        layout.addWidget(self.polish_progress)
        layout.addWidget(self.polish_log)
        
        self.content_stack.addWidget(page)
    
    def create_tts_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 添加输入控件
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入目录:"))
        self.tts_input_dir = QLineEdit()
        input_layout.addWidget(self.tts_input_dir)
        self.btn_browse_tts_input = QPushButton("浏览...")
        input_layout.addWidget(self.btn_browse_tts_input)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.tts_output_dir = QLineEdit()
        output_layout.addWidget(self.tts_output_dir)
        self.btn_browse_tts_output = QPushButton("浏览...")
        output_layout.addWidget(self.btn_browse_tts_output)
        
        # 添加开始按钮
        self.start_tts_btn = QPushButton("开始合成")
        
        # 添加进度条
        self.tts_progress = QProgressBar()
        self.tts_progress.setRange(0, 0)  # 不确定进度模式
        self.tts_progress.setVisible(False)
        
        # 添加日志显示区域
        self.tts_log = QTextEdit()
        self.tts_log.setReadOnly(True)
        
        # 将所有控件添加到布局
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.start_tts_btn)
        layout.addWidget(self.tts_progress)
        layout.addWidget(self.tts_log)
        
        self.content_stack.addWidget(page)
        
        # 连接信号和槽
        self.connect_signals()

    # 在NovelProcessorApp类中添加connect_signals方法
    def connect_signals(self):
        # 导航按钮连接到切换页面
        self.btn_crawl.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.btn_clean.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.btn_merge.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
        self.btn_summary.clicked.connect(lambda: self.content_stack.setCurrentIndex(3))
        self.btn_polish.clicked.connect(lambda: self.content_stack.setCurrentIndex(4))
        self.btn_tts.clicked.connect(lambda: self.content_stack.setCurrentIndex(5))
        
        # 浏览按钮连接到选择目录函数
        self.btn_browse_crawl.clicked.connect(lambda: self.browse_directory(self.crawl_output_dir))
        self.btn_browse_clean_input.clicked.connect(lambda: self.browse_directory(self.clean_input_dir))
        self.btn_browse_clean_output.clicked.connect(lambda: self.browse_directory(self.clean_output_dir))
        self.btn_browse_merge_input.clicked.connect(lambda: self.browse_directory(self.merge_input_dir))
        self.btn_browse_merge_output.clicked.connect(lambda: self.browse_directory(self.merge_output_dir))
        self.btn_browse_summary_input.clicked.connect(lambda: self.browse_directory(self.summary_input_dir))
        self.btn_browse_summary_output.clicked.connect(lambda: self.browse_directory(self.summary_output_dir))
        self.btn_browse_polish_input.clicked.connect(lambda: self.browse_directory(self.polish_input_dir))
        self.btn_browse_polish_output.clicked.connect(lambda: self.browse_directory(self.polish_output_dir))
        self.btn_browse_tts_input.clicked.connect(lambda: self.browse_directory(self.tts_input_dir))
        self.btn_browse_tts_output.clicked.connect(lambda: self.browse_directory(self.tts_output_dir))
        
        # 开始按钮连接到相应的功能
        self.start_crawl_btn.clicked.connect(self.start_crawling)
        self.start_clean_btn.clicked.connect(self.start_cleaning)
        self.start_merge_btn.clicked.connect(self.start_merging)
        self.start_summary_btn.clicked.connect(self.start_summarizing)
        self.start_polish_btn.clicked.connect(self.start_polishing)
        self.start_tts_btn.clicked.connect(self.start_tts)
        
        # 设置默认目录关联
        self.crawl_output_dir.textChanged.connect(lambda: self.update_related_dir(self.crawl_output_dir, self.clean_input_dir))
        self.clean_output_dir.textChanged.connect(lambda: self.update_related_dir(self.clean_output_dir, self.merge_input_dir))
        self.merge_output_dir.textChanged.connect(lambda: self.update_related_dir(self.merge_output_dir, self.summary_input_dir))
        self.summary_output_dir.textChanged.connect(lambda: self.update_related_dir(self.summary_output_dir, self.polish_input_dir))
        self.polish_output_dir.textChanged.connect(lambda: self.update_related_dir(self.polish_output_dir, self.tts_input_dir))
    
    # 添加目录浏览功能
    def browse_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "选择目录", line_edit.text())
        if directory:
            line_edit.setText(directory)
    
    # 添加关联目录更新功能
    def update_related_dir(self, source, target):
        if not target.text() or target.text() == "":
            target.setText(source.text())
    
    # 添加爬虫功能实现
    def start_crawling(self):
        url_template = self.url_input.text()
        chapter_count = self.chapter_spin.value()
        output_dir = self.crawl_output_dir.text()
        
        if not url_template or "{i}" not in url_template:
            QMessageBox.warning(self, "输入错误", "请输入有效的URL模板，包含{i}作为章节号占位符")
            return
        
        # 清空日志并显示进度条
        self.crawl_log.clear()
        self.crawl_progress.setVisible(True)
        self.crawl_progress.setRange(0, chapter_count)
        self.crawl_progress.setValue(0)
        self.start_crawl_btn.setEnabled(False)
        
        # 创建并启动工作线程
        self.crawler_worker = CrawlerWorker(url_template, chapter_count, output_dir)
        self.crawler_worker.progress.connect(self.update_crawl_log)
        self.crawler_worker.error.connect(self.update_crawl_error)
        self.crawler_worker.finished.connect(self.on_crawl_finished)
        self.crawler_worker.start()
    
    def update_crawl_log(self, message):
        self.crawl_log.append(message)
        # 更新进度条
        current = self.crawl_progress.value()
        self.crawl_progress.setValue(current + 1)
    
    def update_crawl_error(self, error):
        self.crawl_log.append(f"<span style='color:red'>{error}</span>")
    
    def on_crawl_finished(self):
        self.crawl_log.append("<b>爬取完成!</b>")
        self.start_crawl_btn.setEnabled(True)
    
    # 添加文本清洗功能实现
    def start_cleaning(self):
        input_dir = self.clean_input_dir.text()
        output_dir = self.clean_output_dir.text()
        
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, "输入错误", "请选择有效的输入目录")
            return
        
        # 清空日志并显示进度条
        self.clean_log.clear()
        self.clean_progress.setVisible(True)
        self.start_clean_btn.setEnabled(False)
        
        # 创建并启动工作线程
        self.text_worker = TextProcessWorker(input_dir, output_dir)
        self.text_worker.progress.connect(self.update_clean_log)
        self.text_worker.error.connect(self.update_clean_error)
        self.text_worker.finished.connect(self.on_clean_finished)
        self.text_worker.start()
    
    def update_clean_log(self, message):
        self.clean_log.append(message)
    
    def update_clean_error(self, error):
        self.clean_log.append(f"<span style='color:red'>{error}</span>")
    
    def on_clean_finished(self):
        self.clean_log.append("<b>文本清洗完成!</b>")
        self.start_clean_btn.setEnabled(True)
        self.clean_progress.setVisible(False)
    
    # 添加章节合并功能实现
    def start_merging(self):
        input_dir = self.merge_input_dir.text()
        output_dir = self.merge_output_dir.text()
        chunk_size = self.chunk_spin.value()
        
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, "输入错误", "请选择有效的输入目录")
            return
        
        # 清空日志并显示进度条
        self.merge_log.clear()
        self.merge_progress.setVisible(True)
        self.start_merge_btn.setEnabled(False)
        
        # 创建并启动工作线程
        self.merge_worker = MergeWorker(input_dir, output_dir, chunk_size)
        self.merge_worker.progress.connect(self.update_merge_log)
        self.merge_worker.error.connect(self.update_merge_error)
        self.merge_worker.finished.connect(self.on_merge_finished)
        self.merge_worker.start()
    
    def update_merge_log(self, message):
        self.merge_log.append(message)
    
    def update_merge_error(self, error):
        self.merge_log.append(f"<span style='color:red'>{error}</span>")
    
    def on_merge_finished(self):
        self.merge_log.append("<b>章节合并完成!</b>")
        self.start_merge_btn.setEnabled(True)
        self.merge_progress.setVisible(False)
    
    # 添加摘要生成功能实现
    def start_summarizing(self):
        input_dir = self.summary_input_dir.text()
        output_dir = self.summary_output_dir.text()
        api_key = self.api_key_input.text() or self.api_key
        
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, "输入错误", "请选择有效的输入目录")
            return
        
        if not api_key:
            QMessageBox.warning(self, "API密钥缺失", "请在环境变量或输入框中提供ARK_API_KEY")
            return
        
        # 清空日志并显示进度条
        self.summary_log.clear()
        self.summary_progress.setVisible(True)
        self.start_summary_btn.setEnabled(False)
        
        # 创建并启动工作线程
        self.summary_worker = SummaryWorker(input_dir, output_dir, api_key)
        self.summary_worker.progress.connect(self.update_summary_log)
        self.summary_worker.error.connect(self.update_summary_error)
        self.summary_worker.finished.connect(self.on_summary_finished)
        self.summary_worker.start()
    
    def update_summary_log(self, message):
        self.summary_log.append(message)
    
    def update_summary_error(self, error):
        self.summary_log.append(f"<span style='color:red'>{error}</span>")
    
    def on_summary_finished(self):
        self.summary_log.append("<b>摘要生成完成!</b>")
        self.start_summary_btn.setEnabled(True)
        self.summary_progress.setVisible(False)
    
    # 添加文案润色功能实现
    def start_polishing(self):
        input_dir = self.polish_input_dir.text()
        output_dir = self.polish_output_dir.text()
        api_key = self.api_key
        
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, "输入错误", "请选择有效的输入目录")
            return
        
        if not api_key:
            QMessageBox.warning(self, "API密钥缺失", "请在环境变量中提供ARK_API_KEY")
            return
        
        # 清空日志并显示进度条
        self.polish_log.clear()
        self.polish_progress.setVisible(True)
        self.start_polish_btn.setEnabled(False)
        
        # 创建并启动工作线程
        self.polish_worker = PolishWorker(input_dir, output_dir, api_key)
        self.polish_worker.progress.connect(self.update_polish_log)
        self.polish_worker.error.connect(self.update_polish_error)
        self.polish_worker.finished.connect(self.on_polish_finished)
        self.polish_worker.start()
    
    def update_polish_log(self, message):
        self.polish_log.append(message)
    
    def update_polish_error(self, error):
        self.polish_log.append(f"<span style='color:red'>{error}</span>")
    
    def on_polish_finished(self):
        self.polish_log.append("<b>文案润色完成!</b>")
        self.start_polish_btn.setEnabled(True)
        self.polish_progress.setVisible(False)
    
    # 添加TTS功能实现
    def start_tts(self):
        input_dir = self.tts_input_dir.text()
        output_dir = self.tts_output_dir.text()
        voice = "zh-CN-XiaoxiaoNeural"  # 默认使用小小的声音
        
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, "输入错误", "请选择有效的输入目录")
            return
        
        # 清空日志并显示进度条
        self.tts_log.clear()
        self.tts_progress.setVisible(True)
        self.start_tts_btn.setEnabled(False)
        
        # 创建并启动工作线程
        self.tts_worker = TTSWorker(input_dir, output_dir, voice)
        self.tts_worker.progress.connect(self.update_tts_log)
        self.tts_worker.error.connect(self.update_tts_error)
        self.tts_worker.finished.connect(self.on_tts_finished)
        self.tts_worker.start()
    
    def update_tts_log(self, message):
        self.tts_log.append(message)
    
    def update_tts_error(self, error):
        self.tts_log.append(f"<span style='color:red'>{error}</span>")
    
    def on_tts_finished(self):
        self.tts_log.append("<b>语音合成完成!</b>")
        self.start_tts_btn.setEnabled(True)
        self.tts_progress.setVisible(False)

# 添加在文件末尾
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NovelProcessorApp()
    window.show()
    sys.exit(app.exec())