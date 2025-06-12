#!/usr/bin/env python3
"""批量从文本文件生成语音文件"""

import asyncio
import os
import edge_tts

INPUT_FOLDER = r"C:\Users\Administrator\Desktop\summary_novel\4_summaries_10"
#OUTPUT_FOLDER = r"C:\Users\Administrator\Desktop\summary_novel\6_tts"
VOICE = "zh-CN-YunxiNeural"  # 中文语音
# VOICE = "zh-CN-XiaoxiaoNeural"  # 中文语音
# VOICE = "zh-CN-XiaoyiNeural"
# VOICE = "zh-CN-YunjianNeural"
# VOICE = "zh-CN-YunxiaNeural"
# VOICE = "zh-CN-XiaoxiaoNeural"
# VOICE = "zh-CN-XiaoyiNeural"
# VOICE = "zh-CN-YunjianNeural"
# VOICE = "zh-CN-YunxiaNeural"
# VOICE = "zh-CN-liaoning-XiaobeiNeural"
# VOICE = "zh-CN-shaanxi-XiaoniNeural"  
# VOICE = "zh-CN-YunyangNeural"
# zh-CN-liaoning-XiaobeiNeural
# zh-CN-shaanxi-XiaoniNeural
# zh-HK-HiuGaaiNeural
# zh-HK-HiuMaanNeural
# zh-HK-WanLungNeural
# zh-TW-HsiaoChenNeural
# zh-TW-HsiaoYuNeural
# zh-TW-YunJheNeural
# zu-ZA-ThandoNeural
# zu-ZA-ThembaNeural
async def convert_text_to_speech(text: str, output_path: str) -> None:
    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate="+10%",
        volume="+10%",
        pitch="+10Hz"
    )
    subs = edge_tts.SubMaker()
    # 创建音频文件和字幕文件
    async with communicate.stream() as stream:
        # 保存音频
        with open(output_path, "wb") as audio_file:
            async for chunk in stream:
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    subs.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    # 生成SRT字幕
    srt_path = output_path.replace('.mp3', '.srt')
    with open(srt_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(subs.generate_subs())

# 修改输出目录常量
OUTPUT_FOLDER = r"C:\Users\Administrator\Desktop\summary_novel\7_srt"

async def process_files() -> None:
    """处理文件夹中的所有文本文件"""
    # 确保输出目录存在
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    # 这里需要添加遍历文件并调用 convert_text_to_speech 的逻辑
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                output_mp3_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(file)[0] + '.mp3')
                await convert_text_to_speech(text, output_mp3_path)

if __name__ == '__main__':
    asyncio.run(process_files())