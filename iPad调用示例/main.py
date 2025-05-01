import uvicorn
from fastapi import Body, FastAPI
import traceback
app = FastAPI()
import threading
from plugin_manager import PluginManager
from PySide6.QtCore import *
from pluginbase import *
from Server import Server    
import uuid
import os
from loguru import logger
import os,sys
# TRACE: 最低级别的日志，用于非常详细的调试信息。在生产环境中通常不会使用。
# DEBUG: 用于调试目的的详细输出。它通常包含有关代码执行状态和变量值的信息。
# INFO: 提供一般的信息性消息，用于确认正常的程序执行流程。
# SUCCESS: 表示成功的操作或任务完成的消息。
# WARNING: 表示潜在问题或非致命错误的消息。程序可能会继续运行，但可能会导致一些意外结果。
# ERROR: 表示可恢复的错误或异常情况的消息，可能会导致程序无法继续执行特定的功能。
# CRITICAL: 表示严重错误或导致程序无法正常运行的消息。它可能表示失败的关键任务或系统崩溃。在这种级别下，通常需要紧急采取行动。
os.makedirs("./logs",exist_ok=True)#如果没有就创建
logger.add(f"./logs/log.log", rotation="10 MB", backtrace=True, diagnose=True, level="INFO", retention=5)
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
            elif msg.type == 1: #文本类型   
                logger.info({'type':msg.type,'ts':msg.ts,'sender':msg.sender,'content':msg.content}) 
                # await 系统设置(msg)
            else:
                logger.info(msg)

        # await 转发.转发自动跑(msg)
        plugin_manager = PluginManager()
        await plugin_manager.initialize() 
        result = await plugin_manager.process_message(msg)
        return {
            "status": 0,
            "message": "处理成功",
            "results": result["results"]
        }
    except:
        logger.error(traceback.format_exc())
        server.发送文本('服务器异常',msg.sender)
        return {"status": 1, "message": "失败"}
    
@app.get("/plugins")
async def list_plugins():
    """获取所有插件列表"""
    return PluginManager.get_plugins()

    
if __name__ == "__main__":
    settings = QSettings("config.ini", QSettings.IniFormat)
    设备id =settings.value("DeviceID")
    if not 设备id:
        设备id = str(uuid.uuid4()).replace("-", "")
        settings.setValue("DeviceID",设备id)
    机器人id = settings.value("wxid")
    server = Server()#实例化
    if server.wx心跳(机器人id):
        server.回调接口()
    else:
        机器人id = server.ipad登录(设备id)
        if not 机器人id:
            logger.error("登录失败")
            os._exit(0)
        #保存机器人id
        settings.setValue("wxid",机器人id)
    threading.Thread(target=server.启动心跳检测,args=(机器人id,)).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
