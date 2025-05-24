import uvicorn
from fastapi import Body, FastAPI, Query,HTTPException
from pydantic import BaseModel
import traceback
app = FastAPI()
import threading
from utils.plugin_manager import PluginManager
from PySide6.QtCore import *
from utils.pluginbase import *
from loguru import logger
from fastapi import Depends
from Server import HttpClient
import  time
import webbrowser
plugin_manager = None

async def get_plugin_manager():
    global plugin_manager
    if not plugin_manager:
        plugin_manager = PluginManager()
        await plugin_manager.load_plugins()
    return plugin_manager
@app.post("/callback")     
async def msg_cb(msg: Msg = Body(description="微信消息"),plugin_manager: PluginManager = Depends(get_plugin_manager)):
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
            else:
                logger.info(msg)

        result = await plugin_manager.process_message(msg)
        return {
            "status": 0,
            "message": "处理成功",
            "results": result["results"]
        }
    except:
        logger.error(traceback.format_exc())
        return {"status": 1, "message": "失败"}
    
@app.get("/plugins")
async def list_plugins():
    """获取所有插件列表"""
    return PluginManager.get_plugins()


def run():
    client = HttpClient()
    settings = QSettings("config.ini", QSettings.IniFormat)
    设备id =settings.value("DeviceID")
    if 设备id == None:
        设备id = client.获取二维码('')['DeviceId']
        settings.setValue("DeviceID",设备id)
        
    机器人id = settings.value("wxid")
    if client.wx心跳(机器人id):
        logger.info('心跳成功')
        client.定时回调接口()
    else:
        获取登录 = client.获取二维码(设备id)
        uuid = 获取登录['Data']['Uuid']
        二维码 = 获取登录['Data']['QrUrl']
        logger.info('二维码链接'+二维码)
        webbrowser.open(二维码)
        for _ in range(300):
            if uuid == 0:
                break
            time.sleep(3)
            机器人id = client.检测二维码(uuid)
            if 机器人id:
                logger.info('登录成功')
                client.定时回调接口()#启动回调接口
                client.开启自动心跳自动二次登录(机器人id)
                settings.setValue("wxid",机器人id)
                break
    uvicorn.run(app, host="127.0.0.1", port=8000)
if __name__ == "__main__":
    run()

    
