import asyncio
import os
import edge_tts
'''
给定一篇文章，用不同的语音生成
用于筛选适合的语音
小说解说，普遍用 zh-CN-YunxiNeural yunjian yunyang
知识分享， 用谁呢？
歌曲抒情， ？
'''
OUTPUT_FOLDER = r"C:\Users\Administrator\Desktop\summary_novel\test"
async def process_files() -> None:
    # 固定输入文件路径
    input_file = r"C:\Users\Administrator\Desktop\summary_novel\5_polish\31-40.txt"
    
    # 多语音配置（从06_TTS.py中提取所有可用语音）
    # "zh-HK-HiuGaaiNeural",
    # "zh-HK-HiuMaanNeural",
    # "zh-HK-WanLungNeural",
    # "zh-TW-HsiaoChenNeural",
    # "zh-TW-HsiaoYuNeural",
    # "zh-TW-YunJheNeural"
    VOICES = [
        "zh-CN-YunxiNeural",    # 小说解说 男 云希 ！！！！！！！
        "zh-CN-XiaoxiaoNeural", # 少年晓晓 女
        "zh-CN-YunjianNeural",  # 解说 男 云间  ！！！！！！！！
        #"zh-CN-YunxiaNeural",
        #"zh-CN-liaoning-XiaobeiNeural",
        #"zh-CN-shaanxi-XiaoniNeural",   # 
        "zh-CN-YunyangNeural",  # 气泡声男  ！！！！
        
    ]

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
        print(f"正在处理固定文件: {input_file}")
        
        for voice in VOICES:
            output_filename = os.path.basename(input_file).replace('.txt', f'_{voice.split('-')[-1]}.mp3')
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            try:
                communicate = edge_tts.Communicate(text, voice,rate="+10%", volume="+10%", pitch="+10Hz")
                await communicate.save(output_path)
                print(f"已生成语音文件: {output_path}")
            except Exception as e:
                print(f"语音合成失败({voice}): {e}")

if __name__ == "__main__":
    asyncio.run(process_files())