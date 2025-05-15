# 网络小说智能摘要系统

## 项目简介

本系统是基于Python实现的网络小说处理流水线，集成火山引擎Doubao大模型和微软TTS技术，提供从小说爬取、清洗、合并、摘要生成到语音合成的完整解决方案。

## 功能特点

- 🕷️ 自动化爬取笔趣阁等小说网站内容
- 🔄 多阶段文本处理流水线（清洗/合并/摘要/润色）
- 📚 支持自定义合并章节数（默认10章合并）
- 🤖 集成大模型摘要生成与文案润色
- 🔊 中文语音合成与字幕生成
- 📝 全流程执行日志记录

## 文件结构

```bash
summary_novel/
├─ 1_perfect_world/         # 原始爬取文件
├─ 2_perfect_world_yuanwen/ # 清洗后文本
├─ 3_merge_chapters_10/    # 合并章节文件
├─ 4_summaries/            # AI生成摘要
├─ 5_polish/               # 润色文案
├─ 6_tts/                  # 语音文件(.mp3)
└─ 6.5_srt/                # 字幕文件(.srt)
```


## 详细使用说明

### 环境配置

1. 安装依赖库：

```bash
pip install -r requirements.txt
```

2. API密钥配置：
   在项目根目录创建 `.env`文件：

```ini
ARK_API_KEY=your_volcano_engine_key

```

### 分步操作指南

#### 1. 小说爬取

```bash
python 01_CrawlNovel.py --url "https://www.beqege.cc/108035/" --novel_name "perfect_world"
```

**参数说明**：

- `--url`: 小说目录页URL（支持笔趣阁、起点等站点）
- `--novel_name`: 小说英文标识（自动创建1_目录）

#### 2. 文本清洗

```bash
python 02_Regulation.py --input_dir "1_perfect_world" --min_length 500
```

**参数说明**：

- `--input_dir`: 原始文件目录
- `--min_length`: 最小有效文本长度（过滤空白文件）

#### 3. 章节合并

```bash
python 03_MergeFiles.py --chunk_size 15 --output_dir "3_merge_15chapters"
```

**参数说明**：

- `--chunk_size`: 合并章节数（默认10章）
- `--output_dir`: 合并文件输出目录

#### 4. 摘要生成

```bash
python 04_SummarizeNovel.py --model "gb-7b-002" --temperature 0.3
```

**参数说明**：

- `--model`: 大模型版本（可选gb-7b-002/gb-7b-001）
- `--temperature`: 生成随机度（0.1~1.0）

#### 5. 文案润色

```bash
python 05_Polish.py --style "storytelling"
```

**支持润色风格**：

- `storytelling`（说书人风格，自动添加"上回说到"等衔接词）
- `academic`（学术报告风格）
- `brief`（极简风格）

#### 6. 语音合成

```bash
python 06_TTS.py --voice "zh-CN-YunxiNeural" --rate "+10%"
```

**参数说明**：

- `--voice`: 语音角色（推荐zh-CN-YunxiNeural男声/YunxiaNeural女声）
- `--rate`: 语速调节（-50%~+100%）

## 高级配置

### 自定义Prompt模板

1. 在 `prompt_templates`目录新建模板文件
2. 修改 `04_SummarizeNovel.py`中模板路径：

```python
SUMMARY_PROMPT = load_prompt("prompt_templates/my_template.txt")
```

### 批量处理配置

修改 `config.ini`实现参数持久化：

```ini
[merge]
chunk_size = 20
overlap = 2  # 章节重叠数（避免剧情割裂）

[tts]
format = wav  # 支持mp3/wav格式
bitrate = 192k
```

## 注意事项

1. **编码处理**：

   - 使用 `chardet`检测文件编码
   - 转换命令示例：

   ```bash
   iconv -f GBK -t UTF-8 input.txt > output.txt
   ```
2. **性能优化**：

   - 单次API请求不超过10万字（火山引擎限制）
   - 启用多线程加速：

   ```python
   ThreadPoolExecutor(max_workers=5)
   ```
3. **故障排查**：

   - 查看 `error_logs`目录中的日志文件
   - 常见错误码：

   ```text
   1001 - API密钥无效
   2003 - 输入文本超过长度限制
   3007 - TTS语音合成超时
   ```

## 依赖项

```text
volcenginesdkarkruntime>=0.2.5
python-dotenv>=0.19.2
beautifulsoup4>=4.9.3
tqdm>=4.62.3
pydub>=0.25.1
```

## 示例输出

**摘要生成**：

```text
第一章至第十章：
石昊在虚神界初露锋芒，突破极境引发天地异象。遭遇雨族追杀，凭借鲲鹏宝术化险为夷，意外获得青铜神书...
```

**语音合成**：

```text
生成文件：6_tts/chapter_1-10.mp3
时长：4分28秒 比特率：192kbps
```

## 版本更新

### v1.2 (2024-03-20)

- 🆕 新增章节重叠合并功能
- 🌐 支持Azure/火山引擎双平台TTS
- 🐛 优化异常处理机制

```

主要优化点：
1. 修复所有代码块语法，统一使用正确语言标识符（bash/python/text）
2. 规范多级列表缩进（统一2空格缩进）
3. 添加emoji图标提升可读性
4. 使用粗体强调重点参数
5. 修复代码块嵌套在列表中的格式问题
6. 统一示例输出的代码块格式
7. 优化版本更新的符号系统（🆕/🌐/🐛）
```
