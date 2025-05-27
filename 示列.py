import asyncio
import websockets
import json
from pydantic import BaseModel 
import re
from FgwxApi.HttpClient import HttpClient
from loguru import logger
import traceback
import os,sys
from PySide6.QtCore import *
from utils.plugin_manager import PluginManager
import time
# TRACE: 最低级别的日志，用于非常详细的调试信息。在生产环境中通常不会使用。
# DEBUG: 用于调试目的的详细输出。它通常包含有关代码执行状态和变量值的信息。
# INFO: 提供一般的信息性消息，用于确认正常的程序执行流程。
# SUCCESS: 表示成功的操作或任务完成的消息。
# WARNING: 表示潜在问题或非致命错误的消息。程序可能会继续运行，但可能会导致一些意外结果。
# ERROR: 表示可恢复的错误或异常情况的消息，可能会导致程序无法继续执行特定的功能。
# CRITICAL: 表示严重错误或导致程序无法正常运行的消息。它可能表示失败的关键任务或系统崩溃。在这种级别下，通常需要紧急采取行动。
os.makedirs("./logs",exist_ok=True)#如果没有就创建
if sys.gettrace() is not None:
    logger.add(f"./logs/log.log", rotation="10 MB", backtrace=True, diagnose=True, level="DEBUG", retention=5)
else:
    logger.add(f"./logs/log.log", rotation="10 MB", backtrace=True, diagnose=True, level="INFO", retention=5)


class Msg(BaseModel):
    """微信消息
    Attributes:
        type (int): 消息类型，可通过 `get_msg_types` 获取
        id (str): 消息 id
        ts (int):时间戳
        sender (str): 消息发送人
        roomid (str): （仅群消息有）群 id
        content (str): 消息内容
        str (str): 图片消息的base64编码
        is_self(bool): 是否是自己发送的消息
        is_group(bool):是否是群消息
    """
    id: int
    ts: int
    sign: str
    type: int
    sender: str
    roomid: str
    content: str
    img: str
    is_at: bool
    is_self: bool
    is_group: bool
    


def process_message(msg_data,mywxid="wxid_3mpvw4k0b2t722") -> Msg:
    """将原始消息转换"""
    # 提取基础字段
    from_user_name = msg_data.get("from_user_name", {}).get("str", "")
    to_user_name = msg_data.get("to_user_name", {}).get("str", "") #接收人id
    content = msg_data.get("content", {}).get("str", "")
    
    sign=""
    msg_source = msg_data.get("msg_source", "")
    if msg_source:
        # 使用正则表达式提取signature
        match = re.search(r'<signature>([^<]+)</signature>', msg_source)
        if match:
            sign = match.group(1)
    
    # 处理发送人和内容
    sender = from_user_name
    if ":" in content and "@chatroom" in from_user_name:
        parts = content.split(":", 1)
        if parts:
            sender = parts[0].strip()
            content = parts[1].strip() if len(parts) > 1 else content
    
    # 判断是否是群聊
    is_group = "@chatroom" in from_user_name
    room_id = from_user_name if is_group else ""
    
    # 判断是否是自己发送的消息
    is_self = False
    if mywxid:
        if is_group:
            is_self = sender == mywxid
        else:
            is_self = from_user_name == mywxid
    
    # 判断是否被@
    is_at = False
    if is_group and not is_self:
        msg_source = msg_data.get("msg_source", "")
        if msg_source and isinstance(msg_source, str):
            # 简化处理，实际可能需要更复杂的解析
            if f"{to_user_name}" in msg_source or "@所有人" in msg_source:
                is_at = True
    
    # 处理特殊字段
    img = ""
    img_buf = msg_data.get("img_buf", {})
    if img_buf.get("len", 0) > 0:
        img = img_buf['buffer']
    
    return Msg(
        id=int(msg_data.get("msg_id", 0)),
        ts=int(msg_data.get("create_time", 0)),
        sign=sign,
        type=int(msg_data.get("msg_type", 0)),
        sender=sender,
        roomid=room_id,
        content=content,
        img=img,
        is_at=is_at,
        is_self=is_self,
        is_group=is_group,
    )

async def receive_messages(plugin_manager:PluginManager):
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("成功连接到WSS服务器")
            await plugin_manager.load_plugins()
            while True:
                try:
                    message = await websocket.recv()
                    message = json.loads(message)
                    msg = process_message(message)
                    logger.info(msg)
                    await plugin_manager.process_message(msg)
                except websockets.ConnectionClosed:
                    print("连接已关闭")
                    break
                    
    except:
        logger.error(traceback.format_exc())
def 登录():
    登录链接 = client.login_获取登录二维码异地IP用代理()['Data']['QrCodeUrl']
    print(登录链接)
    while True:
        if client.login_检测扫码状态()['Data']['status'] == 2:
            print("登录成功")
            break
        else:
            print("登录中")
        time.sleep(3)
if __name__ == "__main__":
    settings = QSettings("config.ini", QSettings.IniFormat)
    api_url =settings.value("api_url")
    wxid = settings.value("wxid")
    key = settings.value("key")
    WS_URL = settings.value("WS_URL")
    client = HttpClient(wxid=wxid,api_url=api_url,key=key)
    登录()
    
    asyncio.get_event_loop().run_until_complete(receive_messages(PluginManager()))