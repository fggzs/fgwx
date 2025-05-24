from loguru import logger
import requests
import json
import webbrowser
import time
import base64
from PySide6.QtCore import *
import os
import uuid
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
class HttpClient:
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
        time.sleep(0.5)
        return response
    def 邀请群成员(self,roomid,wxids,机器人id='wxid_ecq4okp3dvta22'):
        url = self.interface_url +"/Group/InviteChatRoomMember"
        data = json.dumps({
        "ChatRoomName": roomid,
        "ToWxids":wxids,
        "Wxid": 机器人id
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
        if not DeviceID:
            DeviceID = str(uuid.uuid4()).replace("-", "")
        url = self.interface_url +"/Login/LoginGetQR"
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
        url = self.interface_url +"/Login/LoginCheckQR"
        params = {
            "uuid": uuid,
        }
        
        response = requests.post(url,params=params, headers=headers).json()
        logger.debug(response['Message'])
        if response['Message'] == '登陆成功':
            self.机器人id = response['Data']['acctSectResp']['userName']
            return self.机器人id 
        return ''


    def 定时回调接口(self,interval=3,callback=""):
        url = self.interface_url+"/Msg/SyncCallback"
        params = {
            "interval": interval,
            "callback": callback
        }
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

    def 发送app消息(self,receiver,appmsg,Type=0):
        url = self.interface_url +"/Msg/SendApp"
        data = json.dumps({
            "ToWxid": receiver,
            "Type": Type,
            "Wxid":self.机器人id,
            "Xml": appmsg
        })
        response = requests.post(url, headers=headers,data=data).json()
        logger.debug(response)
        return response
    def 发送图片(self,path,receiver):
        """ 路径不能为中文 """
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


    

    def 删除收藏(self, FavId, ):
        url = self.interface_url + '/Favor/Del'
        data = {
            'FavId': FavId,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取搜藏信息(self, ):
        url = self.interface_url + '/Favor/GetFavInfo'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 读取收藏内容(self, FavId, ):
        url = self.interface_url + '/Favor/GetFavItem'
        data = {
            'FavId': FavId,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 同步收藏(self, Keybuf, ):
        url = self.interface_url + '/Favor/Sync'
        data = {
            'Keybuf': Keybuf,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 用户中心(self, ):
        url = self.interface_url + '/Finder/UserPrepare'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 添加移除黑名单(self, ToWxid, Val, ):
        url = self.interface_url + '/Friend/Blacklist'
        data = {
            'ToWxid': ToWxid,
            'Val': Val,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 删除好友(self, ToWxid, ):
        url = self.interface_url + '/Friend/Delete'
        data = {
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取通讯录好友详情(self, ChatRoom, Towxids, ):
        url = self.interface_url + '/Friend/GetContractDetail'
        data = {
            'ChatRoom': ChatRoom,
            'Towxids': Towxids,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取通讯录好友(self, CurrentChatRoomContactSeq, CurrentWxcontactSeq, ):
        url = self.interface_url + '/Friend/GetContractList'
        data = {
            'CurrentChatRoomContactSeq': CurrentChatRoomContactSeq,
            'CurrentWxcontactSeq': CurrentWxcontactSeq,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 查询好友状态(self, UserName, ):
        url = self.interface_url + '/Friend/GetFriendstate'
        data = {
            'UserName': UserName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取手机通讯录(self, ):
        url = self.interface_url + '/Friend/GetMFriend'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 附近人(self, Latitude, Longitude, OpCode, ):
        url = self.interface_url + '/Friend/LbsFind'
        data = {
            'Latitude': Latitude,
            'Longitude': Longitude,
            'OpCode': OpCode,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 通过好友请求(self, Scene, V1, V2, ):
        url = self.interface_url + '/Friend/PassVerify'
        data = {
            'Scene': Scene,
            'V1': V1,
            'V2': V2,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 搜索联系人(self, FromScene, SearchScene, ToUserName, ):
        url = self.interface_url + '/Friend/Search'
        data = {
            'FromScene': FromScene,
            'SearchScene': SearchScene,
            'ToUserName': ToUserName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 添加联系人(self, Opcode, Scene, V1, V2, VerifyContent, ):
        url = self.interface_url + '/Friend/SendRequest'
        data = {
            'Opcode': Opcode,
            'Scene': Scene,
            'V1': V1,
            'V2': V2,
            'VerifyContent': VerifyContent,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 设置好友备注(self, Remarks, ToWxid, ):
        url = self.interface_url + '/Friend/SetRemarks'
        data = {
            'Remarks': Remarks,
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 上传通讯录(self, CurrentPhoneNo, Opcode, PhoneNo, ):
        url = self.interface_url + '/Friend/Upload'
        data = {
            'CurrentPhoneNo': CurrentPhoneNo,
            'Opcode': Opcode,
            'PhoneNo': PhoneNo,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 朋友圈点赞评论(self, Content, Id, ReplyCommnetId, Type, ):
        url = self.interface_url + '/FriendCircle/Comment'
        data = {
            'Content': Content,
            'Id': Id,
            'ReplyCommnetId': ReplyCommnetId,
            'Type': Type,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取特定人朋友圈(self, Fristpagemd5, Maxid, Towxid, ):
        url = self.interface_url + '/FriendCircle/GetDetail'
        data = {
            'Fristpagemd5': Fristpagemd5,
            'Maxid': Maxid,
            'Towxid': Towxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取特定ID详情内容(self, Id, Towxid, ):
        url = self.interface_url + '/FriendCircle/GetIdDetail'
        data = {
            'Id': Id,
            'Towxid': Towxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 朋友圈首页列表(self, Fristpagemd5, Maxid, ):
        url = self.interface_url + '/FriendCircle/GetList'
        data = {
            'Fristpagemd5': Fristpagemd5,
            'Maxid': Maxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 发布朋友圈(self, BlackList, Content, WithUserList, ):
        url = self.interface_url + '/FriendCircle/Messages'
        data = {
            'BlackList': BlackList,
            'Content': Content,
            'WithUserList': WithUserList,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 朋友圈同步(self, Synckey, ):
        url = self.interface_url + '/FriendCircle/MmSnsSync'
        data = {
            'Synckey': Synckey,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 朋友圈操作(self, CommnetId, Id, Type, ):
        url = self.interface_url + '/FriendCircle/Operation'
        data = {
            'CommnetId': CommnetId,
            'Id': Id,
            'Type': Type,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 朋友圈权限设置(self, Function, Value, ):
        url = self.interface_url + '/FriendCircle/PrivacySettings'
        data = {
            'Function': Function,
            'Value': Value,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 朋友圈上传(self, Base64, ):
        url = self.interface_url + '/FriendCircle/Upload'
        data = {
            'Base64': Base64,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 增加群成员(self, ChatRoomName, ToWxids, ):
        """ (40人以内) """
        url = self.interface_url + '/Group/AddChatRoomMember'
        data = {
            'ChatRoomName': ChatRoomName,
            'ToWxids': ToWxids,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 同意进入群聊(self, Url, ):
        url = self.interface_url + '/Group/ConsentToJoin'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 创建群聊(self, Latitude, Longitude, OpCode, Password, ):
        url = self.interface_url + '/Group/CreateChatRoom'
        data = {
            'Latitude': Latitude,
            'Longitude': Longitude,
            'OpCode': OpCode,
            'Password': Password,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 删除群成员(self, ChatRoomName, ToWxids, ):
        url = self.interface_url + '/Group/DelChatRoomMember'
        data = {
            'ChatRoomName': ChatRoomName,
            'ToWxids': ToWxids,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取群信息(self, QID, ):
        url = self.interface_url + '/Group/GetChatRoomInfoDetail'
        data = {
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取群成员详情(self, QID, ):
        url = self.interface_url + '/Group/GetChatRoomMemberDetail'
        data = {
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取群二维码(self, QID, ):
        url = self.interface_url + '/Group/GetQRCode'
        data = {
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response


    def 保存到通讯录(self, QID, Val, ):
        url = self.interface_url + '/Group/MoveContractList'
        data = {
            'QID': QID,
            'Val': Val,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 群管理操作(self, QID, ToWxids, Val, ):
        url = self.interface_url + '/Group/OperateChatRoomAdmin'
        data = {
            'QID': QID,
            'ToWxids': ToWxids,
            'Val': Val,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 退出群聊(self, QID, ):
        url = self.interface_url + '/Group/Quit'
        data = {
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 扫码进群(self, Url, ):
        url = self.interface_url + '/Group/ScanIntoGroup'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 扫码进群2(self, Url, ):
        url = self.interface_url + '/Group/ScanIntoGroupEnterprise'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 设置群公告(self, Content, QID, ):
        url = self.interface_url + '/Group/SetChatRoomAnnouncement'
        data = {
            'Content': Content,
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 设置群名称(self, Content, QID, ):
        url = self.interface_url + '/Group/SetChatRoomName'
        data = {
            'Content': Content,
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 设置群备注(self, Content, QID, ):
        url = self.interface_url + '/Group/SetChatRoomRemarks'
        data = {
            'Content': Content,
            'QID': QID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 添加标签(self, LabelName, ):
        url = self.interface_url + '/Label/Add'
        data = {
            'LabelName': LabelName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 删除标签(self, LabelID, ):
        url = self.interface_url + '/Label/Delete'
        data = {
            'LabelID': LabelID,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取标签列表(self, ):
        url = self.interface_url + '/Label/GetList'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 更新标签列表(self, LabelID, ToWxids, ):
        url = self.interface_url + '/Label/UpdateList'
        data = {
            'LabelID': LabelID,
            'ToWxids': ToWxids,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 修改标签(self, LabelID, NewName, ):
        url = self.interface_url + '/Label/UpdateName'
        data = {
            'LabelID': LabelID,
            'NewName': NewName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def wx心跳(self,wxid):
        url = self.interface_url +"/Login/HeartBeat"
        params = {
            "wxid": wxid ,
        }
        response = requests.post(url,params=params, headers=headers)
        if response.json()['Success']:
            self.机器人id = wxid
            return True
        return False
    
    def 开启自动心跳自动二次登录(self, ):
        url = self.interface_url + '/Login/AutoHeartBeat'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 自动心跳日志(self, ):
        url = self.interface_url + '/Login/AutoHeartBeatLog'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 关闭自动心跳自动二次登录(self, ):
        url = self.interface_url + '/Login/CloseAutoHeartBeat'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response




    def 获取登录缓存信息(self, ):
        url = self.interface_url + '/Login/GetCacheInfo'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response


    def 退出登录(self, ):
        url = self.interface_url + '/Login/LogOut'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 唤醒登录(self, ):
        url = self.interface_url + '/Login/LoginAwaken'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response


    def 二次登录(self, ):
        url = self.interface_url + '/Login/LoginTwiceAutoAuth'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 初始化(self, wxid, MaxSynckey, CurrentSynckey):
        url = self.interface_url + '/Login/Newinit'
        params = {
            "Wxid": self.机器人id,
            'MaxSynckey': MaxSynckey,
            'CurrentSynckey': CurrentSynckey,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 提交登录验证码(self, Code, Data62, Ticket, Uuid):
        url = self.interface_url + '/Login/YPayVerificationcode'
        data = {
            'Code': Code,
            'Data62': Data62,
            'Ticket': Ticket,
            'Uuid': Uuid,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 撤回消息(self, ClientMsgId, CreateTime, NewMsgId, ToUserName, ):
        url = self.interface_url + '/Msg/Revoke'
        data = {
            'ClientMsgId': ClientMsgId,
            'CreateTime': CreateTime,
            'NewMsgId': NewMsgId,
            'ToUserName': ToUserName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response





    def 发送Emoji(self, Md5, ToWxid, TotalLen, ):
        url = self.interface_url + '/Msg/SendEmoji'
        data = {
            'Md5': Md5,
            'ToWxid': ToWxid,
            'TotalLen': TotalLen,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response



    def 发送视频(self, Base64, ImageBase64, PlayLength, ToWxid, ):
        url = self.interface_url + '/Msg/SendVideo'
        data = {
            'Base64': Base64,
            'ImageBase64': ImageBase64,
            'PlayLength': PlayLength,
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 发送语音(self, Base64, ToWxid, Type, VoiceTime, ):
        url = self.interface_url + '/Msg/SendVoice'
        data = {
            'Base64': Base64,
            'ToWxid': ToWxid,
            'Type': Type,
            'VoiceTime': VoiceTime,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 分享名片(self, CardAlias, CardNickName, CardWxId, ToWxid, ):
        url = self.interface_url + '/Msg/ShareCard'
        data = {
            'CardAlias': CardAlias,
            'CardNickName': CardNickName,
            'CardWxId': CardWxId,
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 发送分享链接消息(self, ToWxid, Type, Wxid, Xml):
        url = self.interface_url + '/Msg/ShareLink'
        data = {
            'ToWxid': ToWxid,
            'Type': Type,
            "Wxid": self.机器人id,
            'Xml': Xml,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 分享位置(self, Infourl, Label, Poiname, Scale, ToWxid, Wxid, X, Y):
        url = self.interface_url + '/Msg/ShareLocation'
        data = {
            'Infourl': Infourl,
            'Label': Label,
            'Poiname': Poiname,
            'Scale': Scale,
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
            'X': X,
            'Y': Y,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 发送分享视频消息(self, ToWxid, Wxid, Xml):
        url = self.interface_url + '/Msg/ShareVideo'
        data = {
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
            'Xml': Xml,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response



    def 关注(self, Appid, ):
        url = self.interface_url + '/OfficialAccounts/Follow'
        data = {
            'Appid': Appid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 阅读数据(self, Url, ):
        """ 阅读文章,返回分享、看一看、阅读数据 """
        url = self.interface_url + '/OfficialAccounts/GetAppMsgExt'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 阅读数据2(self, Url, ):
        """ 点赞文章,返回分享、看一看、阅读数据 """
        url = self.interface_url + '/OfficialAccounts/GetAppMsgExtLike'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def JSAPIPreVerify(self, Appid, Url, ):
        url = self.interface_url + '/OfficialAccounts/JSAPIPreVerify'
        data = {
            'Appid': Appid,
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def MpGetA8Key(self, Url, ):
        """ (获取文章key和uin) """
        url = self.interface_url + '/OfficialAccounts/MpGetA8Key'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def OauthAuthorize(self, Appid, Url, ):
        url = self.interface_url + '/OfficialAccounts/OauthAuthorize'
        data = {
            'Appid': Appid,
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 取消关注(self, Appid, ):
        url = self.interface_url + '/OfficialAccounts/Quit'
        data = {
            'Appid': Appid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def QWApplyAddContact(self, Context, Username, V1, ):
        url = self.interface_url + '/QWContact/QWApplyAddContact'
        data = {
            'Context': Context,
            'Username': Username,
            'V1': V1,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def QWAddContact(self, Username, V1, ):
        url = self.interface_url + '/QWContact/QWContact/QWAddContact'
        data = {
            'Username': Username,
            'V1': V1,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def SearchQWContact(self, Username, ):
        url = self.interface_url + '/QWContact/SearchQWContact'
        data = {
            'Username': Username,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response



    def 打招呼(self, Scene, V3, V4, VerifyContent, ):
        url = self.interface_url + '/SayHello/Modelv2'
        data = {
            'Scene': Scene,
            'V3': V3,
            'V4': V4,
            'VerifyContent': VerifyContent,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 确认收款(self, InvalidTime, ToUserName, TransFerId, TransactionId, ):
        url = self.interface_url + '/TenPay/Collectmoney'
        data = {
            'InvalidTime': InvalidTime,
            'ToUserName': ToUserName,
            'TransFerId': TransFerId,
            'TransactionId': TransactionId,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 自定义个人收款二维码(self, Money, Name, ):
        url = self.interface_url + '/TenPay/GeMaPayQCode'
        data = {
            'Money': Money,
            'Name': Name,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 自定义经营个人收款单(self, Money, Name, Remark, ):
        url = self.interface_url + '/TenPay/GeMaSkdPayQCode'
        data = {
            'Money': Money,
            'Name': Name,
            'Remark': Remark,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取加密信息(self, ):
        url = self.interface_url + '/TenPay/GetEncryptInfo'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 抢红包(self, SendUserName, Wxid, Xml):
        url = self.interface_url + '/TenPay/OpenHongBao'
        data = {
            'SendUserName': SendUserName,
            "Wxid": self.机器人id,
            'Xml': Xml,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 拆开红包(self, Encrypt_key, Encrypt_userinfo, SendUserName, TimingIdentifier, Wxid, Xml):
        url = self.interface_url + '/TenPay/Openwxhb'
        data = {
            'Encrypt_key': Encrypt_key,
            'Encrypt_userinfo': Encrypt_userinfo,
            'SendUserName': SendUserName,
            'TimingIdentifier': TimingIdentifier,
            "Wxid": self.机器人id,
            'Xml': Xml,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 查看红包(self, Encrypt_key, Encrypt_userinfo, Wxid, Xml):
        url = self.interface_url + '/TenPay/Qrydetailwxhb'
        data = {
            'Encrypt_key': Encrypt_key,
            'Encrypt_userinfo': Encrypt_userinfo,
            "Wxid": self.机器人id,
            'Xml': Xml,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 打开红包(self, Encrypt_key, Encrypt_userinfo, InWay, Wxid, Xml):
        url = self.interface_url + '/TenPay/Receivewxhb'
        data = {
            'Encrypt_key': Encrypt_key,
            'Encrypt_userinfo': Encrypt_userinfo,
            'InWay': InWay,
            "Wxid": self.机器人id,
            'Xml': Xml,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 自定义商家收款单(self, Money, Name, Remark, ):
        url = self.interface_url + '/TenPay/SjSkdPayQCode'
        data = {
            'Money': Money,
            'Name': Name,
            'Remark': Remark,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def CDN下载高清图片(self, FileAesKey, FileNo, ):
        url = self.interface_url + '/Tools/CdnDownloadImage'
        data = {
            'FileAesKey': FileAesKey,
            'FileNo': FileNo,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 文件下载(self, AppID, AttachId, DataLen, Section, UserName, ):
        url = self.interface_url + '/Tools/DownloadFile'
        data = {
            'AppID': AppID,
            'AttachId': AttachId,
            'DataLen': DataLen,
            'Section': Section,
            'UserName': UserName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 高清图片下载(self, CompressType, DataLen, MsgId, Section, ToWxid, ):
        url = self.interface_url + '/Tools/DownloadImg'
        data = {
            'CompressType': CompressType,
            'DataLen': DataLen,
            'MsgId': MsgId,
            'Section': Section,
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 视频下载(self, CompressType, DataLen, MsgId, Section, ToWxid, ):
        url = self.interface_url + '/Tools/DownloadVideo'
        data = {
            'CompressType': CompressType,
            'DataLen': DataLen,
            'MsgId': MsgId,
            'Section': Section,
            'ToWxid': ToWxid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 语音下载(self, Bufid, FromUserName, Length, MsgId, ):
        url = self.interface_url + '/Tools/DownloadVoice'
        data = {
            'Bufid': Bufid,
            'FromUserName': FromUserName,
            'Length': Length,
            'MsgId': MsgId,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 生成支付二维码(self, ):
        url = self.interface_url + '/Tools/GeneratePayQCode'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def GetA8Key(self, CodeType, CodeVersion, CookieBase64, Flag, NetType, OpCode, ReqUrl, Scene, ):
        url = self.interface_url + '/Tools/GetA8Key'
        data = {
            'CodeType': CodeType,
            'CodeVersion': CodeVersion,
            'CookieBase64': CookieBase64,
            'Flag': Flag,
            'NetType': NetType,
            'OpCode': OpCode,
            'ReqUrl': ReqUrl,
            'Scene': Scene,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取余额以及银行卡信息(self, ):
        url = self.interface_url + '/Tools/GetBandCardList'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def GetBoundHardDevices(self, ):
        url = self.interface_url + '/Tools/GetBoundHardDevices'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 获取CDN服务器dns信息(self, ):
        url = self.interface_url + '/Tools/GetCdnDns'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def OauthSdkApp(self, Appid, AvatarId, Opt, State, Wxid, packageName, sdkName):
        url = self.interface_url + '/Tools/OauthSdkApp'
        data = {
            'Appid': Appid,
            'AvatarId': AvatarId,
            'Opt': Opt,
            'State': State,
            "Wxid": self.机器人id,
            'packageName': packageName,
            'sdkName': sdkName,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 第三方APP授权(self, Appid, Url, ):
        url = self.interface_url + '/Tools/ThirdAppGrant'
        data = {
            'Appid': Appid,
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 修改微信步数(self, Number, ):
        url = self.interface_url + '/Tools/UpdateStepNumberApi'
        data = {
            'Number': Number,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 设置删除代理IP(self, Proxy, ):
        url = self.interface_url + '/Tools/setproxy'
        data = {
            'Proxy': Proxy,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 绑定QQ(self, Account, Password, ):
        url = self.interface_url + '/User/BindQQ'
        data = {
            'Account': Account,
            'Password': Password,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 绑定邮箱(self, Email, ):
        url = self.interface_url + '/User/BindingEmail'
        data = {
            'Email': Email,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 换绑手机号(self, Mobile, Verifycode, ):
        url = self.interface_url + '/User/BindingMobile'
        data = {
            'Mobile': Mobile,
            'Verifycode': Verifycode,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 删除登录设备(self, Uuid, ):
        url = self.interface_url + '/User/DelSafetyInfo'
        data = {
            'Uuid': Uuid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 取个人信息(self, ):
        url = self.interface_url + '/User/GetContractProfile'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 取个人二维码(self, Style, ):
        url = self.interface_url + '/User/GetQRCode'
        data = {
            'Style': Style,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 登录设备管理(self, ):
        url = self.interface_url + '/User/GetSafetyInfo'
        params = {
            "Wxid": self.机器人id,
        }
        response = requests.post(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def 隐私设置(self, Function, Value, ):
        url = self.interface_url + '/User/PrivacySettings'
        data = {
            'Function': Function,
            'Value': Value,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def ReportMotion(self, DeviceId, DeviceType, StepCount, ):
        url = self.interface_url + '/User/ReportMotion'
        data = {
            'DeviceId': DeviceId,
            'DeviceType': DeviceType,
            'StepCount': StepCount,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 发送手机验证码(self, Mobile, Opcode, ):
        url = self.interface_url + '/User/SendVerifyMobile'
        data = {
            'Mobile': Mobile,
            'Opcode': Opcode,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 设置微信号(self, Alisa, ):
        url = self.interface_url + '/User/SetAlisa'
        data = {
            'Alisa': Alisa,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 修改密码(self, NewPassword, Ticket, ):
        url = self.interface_url + '/User/SetPasswd'
        data = {
            'NewPassword': NewPassword,
            'Ticket': Ticket,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 修改个人信息(self, City, Country, NickName, Province, Sex, Signature, ):
        url = self.interface_url + '/User/UpdateProfile'
        data = {
            'City': City,
            'Country': Country,
            'NickName': NickName,
            'Province': Province,
            'Sex': Sex,
            'Signature': Signature,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 修改头像(self, Base64, ):
        url = self.interface_url + '/User/UploadHeadImage'
        data = {
            'Base64': Base64,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 验证密码(self, Password, ):
        url = self.interface_url + '/User/VerifyPasswd'
        data = {
            'Password': Password,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def AddAvatar(self, AFilekey, Appid, NickName, ):
        url = self.interface_url + '/Wxapp/AddAvatar'
        data = {
            'AFilekey': AFilekey,
            'Appid': Appid,
            'NickName': NickName,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 小程序绑定增加手机号(self, Appid, Mobile, VerifyCode, ):
        url = self.interface_url + '/Wxapp/AddMobile'
        data = {
            'Appid': Appid,
            'Mobile': Mobile,
            'VerifyCode': VerifyCode,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 新增小程序记录(self, Username, ):
        url = self.interface_url + '/Wxapp/AddWxAppRecord'
        data = {
            'Username': Username,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 小程序云函数(self, Appid, Data, ):
        url = self.interface_url + '/Wxapp/CloudCallFunction'
        data = {
            'Appid': Appid,
            'Data': Data,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 小程序删除手机号(self, Appid, Mobile, Opcode, ):
        url = self.interface_url + '/Wxapp/DelMobile'
        data = {
            'Appid': Appid,
            'Mobile': Mobile,
            'Opcode': Opcode,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def GetAllMobile(self, Appid, Data, Opt, ):
        url = self.interface_url + '/Wxapp/GetAllMobile'
        data = {
            'Appid': Appid,
            'Data': Data,
            'Opt': Opt,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def GetRandomAvatar(self, Appid, ):
        url = self.interface_url + '/Wxapp/GetRandomAvatar'
        data = {
            'Appid': Appid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def GetUserOpenId(self, Appid, ToWxId, ):
        url = self.interface_url + '/Wxapp/GetUserOpenId'
        data = {
            'Appid': Appid,
            'ToWxId': ToWxId,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取小程序支付sessionid(self, Appid, ):
        url = self.interface_url + '/Wxapp/JSGetSessionid'
        data = {
            'Appid': Appid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 获取付小程序款二维码(self, Appid, Package, PaySign, Sessionid, Wxid, nonceStr, timeStamp):
        url = self.interface_url + '/Wxapp/JSGetSessionidQRcode'
        data = {
            'Appid': Appid,
            'Package': Package,
            'PaySign': PaySign,
            'Sessionid': Sessionid,
            "Wxid": self.机器人id,
            'nonceStr': nonceStr,
            'timeStamp': timeStamp,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 授权小程序(self, Appid, ):
        url = self.interface_url + '/Wxapp/JSLogin'
        data = {
            'Appid': Appid,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 小程序操作(self, Appid, Data, Opt, ):
        url = self.interface_url + '/Wxapp/JSOperateWxData'
        data = {
            'Appid': Appid,
            'Data': Data,
            'Opt': Opt,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def 扫码授权登录app或网页(self, Url, ):
        url = self.interface_url + '/Wxapp/QrcodeAuthLogin'
        data = {
            'Url': Url,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def UploadAvatarImg(self, Appid, JPGlink, ):
        url = self.interface_url + '/Wxapp/UploadAvatarImg'
        data = {
            'Appid': Appid,
            'JPGlink': JPGlink,
            "Wxid": self.机器人id,
        }
        response = requests.post(url, json=data, headers=headers).json()
        logger.debug(response)
        return response


if __name__ == "__main__":
    client = HttpClient()
    设备id = client.获取二维码('')['DeviceId']
    print(设备id)


