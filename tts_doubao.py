#coding=utf-8

'''
requires Python 3.6 or later

pip install asyncio
pip install websockets

'''

import asyncio
import websockets
import uuid
import json
import gzip
import copy
import os

# 创建保存MP3文件的目录
MP3_DIR = "8_doubao_tts_mp3"
if not os.path.exists(MP3_DIR):
    os.makedirs(MP3_DIR)

# 读取文本文件
TEXT_FILE = r"C:\Users\Administrator\Desktop\summary_novel\5_polish\11-20.txt"
try:
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        text_content = f.read().strip()
except Exception as e:
    print(f"读取文件失败: {e}")
    text_content = "文件读取失败，使用默认文本。"

# 消息类型定义
MESSAGE_TYPES = {11: "audio-only server response", 12: "frontend server response", 15: "error message from server"}
MESSAGE_TYPE_SPECIFIC_FLAGS = {0: "no sequence number", 1: "sequence number > 0",
                               2: "last message from server (seq < 0)", 3: "sequence number < 0"}
MESSAGE_SERIALIZATION_METHODS = {0: "no serialization", 1: "JSON", 15: "custom type"}
MESSAGE_COMPRESSIONS = {0: "no compression", 1: "gzip", 15: "custom compression method"}

# 需要填写的参数
appid = "3096860082"        # 字节跳动开放平台的应用ID 3096860082
token = "CXiIqi6OTmozcD4h76ZrunxSBlUbXldm"        # 访问令牌
cluster = "volcano_tts"      # 集群信息
voice_type = "zh_male_jieshuoxiaoming_moon_bigtts"   # 语音类型
host = "openspeech.bytedance.com"
api_url = f"wss://{host}/api/v1/tts/ws_binary"

# version: b0001 (4 bits)
# header size: b0001 (4 bits)
# message type: b0001 (Full client request) (4bits)
# message type specific flags: b0000 (none) (4bits)
# message serialization method: b0001 (JSON) (4 bits)
# message compression: b0001 (gzip) (4bits)
# reserved data: 0x00 (1 byte)
default_header = bytearray(b'\x11\x10\x11\x00')

# 请求JSON模板
request_json = {
    "app": {
        "appid": appid,
        "token": token,
        "cluster": cluster
    },
    "user": {
        "uid": "388808087185088"  # 用户ID，可以自定义
    },
    "audio": {
        "voice_type": voice_type,      # 语音类型
        "encoding": "mp3",        # 音频编码格式
        "speed_ratio": 1.2,       # 语速比例
        "volume_ratio": 1.0,      # 音量比例
        "pitch_ratio": 1.0,       # 音调比例
    },
    "request": {
        "reqid": str(uuid.uuid4()),           # 请求ID，使用UUID自动生成
        "text": text_content,  # 从文件中读取的文本
        "text_type": "plain",     # 文本类型
        "operation": "submit"        # 操作类型，默认使用submit
    }
}

async def test_submit():
    """
    测试提交语音合成请求
    功能：向服务器发送语音合成请求，并接收合成的音频数据
    输出：将合成的音频保存为 8_doubao_tts_mp3/test_submit.mp3
    """
    submit_request_json = copy.deepcopy(request_json)
    submit_request_json["audio"]["voice_type"] = voice_type
    submit_request_json["request"]["reqid"] = str(uuid.uuid4())
    submit_request_json["request"]["operation"] = "submit"
    payload_bytes = str.encode(json.dumps(submit_request_json))
    payload_bytes = gzip.compress(payload_bytes)  # if no compression, comment this line
    full_client_request = bytearray(default_header)
    full_client_request.extend((len(payload_bytes)).to_bytes(4, 'big'))  # payload size(4 bytes)
    full_client_request.extend(payload_bytes)  # payload
    print("\n------------------------ test 'submit' -------------------------")
    print("request json: ", submit_request_json)
    print("\nrequest bytes: ", full_client_request)
    file_to_save = open(os.path.join(MP3_DIR, "test_submit.mp3"), "wb")
    header = {"Authorization": f"Bearer; {token}"}
    async with websockets.connect(api_url, additional_headers=header, ping_interval=None) as ws:
        await ws.send(full_client_request)
        while True:
            res = await ws.recv()
            done = parse_response(res, file_to_save)
            if done:
                file_to_save.close()
                break
        print("\nclosing the connection...")

async def test_query():
    """
    测试查询语音合成状态
    功能：向服务器查询语音合成的状态
    输出：将查询结果保存为 8_doubao_tts_mp3/test_query.txt
    """
    query_request_json = copy.deepcopy(request_json)
    query_request_json["audio"]["voice_type"] = voice_type
    query_request_json["request"]["reqid"] = str(uuid.uuid4())
    query_request_json["request"]["operation"] = "query"
    payload_bytes = str.encode(json.dumps(query_request_json))
    payload_bytes = gzip.compress(payload_bytes)  # if no compression, comment this line
    full_client_request = bytearray(default_header)
    full_client_request.extend((len(payload_bytes)).to_bytes(4, 'big'))  # payload size(4 bytes)
    full_client_request.extend(payload_bytes)  # payload
    print("\n------------------------ test 'query' -------------------------")
    print("request json: ", query_request_json)
    print("\nrequest bytes: ", full_client_request)
    file_to_save = open(os.path.join(MP3_DIR, "test_query.txt"), "wb")
    header = {"Authorization": f"Bearer; {token}"}
    async with websockets.connect(api_url, additional_headers=header, ping_interval=None) as ws:
        await ws.send(full_client_request)
        res = await ws.recv()
        parse_response(res, file_to_save)
        file_to_save.close()
        print("\nclosing the connection...")

def parse_response(res, file):
    """
    解析服务器响应
    参数：
        res: 服务器返回的原始响应数据
        file: 用于保存音频数据的文件对象
    返回：
        bool: 如果处理完成返回True，否则返回False
    功能：
        解析服务器返回的二进制数据，提取音频数据并保存到文件
    """
    print("--------------------------- response ---------------------------")
    # print(f"response raw bytes: {res}")
    protocol_version = res[0] >> 4
    header_size = res[0] & 0x0f
    message_type = res[1] >> 4
    message_type_specific_flags = res[1] & 0x0f
    serialization_method = res[2] >> 4
    message_compression = res[2] & 0x0f
    reserved = res[3]
    header_extensions = res[4:header_size*4]
    payload = res[header_size*4:]
    print(f"            Protocol version: {protocol_version:#x} - version {protocol_version}")
    print(f"                 Header size: {header_size:#x} - {header_size * 4} bytes ")
    print(f"                Message type: {message_type:#x} - {MESSAGE_TYPES[message_type]}")
    print(f" Message type specific flags: {message_type_specific_flags:#x} - {MESSAGE_TYPE_SPECIFIC_FLAGS[message_type_specific_flags]}")
    print(f"Message serialization method: {serialization_method:#x} - {MESSAGE_SERIALIZATION_METHODS[serialization_method]}")
    print(f"         Message compression: {message_compression:#x} - {MESSAGE_COMPRESSIONS[message_compression]}")
    print(f"                    Reserved: {reserved:#04x}")
    if header_size != 1:
        print(f"           Header extensions: {header_extensions}")
    if message_type == 0xb:  # audio-only server response
        if message_type_specific_flags == 0:  # no sequence number as ACK
            print("                Payload size: 0")
            return False
        else:
            sequence_number = int.from_bytes(payload[:4], "big", signed=True)
            payload_size = int.from_bytes(payload[4:8], "big", signed=False)
            payload = payload[8:]
            print(f"             Sequence number: {sequence_number}")
            print(f"                Payload size: {payload_size} bytes")
        file.write(payload)
        if sequence_number < 0:
            return True
        else:
            return False
    elif message_type == 0xf:
        code = int.from_bytes(payload[:4], "big", signed=False)
        msg_size = int.from_bytes(payload[4:8], "big", signed=False)
        error_msg = payload[8:]
        if message_compression == 1:
            error_msg = gzip.decompress(error_msg)
        error_msg = str(error_msg, "utf-8")
        print(f"          Error message code: {code}")
        print(f"          Error message size: {msg_size} bytes")
        print(f"               Error message: {error_msg}")
        return True
    elif message_type == 0xc:
        msg_size = int.from_bytes(payload[:4], "big", signed=False)
        payload = payload[4:]
        if message_compression == 1:
            payload = gzip.decompress(payload)
        print(f"            Frontend message: {payload}")
    else:
        print("undefined message type!")
        return True

if __name__ == '__main__':
    asyncio.run(test_submit())  # 执行提交测试
    asyncio.run(test_query())   # 执行查询测试
