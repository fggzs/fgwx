'''
Author: 飞哥
Description: QQ群917830969
Date: 2024-09-20 17:43:21
LastEditTime: 2025-05-01 19:22:24
'''

import uvicorn
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel
import traceback
import requests,time
from loguru import logger
import os,sys
import json,signal
app = FastAPI()

# TRACE: 最低级别的日志，用于非常详细的调试信息。在生产环境中通常不会使用。
# DEBUG: 用于调试目的的详细输出。它通常包含有关代码执行状态和变量值的信息。
# INFO: 提供一般的信息性消息，用于确认正常的程序执行流程。
# SUCCESS: 表示成功的操作或任务完成的消息。
# WARNING: 表示潜在问题或非致命错误的消息。程序可能会继续运行，但可能会导致一些意外结果。
# ERROR: 表示可恢复的错误或异常情况的消息，可能会导致程序无法继续执行特定的功能。
# CRITICAL: 表示严重错误或导致程序无法正常运行的消息。它可能表示失败的关键任务或系统崩溃。在这种级别下，通常需要紧急采取行动。
os.makedirs("./log",exist_ok=True)#如果没有就创建
if sys.gettrace() is not None:
    logger.add(f"./log/log.log", rotation="10 MB", backtrace=True, diagnose=True, level="DEBUG", retention=5)
else:
    logger.add(f"./log/log.log", rotation="10 MB", backtrace=True, diagnose=True, level="INFO", retention=5)
    
    
def checkPort(port: int) -> str:
    try:
        res_list = []
        # 判断端口是否被占用，占用直接把占用端口的进程给杀掉
        with os.popen(f'netstat -aon|findstr "{port}"') as res:
            res = res.read().split('\n')
            for line in res:
                temp = [i for i in line.split(' ') if i != '']
                if len(temp) > 4 and int(temp[4]) > 1:
                    res_list.append(temp[4])
                
        if len(res_list) > 0:
            for i in res_list:
                os.kill(int(i), signal.SIGINT)
                logger.success(f"杀死占用端口的进程成功，该进程pid：{i}")
                tip = "被占用端口" + str(port) + "的进程成功清理，该进程pid：" + str(i)
                print(tip)

        else:
            tip = str(port) + "端口没有被占用，无需清理"
            logger.info(tip)
    except:
        logger.error(traceback.format_exc())
class Msg(BaseModel):
    """微信消息
    Attributes:
        type (int): 消息类型，可通过 `get_msg_types` 获取
        id (str): 消息 id
        ts (int):时间戳
        xml (str): 消息 xml 部分
        sender (str): 消息发送人
        roomid (str): （仅群消息有）群 id
        content (str): 消息内容
        thumb (str): 视频或图片消息的缩略图路径
        extra (str): 视频或图片消息的路径
        is_self(bool): 是否是自己发送的消息
        is_group(bool):是否是群消息
    """
    id: int
    ts: int
    sign: str
    type: int
    xml: str
    sender: str
    roomid: str
    content: str
    thumb: str
    extra: str
    is_at: bool
    is_self: bool
    is_group: bool
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
def 获取完整通讯录():
    url = "http://localhost:9999/contacts"

    response = requests.get(url, headers=headers).json()
    
    return response    
def 获取群成员名片(wxid, roomid):
    
    url = "http://localhost:9999/alias-in-chatroom"
    params={
        "wxid": wxid,
        "roomid": roomid}
    response = requests.get(url,params=params, headers=headers).json()
    return response
def 发送文本(text,receiver,aters=''):
    """ 
    msg (str): 要发送的消息，换行使用 `\\n`；如果 @ 人的话，需要带上跟 `aters` 里数量相同的 @
    receiver (str): 消息接收人，wxid 或者 roomid
    aters (str): 要 @ 的 wxid，多个用逗号分隔；`@所有人` 只需要 `notify@all` 
    """
    url = "http://localhost:9999/text"
    ats = ""
    if aters:
        if aters == "notify@all":  # @所有人
            ats = " @所有人"
        else:
            wxids = aters.split(",")
            for wxid in wxids:
                # 根据 wxid 查找群昵称
                ats += f"@{获取群成员名片(wxid, receiver)['data']['alias']}"

    if ats != "":
        text = f"{ats}\n{text}"

    logger.debug(f"To {receiver}: {ats}\r{text}")
    data = json.dumps({
    "msg": text,
    "receiver": receiver,
    "aters": aters})
    response = requests.post(url, headers=headers,data=data).json()
    logger.info(response)
    return response
    
def 系统设置(msg):
    管理员 = 系统配置['管理员']
    if 管理员:
        #查询群id，微信id
        if '查询-' in msg.content and msg.sender in 管理员:
            content = msg.content.replace('查询-','')
            通讯录 = 获取完整通讯录()["data"]["contacts"]
            for key in 通讯录:
                wxid = key["wxid"]
                name = key["name"]
                if content in name:
                    发送文本(f'{name} {wxid}',msg.sender,'')
            发送文本('查询完成',msg.sender,'')   
    return
 
@app.post("/callback")     
async def msg_cb(msg: Msg = Body(description="微信消息")):
    try:
        if msg.is_self:#是否是自己发送的消息
            return
        if msg.is_group:#是否是群消息
            logger.info({'type':msg.type,'ts':msg.ts,'sender':msg.sender,'roomid':msg.roomid,'content':msg.content})
        else:
            if msg.type == 49:#xml类型
                logger.info({'type':msg.type,'ts':msg.ts,'sender':msg.sender,'xml':msg.xml})
            if msg.type == 1: #文本类型   
                logger.info({'type':msg.type,'ts':msg.ts,'sender':msg.sender,'content':msg.content}) 
                系统设置(msg)
                
        return {"status": 0, "message": "成功"}
    except:
        logger.error(traceback.format_exc())
        发送文本('服务器异常',msg.sender)
        发送文本(f'机器人异常:{traceback.format_exc()}',管理员[0],'')
        return {"status": 1, "message": "失败"}


if __name__ == "__main__":
    """ 先启动接口版.exe，再运行此代码接收消息 """
    # http://127.0.0.1:9999/docs 接口文档
    checkPort(8000)
    系统配置 =  {"管理员":[""]}#第一个是主人
    管理员 = 系统配置['管理员']
    if sys.gettrace() is None:
       发送文本('启动成功',管理员[0],'')
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
    