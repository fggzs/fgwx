from loguru import logger
import requests
import json
import webbrowser
import time
import base64
from PySide6.QtCore import *
import os

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
class Server:
    def __init__(self):
        settings = QSettings("config.ini", QSettings.IniFormat)
        self.机器人id = settings.value("wxid")
        self.interface_url = 'http://127.0.0.1:9999/api'
    def 发送文本(self,text,receiver,aters=''):
        """ 
        msg (str): 要发送的消息，换行使用 `\\n`；如果 @ 人的话，需要带上跟 `aters` 里数量相同的 @
        receiver (str): 消息接收人，wxid 或者 roomid
        aters (str): 要 @ 的 wxid，多个用逗号分隔；`@所有人` 只需要 `notify@all` 
        """
        ats = ""
        if aters:
            if aters == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = aters.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f"@{self.获取群成员名片(wxid, receiver)['data']['alias']}"
        if ats != "":
            text = f"{ats}\n{text}"
        url = self.interface_url +"/Msg/SendTxt"
        data =json.dumps({
        "At": aters,
        "Content": text,
        "ToWxid": receiver,
        "Type": 1,
        "Wxid": self.机器人id
        })
        response = requests.post(url, headers=headers,data=data).json()
        logger.debug(response)
        return response
    def 获取群成员名片(self,wxid, roomid):
        response = self.获取成员详情(roomid)
        for member in response:
            if member["UserName"] == wxid:
                return {"data":{"alias":member["NickName"]}}
        return response
    def 获取成员详情(self,roomid):
        url = self.interface_url +"/Group/GetChatRoomMemberDetail"
        data=json.dumps({
            "QID": roomid,
            "Wxid": self.机器人id})
        response = requests.post(url,data=data, headers=headers).json()
        return response["Data"]["NewChatroomData"]["ChatRoomMember"]
    def 获取二维码(self,DeviceID):
        url = self.interface_url +"/Login/GetQRx"
        data = json.dumps({
        "DeviceID": DeviceID,
        "DeviceName": "iPad",
        "Proxy": {
            "ProxyIp": "",
            "ProxyPassword": "",
            "ProxyUser": ""
        }
        })
        response = requests.post(url,data=data, headers=headers)
        logger.debug(response.json()['Message'])
        return response.json()

    # 检测二维码
    def 检测二维码(self,uuid):
        url = self.interface_url +"/Login/CheckQR"
        params = {
            "uuid": uuid,
        }
        
        response = requests.post(url,params=params, headers=headers).json()
        logger.debug(response['Message'])
        if response['Message'] == '登陆成功':
            self.机器人id = response['Data']['acctSectResp']['userName']
            return self.机器人id 
        return ''

    #/Login/HeartBeatLong
    def wx心跳(self,wxid):
        url = self.interface_url +"/Login/HeartBeatLong"
        params = {
            "wxid": wxid ,
        }
        response = requests.post(url,params=params, headers=headers)
        if response.json()['Success']:
            self.机器人id = wxid
            return True
        return False
    def 回调接口(self):
        url = self.interface_url+"/Msg/SyncCallback"
        params = {
            "interval": 3,
            "callback": "http://127.0.0.1:8000/callback"
        }
        data = json.dumps({
            "Scene": 0,
            "Synckey": "",
            "Wxid": self.机器人id
        })
        response = requests.post(url, headers=headers, params=params, data=data)
        logger.debug(response.json())
        return response.json()

    def ipad登录(self,DeviceID):
        获取登录 = self.获取二维码(DeviceID)
        uuid = 获取登录['Data']['Uuid']
        二维码 = 获取登录['Data']['QrUrl']
        logger.info('二维码链接'+二维码)
        webbrowser.open(二维码)
        for _ in range(300):
            if uuid == 0:
                break
            time.sleep(3)
            wxid = self.检测二维码(uuid)
            if wxid:
                logger.info('登录成功')
                self.回调接口()#启动回调接口
                return wxid
        return False
    def 启动心跳检测(self,机器人id):
        while True:
            time.sleep(30)
            if not self.wx心跳(机器人id):
                os._exit(0)
            

    def 发送图片(self,path,receiver):

        url = self.interface_url +"/Msg/UploadImg"
        with open(path, 'rb') as f:
            Base64 = base64.b64encode(f.read()).decode('utf-8')  
        data = json.dumps({
            "Base64": Base64,
            "ToWxid": receiver,
            "Wxid": self.机器人id
            })

        response = requests.post(url, headers=headers,data=data).json()
        logger.debug(response)
        return response
