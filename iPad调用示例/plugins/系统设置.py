from pluginbase import *
from Server import Server
import pyautogui

class 系统设置(PluginBase):
    def __init__(self):
        self.metadata = {
            "name": "系统设置功能",
            "version": "1.0.0",
            "author": "fg",
            "description": "示例插件",
            "priority": 50,
            "block": False
        }
        self.enabled = True
        self.server = Server()
    async def process(self, msg: Msg):

        if msg.type == 1:
            await self.系统设置(msg)

    async def 系统设置(self, msg: Msg):

        if '服务器运行图' in msg.content:
            screenshot = pyautogui.screenshot()  
            screenshot.save('D:\screenshot.png')
            self.server.发送图片('D:\screenshot.png',msg.sender)
        return
    async def on_load(self):
        """插件加载时执行的逻辑"""
        print(f"Plugin {self.metadata['name']} loaded successfully.")
