#!/usr/bin/env python3
"""批量从文本文件生成语音文件"""

import asyncio
import os
import edge_tts

INPUT_FOLDER = r"C:\Users\Administrator\Desktop\summary_novel\5_polish"
OUTPUT_FOLDER = r"C:\Users\Administrator\Desktop\summary_novel\6_tts_srt"
#VOICE = "zh-CN-YunxiNeural"  # 中文语音
# VOICE = "zh-CN-XiaoxiaoNeural"  # 中文语音
# VOICE = "zh-CN-XiaoyiNeural"
# VOICE = "zh-CN-YunjianNeural"
VOICE = "zh-CN-YunxiaNeural"
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
    """将文本转换为语音并保存为MP3"""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

async def process_files() -> None:
    """处理文件夹中的所有文本文件"""
    # 确保输出目录存在
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.txt'):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_filename = filename.replace('.txt', '.mp3')
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    print(f"正在处理: {filename}")
                    await convert_text_to_speech(text, output_path)
                    print(f"已生成: {output_path}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

if __name__ == "__main__":
    asyncio.run(process_files())