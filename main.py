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
from Server import Server
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
    settings = QSettings("config.ini", QSettings.IniFormat)
    #调度器初始化
    settings.setValue("scheduler_started",False)
    # checkPort(8000)
    设备id =settings.value("DeviceID")
    if not 设备id:
        设备id = str(uuid.uuid4()).replace("-", "")
        settings.setValue("DeviceID",设备id)
        
    机器人id = settings.value("wxid")
    server = Server()#实例化

    if server.wx心跳(机器人id):
        server.二次登录()
        server.回调接口()
    else:
        机器人id = server.ipad登录(设备id)
        if not 机器人id:
            logger.error("登录失败")
            os._exit(0)
        #保存机器人id
        settings.setValue("wxid",机器人id)
    
if __name__ == "__main__":
    run()

    
