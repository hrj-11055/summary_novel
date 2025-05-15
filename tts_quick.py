import asyncio
import edge_tts
""" 用于快速文本转语音，测试新文案的TTS后的，  方便选用不同Voice"""
async def text_to_speech(
    text: str = """
    域外少女说：“哎呀呀，妹妹，你们是双胞胎啊，我才发现！” 
    月婵盯着清漪，心里那叫一个纠结。石昊问清漪：“清漪，你最近怎样，去了哪里？” 
    清漪说：“我还好。”
    
    石昊提起：“你忘了曾对我说的话了吗，有一个约定。” 
    清漪装傻：“什么约定？” 
    石昊笑道：“你曾说过，我若是进入仙古遗迹后独占鳌头，天下第一，你要怎样做？” 
    清漪脸 “唰” 地就红了，耍赖说忘了。石昊嘿嘿笑着：“你曾说过，我在仙古夺得天下第一名后，你会以身相许。” 
    清漪瞪他：“哪有！” 石昊抓住她的手臂：“喂，说话要算话。” 
    月婵低声斥道：“放手！” 石昊揽住清漪的腰，看着月婵：“关你什么事情，你确信要跟我们一同进入天神书院？”

    石昊还厚着脸皮问：“清漪，你上次不告而别，是不是…… 有了？” 
    月婵气得浑身发抖，清漪呵斥道：“你不要乱说话！” 
    石昊大笑：“好，我们私下里说。” 接着就开始和清漪传音。
    """,
    voice: str = "zh-CN-YunxiNeural",  # 中文语音模型
    output: str = "output.mp3",
    rate: str = "+15%",  # 语速调整
    volume: str = "+20%"  # 音量调整
):
    """快速文本转语音函数"""
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume
    )
    await communicate.save(output)
    print(f"语音文件已生成: {output}")

if __name__ == '__main__':
    asyncio.run(text_to_speech())