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

# ... existing code ...

class HttpClient:
    def __init__(self,wxid='',api_url='http://127.0.0.1:9999',key=''):
        self.机器人id = wxid
        self.interface_url = api_url
        self.key = key

    # --- Generated Methods based on swagger.json ---

    def admin_授权码延期(self, Days, ExpiryDate, Key):
        """管理-授权码延期"""
        url = self.interface_url + '/admin/DelayAuthKey'
        params = {}
        params['key'] = self.key
        data = {
            'Days': Days,
            'ExpiryDate': ExpiryDate,
            'Key': Key,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def admin_删除授权码(self, Key, Opt):
        """管理-删除授权码"""
        url = self.interface_url + '/admin/DeleteAuthKey'
        params = {}
        params['key'] = self.key
        data = {
            'Key': Key,
            'Opt': Opt,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def admin_禁用授权码(self, IsBanned, Key):
        """管理-禁用授权码"""
        url = self.interface_url + '/admin/DisableAuthKey'
        params = {}
        params['key'] = self.key
        data = {
            'IsBanned': IsBanned,
            'Key': Key,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def admin_生成授权码新设备(self, Count, Days):
        """管理-生成授权码(新设备)"""
        url = self.interface_url + '/admin/GenAuthKey1'
        params = {}
        params['key'] = self.key
        data = {
            'Count': Count,
            'Days': Days,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def admin_生成授权码新设备2(self):
        """管理-生成授权码(新设备)"""
        url = self.interface_url + '/admin/GenAuthKey2'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def admin_生成授权码类型(self, Count, Type):
        """管理-生成授权码(1-日 7-周 30-月 90-季 180-半年 365-年 30000-永久)此key不使用无过期时间"""
        url = self.interface_url + '/admin/GenAuthKey3'
        params = {}
        params['key'] = self.key
        data = {
            'Count': Count,
            'Type': Type,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def admin_查询所有激活状态的卡密(self):
        """管理-查询所有激活状态的卡密"""
        url = self.interface_url + '/admin/GetActiveLicenseKeys'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def admin_获取代理映射列表(self):
        """管理-获取代理映射列表"""
        url = self.interface_url + '/admin/GetProxyMappingList'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def admin_同步卡密激活状态HTTP轮询方式(self):
        """管理-同步卡密激活状态, HTTP-轮询方式"""
        url = self.interface_url + '/admin/HttpSyncLicenseKey'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def applet_授权公众号登录(self, Opcode, ReqUrl, Scene):
        """公众号/小程序-授权公众号登录"""
        url = self.interface_url + '/applet/AuthMpLogin'
        params = {}
        params['key'] = self.key
        data = {
            'Opcode': Opcode,
            'ReqUrl': ReqUrl,
            'Scene': Scene,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_关注公众号(self, GHList):
        """公众号/小程序-关注公众号"""
        url = self.interface_url + '/applet/FollowGH'
        params = {}
        params['key'] = self.key
        data = {
            'GHList': GHList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_授权链接(self, OpCode, ReqUrl, Scene):
        """公众号/小程序-授权链接"""
        url = self.interface_url + '/applet/GetA8Key'
        params = {}
        params['key'] = self.key
        data = {
            'OpCode': OpCode,
            'ReqUrl': ReqUrl,
            'Scene': Scene,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_阅读公众号文章(self, Url):
        """公众号/小程序-阅读公众号文章"""
        url = self.interface_url + '/applet/GetAppMsgExt'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_点赞公众号文章(self, Url):
        """公众号/小程序-点赞公众号文章"""
        url = self.interface_url + '/applet/GetAppMsgExtLike'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_获取公众号文章阅读数(self, Url):
        """公众号/小程序-获取公众号文章阅读数"""
        url = self.interface_url + '/applet/GetAppMsgReadCount'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_授权链接MpA8Key(self, Opcode, Scene, Url):
        """公众号/小程序-授权链接"""
        url = self.interface_url + '/applet/GetMpA8Key'
        params = {}
        params['key'] = self.key
        data = {
            'Opcode': Opcode,
            'Scene': Scene,
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_获取公众号历史消息(self, Url):
        """公众号/小程序-获取公众号历史消息"""
        url = self.interface_url + '/applet/GetMpHistoryMessage'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_小程序云函数操作(self, AppId, Data, Opt, PackageName, SdkName):
        """公众号/小程序-小程序云函数操作"""
        url = self.interface_url + '/applet/JSOperateWxData'
        params = {}
        params['key'] = self.key
        data = {
            'AppId': AppId,
            'Data': Data,
            'Opt': Opt,
            'PackageName': PackageName,
            'SdkName': SdkName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_授权小程序返回授权后的code(self, AppId, Data, Opt, PackageName, SdkName):
        """公众号/小程序-授权小程序(返回授权后的code)"""
        url = self.interface_url + '/applet/JsLogin'
        params = {}
        params['key'] = self.key
        data = {
            'AppId': AppId,
            'Data': Data,
            'Opt': Opt,
            'PackageName': PackageName,
            'SdkName': SdkName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_二维码授权请求(self, QrUrl):
        """公众号/小程序-二维码授权请求"""
        url = self.interface_url + '/applet/QRConnectAuthorize'
        params = {}
        params['key'] = self.key
        data = {
            'QrUrl': QrUrl,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_二维码授权确认(self, QrUrl):
        """公众号/小程序-二维码授权确认"""
        url = self.interface_url + '/applet/QRConnectAuthorizeConfirm'
        params = {}
        params['key'] = self.key
        data = {
            'QrUrl': QrUrl,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def applet_应用授权(self, AppId, Data, Opt, PackageName, SdkName):
        """公众号/小程序-应用授权"""
        url = self.interface_url + '/applet/SdkOauthAuthorize'
        params = {}
        params['key'] = self.key
        data = {
            'AppId': AppId,
            'Data': Data,
            'Opt': Opt,
            'PackageName': PackageName,
            'SdkName': SdkName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def equipment_删除安全设备(self, DeviceUUID):
        """设备-删除安全设备"""
        url = self.interface_url + '/equipment/DelSafeDevice'
        params = {}
        params['key'] = self.key
        data = {
            'DeviceUUID': DeviceUUID,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def equipment_获取硬件设备情况(self):
        """设备-获取硬件设备情况"""
        url = self.interface_url + '/equipment/GetBoundHardDevice'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def equipment_获取在线设备信息(self):
        """设备-获取在线设备信息"""
        url = self.interface_url + '/equipment/GetOnlineInfo'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def equipment_获取安全设备列表(self):
        """设备-获取安全设备列表"""
        url = self.interface_url + '/equipment/GetSafetyInfo'
        params = {}
        params['key'] = self.key
        # Swagger defines this as POST with no body params. Sending empty body.
        response = requests.post(url, params=params, json={}, headers=headers).json()
        logger.debug(response)
        return response

    def favor_删除收藏(self, FavId, KeyBuf):
        """收藏-删除收藏"""
        url = self.interface_url + '/favor/BatchDelFavItem'
        params = {}
        params['key'] = self.key
        data = {
            'FavId': FavId,
            'KeyBuf': KeyBuf,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def favor_同步收藏(self):
        """收藏-同步收藏"""
        url = self.interface_url + '/favor/FavSync'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def favor_获取收藏详细(self, FavId, KeyBuf):
        """收藏-获取收藏详细"""
        url = self.interface_url + '/favor/GetFavItemId'
        params = {}
        params['key'] = self.key
        data = {
            'FavId': FavId,
            'KeyBuf': KeyBuf,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def favor_获取收藏list(self, FavId, KeyBuf):
        """收藏-获取收藏list"""
        url = self.interface_url + '/favor/GetFavList'
        params = {}
        params['key'] = self.key
        data = {
            'FavId': FavId,
            'KeyBuf': KeyBuf,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def finder_关注取消(self, Cook, FinderUserName, OpType, PosterUsername, RefObjectId, Userver):
        """视频号-关注取消"""
        url = self.interface_url + '/finder/FinderFollow'
        params = {}
        params['key'] = self.key
        data = {
            'Cook': Cook,
            'FinderUserName': FinderUserName,
            'OpType': OpType,
            'PosterUsername': PosterUsername,
            'RefObjectId': RefObjectId,
            'Userver': Userver,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def finder_视频号搜索(self, Index, UserKey, Userver, Uuid):
        """视频号-视频号搜索"""
        url = self.interface_url + '/finder/FinderSearch'
        params = {}
        params['key'] = self.key
        data = {
            'Index': Index,
            'UserKey': UserKey,
            'Userver': Userver,
            'Uuid': Uuid,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def finder_视频号中心(self, Userver):
        """视频号-视频号中心"""
        url = self.interface_url + '/finder/FinderUserPrepare'
        params = {}
        params['key'] = self.key
        data = {
            'Userver': Userver,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_同意好友请求(self, ChatRoomUserName, OpCode, Scene, V3, V4, VerifyContent):
        """朋友-同意好友请求"""
        url = self.interface_url + '/friend/AgreeAdd'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomUserName': ChatRoomUserName,
            'OpCode': OpCode,
            'Scene': Scene,
            'V3': V3,
            'V4': V4,
            'VerifyContent': VerifyContent,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_删除好友(self, DelUserName):
        """朋友-删除好友"""
        url = self.interface_url + '/friend/DelContact'
        params = {}
        params['key'] = self.key
        data = {
            'DelUserName': DelUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_获取联系人详情(self, RoomWxIDList, UserNames):
        """朋友-获取联系人详情"""
        url = self.interface_url + '/friend/GetContactDetailsList'
        params = {}
        params['key'] = self.key
        data = {
            'RoomWxIDList': RoomWxIDList,
            'UserNames': UserNames,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_获取全部联系人(self, CurrentChatRoomContactSeq, CurrentWxcontactSeq):
        """朋友-获取全部联系人"""
        url = self.interface_url + '/friend/GetContactList'
        params = {}
        params['key'] = self.key
        data = {
            'CurrentChatRoomContactSeq': CurrentChatRoomContactSeq,
            'CurrentWxcontactSeq': CurrentWxcontactSeq,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_获取好友关系(self, UserName):
        """朋友-获取好友关系"""
        url = self.interface_url + '/friend/GetFriendRelation'
        params = {}
        params['key'] = self.key
        data = {
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_获取关注的公众号列表(self):
        """朋友-获取关注的公众号列表"""
        url = self.interface_url + '/friend/GetGHList'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def friend_获取手机通讯录好友(self):
        """朋友-获取手机通讯录好友"""
        url = self.interface_url + '/friend/GetMFriend'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def friend_获取保存的群聊列表(self, Key_param=None):
        """朋友-获取保存的群聊列表"""
        url = self.interface_url + '/friend/GroupList'
        params = {}
        params['key'] = self.key
        if Key_param is not None:
            params['Key'] = Key_param # Parameter named Key_param to avoid conflict with query param 'key'
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def friend_搜索联系人(self, FromScene, OpCode, SearchScene, UserName):
        """朋友-搜索联系人"""
        url = self.interface_url + '/friend/SearchContact'
        params = {}
        params['key'] = self.key
        data = {
            'FromScene': FromScene,
            'OpCode': OpCode,
            'SearchScene': SearchScene,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_上传手机通讯录好友(self, Mobile, MobileList, Opcode):
        """朋友-上传手机通讯录好友"""
        url = self.interface_url + '/friend/UploadMContact'
        params = {}
        params['key'] = self.key
        data = {
            'Mobile': Mobile,
            'MobileList': MobileList,
            'Opcode': Opcode,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def friend_验证好友添加好友(self, ChatRoomUserName, OpCode, Scene, V3, V4, VerifyContent):
        """朋友-验证好友/添加好友"""
        url = self.interface_url + '/friend/VerifyUser'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomUserName': ChatRoomUserName,
            'OpCode': OpCode,
            'Scene': Scene,
            'V3': V3,
            'V4': V4,
            'VerifyContent': VerifyContent,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_添加群成员(self, ChatRoomName, UserList):
        """群管理-添加群成员"""
        url = self.interface_url + '/group/AddChatRoomMembers'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'UserList': UserList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_添加群管理员(self, ChatRoomName, UserList):
        """群管理-添加群管理员"""
        url = self.interface_url + '/group/AddChatroomAdmin'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'UserList': UserList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_创建群请求(self, TopIc, UserList):
        """群管理-创建群请求"""
        url = self.interface_url + '/group/CreateChatRoom'
        params = {}
        params['key'] = self.key
        data = {
            'TopIc': TopIc,
            'UserList': UserList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_删除群管理员(self, ChatRoomName, UserList):
        """群管理-删除群管理员"""
        url = self.interface_url + '/group/DelChatroomAdmin'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'UserList': UserList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_获取群详情(self, ChatRoomWxIdList):
        """群管理-获取群详情"""
        url = self.interface_url + '/group/GetChatRoomInfo'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomWxIdList': ChatRoomWxIdList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_获取群成员详细(self, ChatRoomName):
        """群管理-获取群成员详细"""
        url = self.interface_url + '/group/GetChatroomMemberDetail'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        return response['Data']['member_data']['chatroom_member_list']
    def group_获取群成员名片(self,wxid, roomid):
        response = self.group_获取群成员详细(roomid)
        for member in response:
            if member["user_name"] == wxid:
                return {"data":{"alias":member["nick_name"]}}
        return response

    def group_获取群二维码(self, ChatRoomName):
        """群管理-获取群二维码"""
        url = self.interface_url + '/group/GetChatroomQrCode'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_邀请群成员(self, ChatRoomName, UserList):
        """群管理-邀请群成员"""
        url = self.interface_url + '/group/InviteChatroomMembers'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'UserList': UserList.split(","),
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_获取群聊(self, ChatRoomName, Val):
        """群管理-获取群聊"""
        url = self.interface_url + '/group/MoveToContract'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Val': Val,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_退出群聊(self, ChatRoomName):
        """群管理-退出群聊"""
        url = self.interface_url + '/group/QuitChatroom'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_扫码入群(self, Url):
        """群管理-扫码入群"""
        url = self.interface_url + '/group/ScanIntoUrlGroup'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_删除群成员2(self, ChatRoomName, UserList):
        """群管理-删除群成员"""
        url = self.interface_url + '/group/SendDelDelChatRoomMember'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'UserList': UserList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_群拍一拍功能(self, ChatRoomName, Scene, ToUserName):
        """群管理-群拍一拍功能"""
        url = self.interface_url + '/group/SendPat'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Scene': Scene,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_转让群(self, ChatRoomName, NewOwnerUserName):
        """群管理-转让群"""
        url = self.interface_url + '/group/SendTransferGroupOwner'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'NewOwnerUserName': NewOwnerUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_设置群聊邀请开关(self, ChatRoomName, Enable):
        """群管理-设置群聊邀请开关"""
        url = self.interface_url + '/group/SetChatroomAccessVerify'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Enable': Enable,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_设置群公告(self, ChatRoomName, Content):
        """群管理-设置群公告"""
        url = self.interface_url + '/group/SetChatroomAnnouncement'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Content': Content,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_设置群昵称(self, ChatRoomName, Nickname):
        """群管理-设置群昵称"""
        url = self.interface_url + '/group/SetChatroomName'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Nickname': Nickname,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_获取群公告(self, ChatRoomName):
        """群管理-获取群公告"""
        url = self.interface_url + '/group/SetGetChatRoomInfoDetail'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def group_同意入群(self, Url):
        """群管理-同意入群"""
        url = self.interface_url + '/group/ToJoinGroup'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def label_添加列表(self, LabelId, LabelNameList, UserLabelList):
        """标签-添加列表"""
        url = self.interface_url + '/label/AddContactLabel'
        params = {}
        params['key'] = self.key
        data = {
            'LabelId': LabelId,
            'LabelNameList': LabelNameList,
            'UserLabelList': UserLabelList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def label_删除标签(self, LabelId, LabelNameList, UserLabelList):
        """标签-删除标签"""
        url = self.interface_url + '/label/DelContactLabel'
        params = {}
        params['key'] = self.key
        data = {
            'LabelId': LabelId,
            'LabelNameList': LabelNameList,
            'UserLabelList': UserLabelList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def label_获取标签列表(self):
        """标签-获取标签列表"""
        url = self.interface_url + '/label/GetContactLabelList'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def label_获取标签下所有好友(self, LabelId, LabelNameList, UserLabelList):
        """标签-获取标签下所有好友"""
        url = self.interface_url + '/label/GetWXFriendListByLabel'
        params = {}
        params['key'] = self.key
        data = {
            'LabelId': LabelId,
            'LabelNameList': LabelNameList,
            'UserLabelList': UserLabelList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def label_修改标签(self, LabelId, LabelNameList, UserLabelList):
        """标签-修改标签"""
        url = self.interface_url + '/label/ModifyLabel'
        params = {}
        params['key'] = self.key
        data = {
            'LabelId': LabelId,
            'LabelNameList': LabelNameList,
            'UserLabelList': UserLabelList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_数据登录(self, DeviceInfo, LoginData, Password, Proxy, Ticket, Type, UserName):
        """登录-数据登录"""
        url = self.interface_url + '/login/A16Login'
        params = {}
        params['key'] = self.key
        data = {
            'DeviceInfo': DeviceInfo,
            'LoginData': LoginData,
            'Password': Password,
            'Proxy': Proxy,
            'Ticket': Ticket,
            'Type': Type,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_获取安卓平板登录二维码异地IP必须用代理(self, Check, Proxy):
        """登录-获取安卓平板登录二维码 (异地IP必须用代理 socks5://username:password@ipv4:port)"""
        url = self.interface_url + '/login/AndroidPadLogin'
        params = {}
        params['key'] = self.key
        data = {
            'Check': Check,
            'Proxy': Proxy,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_检测微信登录环境(self):
        """登录-检测微信登录环境"""
        url = self.interface_url + '/login/CheckCanSetAlias'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_检测扫码状态(self):
        """登录-检测扫码状态"""
        url = self.interface_url + '/login/CheckLoginStatus'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_62账号密码登录(self, DeviceInfo, LoginData, Password, Proxy, Ticket, Type, UserName):
        """登录-62账号密码登录"""
        url = self.interface_url + '/login/DeviceLogin'
        params = {}
        params['key'] = self.key
        data = {
            'DeviceInfo': DeviceInfo,
            'LoginData': LoginData,
            'Password': Password,
            'Proxy': Proxy,
            'Ticket': Ticket,
            'Type': Type,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_提取62数据(self):
        """登录-提取62数据"""
        url = self.interface_url + '/login/Get62Data'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_打印链接数量(self):
        """登录-打印链接数量"""
        url = self.interface_url + '/login/GetIWXConnect'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_初始化状态(self):
        """登录-初始化状态"""
        url = self.interface_url + '/login/GetInItStatus'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_获取登录二维码异地IP用代理(self, Check=False, Proxy=''):
        """登录-获取登录二维码(异地IP用代理 socks5://username:password@ipv4:port)"""
        url = self.interface_url + '/login/GetLoginQrCodeNew'
        params = {}
        params['key'] = self.key
        data = {
            'Check': Check,
            'Proxy': Proxy,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_获取在线状态(self):
        """登录-获取在线状态"""
        url = self.interface_url + '/login/GetLoginStatus'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_退出登录(self):
        """登录-退出登录"""
        url = self.interface_url + '/login/LogOut'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_62LoginNew新疆号登录(self, DeviceInfo, LoginData, Password, Proxy, Ticket, Type, UserName):
        """登录-62LoginNew新疆号登录"""
        url = self.interface_url + '/login/LoginNew'
        params = {}
        params['key'] = self.key
        data = {
            'DeviceInfo': DeviceInfo,
            'LoginData': LoginData,
            'Password': Password,
            'Proxy': Proxy,
            'Ticket': Ticket,
            'Type': Type,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_获取Mac登录二维码异地IP必须用代理(self, Check, Proxy):
        """登录-获取Mac登录二维码 (异地IP必须用代理 socks5://username:password@ipv4:port)"""
        url = self.interface_url + '/login/MacLogin'
        params = {}
        params['key'] = self.key
        data = {
            'Check': Check,
            'Proxy': Proxy,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_辅助新手机登录(self, Url):
        """登录-辅助新手机登录"""
        url = self.interface_url + '/login/PhoneDeviceLogin'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_HTML展示登录二维码(self):
        """登录-HTML展示登录二维码"""
        url = self.interface_url + '/login/ShowQrCode'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def login_短信登录(self, DeviceInfo, LoginData, Password, Proxy, Ticket, Type, UserName):
        """登录-短信登录"""
        url = self.interface_url + '/login/SmsLogin'
        params = {}
        params['key'] = self.key
        data = {
            'DeviceInfo': DeviceInfo,
            'LoginData': LoginData,
            'Password': Password,
            'Proxy': Proxy,
            'Ticket': Ticket,
            'Type': Type,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_唤醒登录只限扫码登录(self, Check, Proxy):
        """登录-唤醒登录(只限扫码登录)"""
        url = self.interface_url + '/login/WakeUpLogin'
        params = {}
        params['key'] = self.key
        data = {
            'Check': Check,
            'Proxy': Proxy,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def login_获取验证码(self, OpCode, PhoneNumber, Proxy, Reg, VerifyCode):
        """登录-获取验证码"""
        url = self.interface_url + '/login/WxBindOpMobileForReg'
        params = {}
        params['key'] = self.key
        data = {
            'OpCode': OpCode,
            'PhoneNumber': PhoneNumber,
            'Proxy': Proxy,
            'Reg': Reg,
            'VerifyCode': VerifyCode,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_添加要发送的文本消息进入管理器(self, MsgItem):
        """消息-添加要发送的文本消息进入管理器"""
        url = self.interface_url + '/message/AddMessageMgr'
        params = {}
        params['key'] = self.key
        data = {
            'MsgItem': MsgItem,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_上传视频(self, ThumbData, ToUserName, VideoData):
        """消息-上传视频"""
        url = self.interface_url + '/message/CdnUploadVideo'
        params = {}
        params['key'] = self.key
        data = {
            'ThumbData': ThumbData,
            'ToUserName': ToUserName,
            'VideoData': VideoData,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_删除消息回调配置(self):
        """消息回调-删除消息回调配置"""
        url = self.interface_url + '/message/DeleteCallback'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def message_转发表情包含动图(self, EmojiList):
        """消息-转发表情，包含动图"""
        url = self.interface_url + '/message/ForwardEmoji'
        params = {}
        params['key'] = self.key
        data = {
            'EmojiList': EmojiList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_转发图片(self, ForwardImageList, ForwardVideoList):
        """消息-转发图片"""
        url = self.interface_url + '/message/ForwardImageMessage'
        params = {}
        params['key'] = self.key
        data = {
            'ForwardImageList': ForwardImageList,
            'ForwardVideoList': ForwardVideoList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_转发视频(self, ForwardImageList, ForwardVideoList):
        """消息-转发视频"""
        url = self.interface_url + '/message/ForwardVideoMessage'
        params = {}
        params['key'] = self.key
        data = {
            'ForwardImageList': ForwardImageList,
            'ForwardVideoList': ForwardVideoList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_获取消息回调配置(self):
        """消息回调-获取消息回调配置"""
        url = self.interface_url + '/message/GetCallback'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def message_获取图片高清图片下载(self, CompressType, FromUserName, MsgId, Section, ToUserName, TotalLen):
        """消息-获取图片(高清图片下载)"""
        url = self.interface_url + '/message/GetMsgBigImg'
        params = {}
        params['key'] = self.key
        data = {
            'CompressType': CompressType,
            'FromUserName': FromUserName,
            'MsgId': MsgId,
            'Section': Section,
            'ToUserName': ToUserName,
            'TotalLen': TotalLen,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_获取视频视频数据下载(self, CompressType, FromUserName, MsgId, Section, ToUserName, TotalLen):
        """消息-获取视频(视频数据下载)"""
        url = self.interface_url + '/message/GetMsgVideo'
        params = {}
        params['key'] = self.key
        data = {
            'CompressType': CompressType,
            'FromUserName': FromUserName,
            'MsgId': MsgId,
            'Section': Section,
            'ToUserName': ToUserName,
            'TotalLen': TotalLen,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_下载语音消息(self, Bufid, Length, NewMsgId, ToUserName):
        """消息-下载语音消息"""
        url = self.interface_url + '/message/GetMsgVoice'
        params = {}
        params['key'] = self.key
        data = {
            'Bufid': Bufid,
            'Length': Length,
            'NewMsgId': NewMsgId,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_群发图片(self, ImageBase64, ToUserName):
        """消息-群发图片"""
        url = self.interface_url + '/message/GroupMassMsgImage'
        params = {}
        params['key'] = self.key
        data = {
            'ImageBase64': ImageBase64,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_群发接口(self, Content, ToUserName):
        """消息-群发接口"""
        url = self.interface_url + '/message/GroupMassMsgText'
        params = {}
        params['key'] = self.key
        data = {
            'Content': Content,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_同步消息HTTP轮询方式(self, Count):
        """消息-同步消息, HTTP-轮询方式"""
        url = self.interface_url + '/message/HttpSyncMsg'
        params = {}
        params['key'] = self.key
        data = {
            'Count': Count,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_同步历史消息(self):
        """消息-同步历史消息"""
        url = self.interface_url + '/message/NewSyncHistoryMessage'
        params = {}
        params['key'] = self.key
        # Swagger defines this as POST with no body params. Sending empty body.
        response = requests.post(url, params=params, json={}, headers=headers).json()
        logger.debug(response)
        return response

    def message_撤销消息(self, ClientImgIdStr, ClientMsgId, CreateTime, IsImage, NewMsgId, ToUserName):
        """消息-撤销消息"""
        url = self.interface_url + '/message/RevokeMsg'
        params = {}
        params['key'] = self.key
        data = {
            'ClientImgIdStr': ClientImgIdStr,
            'ClientMsgId': ClientMsgId,
            'CreateTime': CreateTime,
            'IsImage': IsImage,
            'NewMsgId': NewMsgId,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_撤回消息New(self, ClientImgIdStr, ClientMsgId, CreateTime, IsImage, NewMsgId, ToUserName):
        """消息-撤回消息（New）"""
        url = self.interface_url + '/message/RevokeMsgNew'
        params = {}
        params['key'] = self.key
        data = {
            'ClientImgIdStr': ClientImgIdStr,
            'ClientMsgId': ClientMsgId,
            'CreateTime': CreateTime,
            'IsImage': IsImage,
            'NewMsgId': NewMsgId,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_发送App消息(self, AppList):
        """消息-发送App消息"""
        url = self.interface_url + '/message/SendAppMessage'
        params = {}
        params['key'] = self.key
        data = {
            'AppList': AppList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_下载请求(self, AesKey, FileType, FileURL):
        """消息-下载 请求"""
        url = self.interface_url + '/message/SendCdnDownload'
        params = {}
        params['key'] = self.key
        data = {
            'AesKey': AesKey,
            'FileType': FileType,
            'FileURL': FileURL,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_发送表情(self, EmojiList):
        """消息-发送表情"""
        url = self.interface_url + '/message/SendEmojiMessage'
        params = {}
        params['key'] = self.key
        data = {
            'EmojiList': EmojiList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_发送图片消息(self, MsgItem):
        """消息-发送图片消息"""
        url = self.interface_url + '/message/SendImageMessage'
        params = {}
        params['key'] = self.key
        data = {
            'MsgItem': MsgItem,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_发送图片消息New(self, MsgItem):
        """消息-发送图片消息（New）"""
        url = self.interface_url + '/message/SendImageNewMessage'
        params = {}
        params['key'] = self.key
        data = {
            'MsgItem': MsgItem,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_发送文本消息(self, text,receiver,aters=''):
        """消息-发送文本消息"""
        
        ats = ""
        wxids = []
        if aters:
            if aters == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = aters.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f"@{self.group_获取群成员名片(wxid, receiver)['data']['alias']}"
        if ats != "":
            text = f"{ats}\n{text}"
        MsgItem = [
        {
            "AtWxIDList": wxids,
            "ImageContent": "",
            "MsgType": 1,
            "TextContent": text,
            "ToUserName": receiver
        },
        ]
        url = self.interface_url + '/message/SendTextMessage'
        params = {}
        params['key'] = self.key
        data = {
            'MsgItem': MsgItem,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_发送语音(self, ToUserName, VoiceData, VoiceFormat, VoiceSecond):
        """消息-发送语音"""
        url = self.interface_url + '/message/SendVoice'
        params = {}
        params['key'] = self.key
        data = {
            'ToUserName': ToUserName,
            'VoiceData': VoiceData,
            'VoiceFormat': VoiceFormat,
            'VoiceSecond,': VoiceSecond,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_设置消息回调(self, CallbackURL, Enabled):
        """消息回调-设置消息回调"""
        url = self.interface_url + '/message/SetCallback'
        params = {}
        params['key'] = self.key
        data = {
            'CallbackURL': CallbackURL,
            'Enabled': Enabled,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def message_分享名片消息(self, CardAlias, CardFlag, CardNickName, CardWxId, ToUserName):
        """消息-分享名片消息"""
        url = self.interface_url + '/message/ShareCardMessage'
        params = {}
        params['key'] = self.key
        data = {
            'CardAlias': CardAlias,
            'CardFlag': CardFlag,
            'CardNickName': CardNickName,
            'CardWxId': CardWxId,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def other_查看附近的人(self, Latitude, Longitude):
        """其他-查看附近的人"""
        url = self.interface_url + '/other/GetPeopleNearby'
        params = {}
        params['key'] = self.key
        data = {
            'Latitude': Latitude,
            'Longitude': Longitude,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def other_获取项目完整路径(self):
        """其他-获取项目完整路径"""
        url = self.interface_url + '/other/GetProjectFullPath'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def other_获取缓存在redis中的消息(self, Key):
        """其他-获取缓存在redis中的消息"""
        url = self.interface_url + '/other/GetRedisSyncMsg'
        params = {}
        params['key'] = self.key
        data = {
            'Key': Key,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def other_获取步数排行数据列表(self, RankId):
        """其他-获取步数排行数据列表"""
        url = self.interface_url + '/other/GetUserRankLikeCount'
        params = {}
        params['key'] = self.key
        data = {
            'RankId': RankId,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def other_更新指令状态(self, Key, Value, ValueStr):
        """其他-更新指令状态, key 为指令 id，Value 为指令状态 0|1，ValueStr 为字符串值"""
        url = self.interface_url + '/other/UpdateCmdStatus'
        params = {}
        params['key'] = self.key
        data = {
            'Key': Key,
            'Value': Value,
            'ValueStr': ValueStr,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def other_修改步数(self, Number):
        """其他-修改步数"""
        url = self.interface_url + '/other/UpdateStepNumber'
        params = {}
        params['key'] = self.key
        data = {
            'Number': Number,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def other_上传文件(self, fileData):
        """其他-上传文件"""
        url = self.interface_url + '/other/UploadAppAttach'
        params = {}
        params['key'] = self.key
        data = {
            'fileData': fileData,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_确定收款(self, InvalidTime, ToUserName, TransFerId, TransactionId):
        """支付-确定收款"""
        url = self.interface_url + '/pay/Collectmoney'
        params = {}
        params['key'] = self.key
        data = {
            'InvalidTime': InvalidTime,
            'ToUserName': ToUserName,
            'TransFerId': TransFerId,
            'TransactionId': TransactionId,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_确认转账客户端版本过低会无法转账(self, BankSerial, BankType, PayPassword, ReqKey):
        """支付-确认转账(客户端版本过低会无法转账)"""
        url = self.interface_url + '/pay/ConfirmPreTransfer'
        params = {}
        params['key'] = self.key
        data = {
            'BankSerial': BankSerial,
            'BankType': BankType,
            'PayPassword': PayPassword,
            'ReqKey': ReqKey,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_创建转账(self, Description, Fee, ToUserName):
        """支付-创建转账"""
        url = self.interface_url + '/pay/CreatePreTransfer'
        params = {}
        params['key'] = self.key
        data = {
            'Description': Description,
            'Fee': Fee,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_生成自定义收款二维码(self, Money, Name):
        """支付-生成自定义收款二维码"""
        url = self.interface_url + '/pay/GeneratePayQCode'
        params = {}
        params['key'] = self.key
        data = {
            'Money': Money,
            'Name': Name,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_获取银行卡信息(self):
        """支付-获取银行卡信息"""
        url = self.interface_url + '/pay/GetBandCardList'
        params = {}
        params['key'] = self.key
        # Swagger defines this as POST with no body params. Sending empty body.
        response = requests.post(url, params=params, json={}, headers=headers).json()
        logger.debug(response)
        return response

    def pay_查看红包详情(self, HongBaoItem, Limit, NativeURL, Offset):
        """支付-查看红包详情"""
        url = self.interface_url + '/pay/GetRedEnvelopesDetail'
        params = {}
        params['key'] = self.key
        data = {
            'HongBaoItem': HongBaoItem,
            'Limit': Limit,
            'NativeURL': NativeURL,
            'Offset': Offset,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_查看红包领取列表(self, HongBaoItem, Limit, NativeURL, Offset):
        """支付-查看红包领取列表"""
        url = self.interface_url + '/pay/GetRedPacketList'
        params = {}
        params['key'] = self.key
        data = {
            'HongBaoItem': HongBaoItem,
            'Limit': Limit,
            'NativeURL': NativeURL,
            'Offset': Offset,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_拆红包(self, HongBaoItem, Limit, NativeURL, Offset):
        """支付-拆红包"""
        url = self.interface_url + '/pay/OpenRedEnvelopes'
        params = {}
        params['key'] = self.key
        data = {
            'HongBaoItem': HongBaoItem,
            'Limit': Limit,
            'NativeURL': NativeURL,
            'Offset': Offset,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def pay_创建红包(self, Amount, Content, Count, From, RedType, Username):
        """支付-创建红包"""
        url = self.interface_url + '/pay/WXCreateRedPacket'
        params = {}
        params['key'] = self.key
        data = {
            'Amount': Amount,
            'Content': Content,
            'Count': Count,
            'From': From,
            'RedType': RedType,
            'Username': Username,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_同意进企业群(self, Link, Opcode):
        """企业微信-同意进企业群"""
        url = self.interface_url + '/qy/QWAcceptChatRoom'
        params = {}
        params['key'] = self.key
        data = {
            'Link': Link,
            'Opcode': Opcode,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_直接拉朋友进企业群(self, ChatRoomName, ToUserName):
        """企业微信-直接拉朋友进企业群"""
        url = self.interface_url + '/qy/QWAddChatRoomMember'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_设定企业群管理审核进群(self, ChatRoomName, P):
        """企业微信-设定企业群管理审核进群"""
        url = self.interface_url + '/qy/QWAdminAcceptJoinChatRoomSet'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'P': P,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_向企业微信打招呼(self, Content, UserName, V1):
        """企业微信-向企业微信打招呼"""
        url = self.interface_url + '/qy/QWApplyAddContact'
        params = {}
        params['key'] = self.key
        data = {
            'Content': Content,
            'UserName': UserName,
            'V1': V1,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_增加企业管理员(self, ChatRoomName, ToUserName):
        """企业微信-增加企业管理员"""
        url = self.interface_url + '/qy/QWAppointChatRoomAdmin'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_发布企业群公告(self, ChatRoomName, Name):
        """企业微信-发布企业群公告"""
        url = self.interface_url + '/qy/QWChatRoomAnnounce'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Name': Name,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_转让企业群(self, ChatRoomName, ToUserName):
        """企业微信-转让企业群"""
        url = self.interface_url + '/qy/QWChatRoomTransferOwner'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_提取企业wx详情(self, ChatRoom, T, ToUserName):
        """企业微信-提取企业 wx 详情"""
        url = self.interface_url + '/qy/QWContact'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoom': ChatRoom,
            'T': T,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_创建企业群(self, ToUserName):
        """企业微信-创建企业群"""
        url = self.interface_url + '/qy/QWCreateChatRoom'
        params = {}
        params['key'] = self.key
        data = {
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_删除企业群(self, ChatRoomName, Name):
        """企业微信-删除企业群"""
        url = self.interface_url + '/qy/QWDelChatRoom'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Name': Name,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_移除群管理员(self, ChatRoomName, ToUserName):
        """企业微信-移除群管理员"""
        url = self.interface_url + '/qy/QWDelChatRoomAdmin'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_删除企业群成员(self, ChatRoomName, ToUserName):
        """企业微信-删除企业群成员"""
        url = self.interface_url + '/qy/QWDelChatRoomMember'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_提取企业群全部成员(self, ChatRoomName, ToUserName):
        """企业微信-提取企业群全部成员"""
        url = self.interface_url + '/qy/QWGetChatRoomMember'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_提取企业群二维码(self, ChatRoomName, ToUserName):
        """企业微信-提取企业群二维码"""
        url = self.interface_url + '/qy/QWGetChatRoomQR'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_提取企业群名称公告设定等信息(self, ChatRoomName, ToUserName):
        """企业微信-提取企业群名称公告设定等信息"""
        url = self.interface_url + '/qy/QWGetChatroomInfo'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_发送群邀请链接(self, ChatRoomName, ToUserName):
        """企业微信-发送群邀请链接"""
        url = self.interface_url + '/qy/QWInviteChatRoomMember'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_修改成员在群中呢称(self, ChatRoomName, Name):
        """企业微信-修改成员在群中呢称"""
        url = self.interface_url + '/qy/QWModChatRoomMemberNick'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Name': Name,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_修改企业群名称(self, ChatRoomName, Name):
        """企业微信-修改企业群名称"""
        url = self.interface_url + '/qy/QWModChatRoomName'
        params = {}
        params['key'] = self.key
        data = {
            'ChatRoomName': ChatRoomName,
            'Name': Name,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_备注企业wxid(self, Name, ToUserName):
        """企业微信-备注企业 wxid"""
        url = self.interface_url + '/qy/QWRemark'
        params = {}
        params['key'] = self.key
        data = {
            'Name': Name,
            'ToUserName': ToUserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_搜手机或企业对外名片链接提取验证(self, FromScene, Tg, UserName):
        """企业微信-搜手机或企业对外名片链接提取验证"""
        url = self.interface_url + '/qy/QWSearchContact'
        params = {}
        params['key'] = self.key
        data = {
            'FromScene': FromScene,
            'Tg': Tg,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_提取全部企业微信群(self, Key):
        """企业微信-提取全部企业微信群-"""
        url = self.interface_url + '/qy/QWSyncChatRoom'
        params = {}
        params['key'] = self.key
        data = {
            'Key': Key,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def qy_提取全部的企业通讯录(self):
        """企业微信-提取全部的企业通讯录"""
        url = self.interface_url + '/qy/QWSyncContact'
        params = {}
        params['key'] = self.key
        # Swagger defines this as POST with no body params. Sending empty body.
        response = requests.post(url, params=params, json={}, headers=headers).json()
        logger.debug(response)
        return response

    def sns_上传CDN朋友圈视频(self, ThumbData, VideoData):
        """朋友圈-上传CDN朋友圈视频"""
        url = self.interface_url + '/sns/CdnSnsVideoUpload'
        params = {}
        params['key'] = self.key
        data = {
            'ThumbData': ThumbData,
            'VideoData': VideoData,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_下载朋友圈视频(self, Key, URL):
        """朋友圈-下载朋友圈视频"""
        url = self.interface_url + '/sns/DownloadMedia'
        params = {}
        params['key'] = self.key
        data = {
            'Key': Key,
            'URL': URL,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_获取收藏朋友圈详情(self, BlackList, FavItemID, Location, LocationVal, SourceID):
        """朋友圈-获取收藏朋友圈详情"""
        url = self.interface_url + '/sns/GetCollectCircle'
        params = {}
        params['key'] = self.key
        data = {
            'BlackList': BlackList,
            'FavItemID': FavItemID,
            'Location': Location,
            'LocationVal': LocationVal,
            'SourceID': SourceID,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_同步朋友圈(self):
        """朋友圈-同步朋友圈"""
        url = self.interface_url + '/sns/GetSnsSync'
        params = {}
        params['key'] = self.key
        # Swagger defines this as POST with no body params. Sending empty body.
        response = requests.post(url, params=params, json={}, headers=headers).json()
        logger.debug(response)
        return response

    def sns_转发收藏朋友圈(self, BlackList, FavItemID, Location, LocationVal, SourceID):
        """朋友圈-转发收藏朋友圈"""
        url = self.interface_url + '/sns/SendFavItemCircle'
        params = {}
        params['key'] = self.key
        data = {
            'BlackList': BlackList,
            'FavItemID': FavItemID,
            'Location': Location,
            'LocationVal': LocationVal,
            'SourceID': SourceID,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_发送朋友圈(self, BlackList, Content, ContentStyle, ContentUrl, Description, GroupUserList, LocationInfo, MediaList, Privacy, WithUserList):
        """朋友圈-发送朋友圈"""
        url = self.interface_url + '/sns/SendFriendCircle'
        params = {}
        params['key'] = self.key
        data = {
            'BlackList': BlackList,
            'Content': Content,
            'ContentStyle': ContentStyle,
            'ContentUrl': ContentUrl,
            'Description': Description,
            'GroupUserList': GroupUserList,
            'LocationInfo': LocationInfo,
            'MediaList': MediaList,
            'Privacy': Privacy,
            'WithUserList': WithUserList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_发送朋友圈XML结构(self, ActionInfo, AppInfo, ContentDesc, ContentDescScene, ContentDescShowType, ContentObject, ContentObjectVideo, CreateTime, ID, Location, Private, PublicUserName, ShowFlag, SightFolded, SourceNickName, SourceUserName, StatExtStr, StatisticsData, StreamVideo, UserName):
        """朋友圈-发送朋友圈XML结构"""
        url = self.interface_url + '/sns/SendFriendCircleByXMl'
        params = {}
        params['key'] = self.key
        data = {
            'ActionInfo': ActionInfo,
            'AppInfo': AppInfo,
            'ContentDesc': ContentDesc,
            'ContentDescScene': ContentDescScene,
            'ContentDescShowType': ContentDescShowType,
            'ContentObject': ContentObject,
            'ContentObjectVideo': ContentObjectVideo,
            'CreateTime': CreateTime,
            'ID': ID,
            'Location': Location,
            'Private': Private,
            'PublicUserName': PublicUserName,
            'ShowFlag': ShowFlag,
            'SightFolded': SightFolded,
            'SourceNickName': SourceNickName,
            'SourceUserName': SourceUserName,
            'StatExtStr': StatExtStr,
            'StatisticsData': StatisticsData,
            'StreamVideo': StreamVideo,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_一键转发朋友圈(self, BlackList, Id, Location, LocationVal):
        """朋友圈-一键转发朋友圈"""
        url = self.interface_url + '/sns/SendOneIdCircle'
        params = {}
        params['key'] = self.key
        data = {
            'BlackList': BlackList,
            'Id': Id,
            'Location': Location,
            'LocationVal': LocationVal,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_点赞评论(self, SnsCommentList, Tx):
        """朋友圈-点赞评论"""
        url = self.interface_url + '/sns/SendSnsComment'
        params = {}
        params['key'] = self.key
        data = {
            'SnsCommentList': SnsCommentList,
            'Tx': Tx,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_朋友圈操作(self, SnsObjectOpList):
        """朋友圈-朋友圈操作"""
        url = self.interface_url + '/sns/SendSnsObjectOp'
        params = {}
        params['key'] = self.key
        data = {
            'SnsObjectOpList': SnsObjectOpList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_获取指定id朋友圈(self, BlackList, Id, Location, LocationVal):
        """朋友圈-获取指定id朋友圈"""
        url = self.interface_url + '/sns/SendSnsObjectDetailById'
        params = {}
        params['key'] = self.key
        data = {
            'BlackList': BlackList,
            'Id': Id,
            'Location': Location,
            'LocationVal': LocationVal,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_获取朋友圈主页(self, FirstPageMD5, MaxID, UserName):
        """朋友圈-获取朋友圈主页"""
        url = self.interface_url + '/sns/SendSnsTimeLine'
        params = {}
        params['key'] = self.key
        data = {
            'FirstPageMD5': FirstPageMD5,
            'MaxID': MaxID,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_获取指定人朋友圈(self, FirstPageMD5, MaxID, UserName):
        """朋友圈-获取指定人朋友圈"""
        url = self.interface_url + '/sns/SendSnsUserPage'
        params = {}
        params['key'] = self.key
        data = {
            'FirstPageMD5': FirstPageMD5,
            'MaxID': MaxID,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_设置朋友圈背景图片(self, Url):
        """朋友圈-设置朋友圈背景图片"""
        url = self.interface_url + '/sns/SetBackgroundImage'
        params = {}
        params['key'] = self.key
        data = {
            'Url': Url,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_设置朋友圈可见天数(self, Function, Value):
        """朋友圈-设置朋友圈可见天数"""
        url = self.interface_url + '/sns/SetFriendCircleDays'
        params = {}
        params['key'] = self.key
        data = {
            'Function': Function,
            'Value': Value,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def sns_上传图片信息(self, ImageDataList, VideoDataList):
        """朋友圈-上传图片信息"""
        url = self.interface_url + '/sns/UploadFriendCircleImage'
        params = {}
        params['key'] = self.key
        data = {
            'ImageDataList': ImageDataList,
            'VideoDataList': VideoDataList,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_更改密码(self, newPass, oldPass, opCode):
        """用户-更改密码"""
        url = self.interface_url + '/user/ChangePwd'
        params = {}
        params['key'] = self.key
        data = {
            'newPass': newPass,
            'oldPass': oldPass,
            'opCode': opCode,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取管理员关键词配置(self):
        """用户-获取管理员关键词配置"""
        url = self.interface_url + '/user/GetAdminKeyword'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取关键词邀请入群配置(self):
        """用户-获取关键词邀请入群配置"""
        url = self.interface_url + '/user/GetInviteKeyword'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取关键词自动回复配置(self):
        """用户-获取关键词自动回复配置"""
        url = self.interface_url + '/user/GetKeywordReply'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取踢人关键词配置(self):
        """用户-获取踢人关键词配置"""
        url = self.interface_url + '/user/GetKickKeyword'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取我的二维码(self, Recover, Style):
        """用户-获取我的二维码"""
        url = self.interface_url + '/user/GetMyQrCode'
        params = {}
        params['key'] = self.key
        data = {
            'Recover': Recover,
            'Style': Style,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取个人资料信息(self):
        """用户-获取个人资料信息"""
        url = self.interface_url + '/user/GetProfile'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def user_获取欢迎词配置(self):
        """用户-获取欢迎词配置"""
        url = self.interface_url + '/user/GetWelcome'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改备注(self, RemarkName, UserName):
        """用户-修改备注"""
        url = self.interface_url + '/user/ModifyRemark'
        params = {}
        params['key'] = self.key
        data = {
            'RemarkName': RemarkName,
            'UserName': UserName,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改资料(self, City, Country, InitFlag, NickName, Province, Sex, Signature):
        """用户-修改资料"""
        url = self.interface_url + '/user/ModifyUserInfo'
        params = {}
        params['key'] = self.key
        data = {
            'City': City,
            'Country': Country,
            'InitFlag': InitFlag,
            'NickName': NickName,
            'Province': Province,
            'Sex': Sex,
            'Signature': Signature,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_重置性别(self):
        """用户-重置性别"""
        url = self.interface_url + '/user/ResetGender'
        params = {}
        params['key'] = self.key
        # Swagger defines this as POST with no body params. Sending empty body.
        response = requests.post(url, params=params, json={}, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置管理员关键词配置(self, Key, Params1, Params2, Params3, Params4, Value, ValueStr):
        """用户-设置管理员关键词配置"""
        url = self.interface_url + '/user/SetAdminKeyword'
        params = {}
        params['key'] = self.key
        data = {
            'Key': Key,
            'Params1': Params1,
            'Params2': Params2,
            'Params3': Params3,
            'Params4': Params4,
            'Value': Value,
            'ValueStr': ValueStr,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置添加我的方式(self, Function, Value):
        """用户-设置添加我的方式"""
        url = self.interface_url + '/user/SetFunctionSwitch'
        params = {}
        params['key'] = self.key
        data = {
            'Function': Function,
            'Value': Value,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置关键词邀请入群配置(self, Enable, Groups, InviteMessage, Mode, TimeInSeconds):
        """用户-设置关键词邀请入群配置"""
        url = self.interface_url + '/user/SetInviteKeyword'
        params = {}
        params['key'] = self.key
        data = {
            'Enable': Enable,
            'Groups': Groups,
            'InviteMessage': InviteMessage,
            'Mode': Mode,
            'TimeInSeconds': TimeInSeconds,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置关键词自动回复(self, CommentMessages, Enable, EndTime, Groups, Mode, StartTime, TimeInSeconds):
        """用户-设置关键词自动回复"""
        url = self.interface_url + '/user/SetKeywordReply'
        params = {}
        params['key'] = self.key
        data = {
            'CommentMessages': CommentMessages,
            'Enable': Enable,
            'EndTime': EndTime,
            'Groups': Groups,
            'Mode': Mode,
            'StartTime': StartTime,
            'TimeInSeconds': TimeInSeconds,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置踢人关键词配置(self, Enable, IsCardKick, IsImageQRCodeKick, IsLinkKick, IsMiniProgramKick, Keywords, Mode, Rooms):
        """用户-设置踢人关键词配置"""
        url = self.interface_url + '/user/SetKickKeyword'
        params = {}
        params['key'] = self.key
        data = {
            'Enable': Enable,
            'IsCardKick': IsCardKick,
            'IsImageQRCodeKick': IsImageQRCodeKick,
            'IsLinkKick': IsLinkKick,
            'IsMiniProgramKick': IsMiniProgramKick,
            'Keywords': Keywords,
            'Mode': Mode,
            'Rooms': Rooms,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置昵称(self, Scene, Val):
        """用户-设置昵称"""
        url = self.interface_url + '/user/SetNickName'
        params = {}
        params['key'] = self.key
        data = {
            'Scene': Scene,
            'Val': Val,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改Socks5代理socks5usernamepasswordipv4(self, Check, Proxy):
        """用户-修改Socks5代理  socks5://username:password@ipv4:"""
        url = self.interface_url + '/user/SetProxy'
        params = {}
        params['key'] = self.key
        data = {
            'Check': Check,
            'Proxy': Proxy,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置拍一拍名称(self, Value):
        """用户-设置拍一拍名称"""
        url = self.interface_url + '/user/SetSendPat'
        params = {}
        params['key'] = self.key
        data = {
            'Value': Value,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改性别(self, City, Country, Province, Sex):
        """用户-修改性别"""
        url = self.interface_url + '/user/SetSexDq'
        params = {}
        params['key'] = self.key
        data = {
            'City': City,
            'Country': Country,
            'Province': Province,
            'Sex': Sex,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改签名(self, Scene, Val):
        """用户-修改签名"""
        url = self.interface_url + '/user/SetSignature'
        params = {}
        params['key'] = self.key
        data = {
            'Scene': Scene,
            'Val': Val,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置微信号(self, Alisa):
        """用户-设置微信号"""
        url = self.interface_url + '/user/SetWechat'
        params = {}
        params['key'] = self.key
        data = {
            'Alisa': Alisa,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_设置欢迎词配置(self, Enable, Groups, Mode, Rooms, WelcomeMsg):
        """用户-设置欢迎词配置"""
        url = self.interface_url + '/user/SetWelcome'
        params = {}
        params['key'] = self.key
        data = {
            'Enable': Enable,
            'Groups': Groups,
            'Mode': Mode,
            'Rooms': Rooms,
            'WelcomeMsg': WelcomeMsg,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改加好友需要验证属性(self, SwitchType):
        """用户-修改加好友需要验证属性"""
        url = self.interface_url + '/user/UpdateAutoPass'
        params = {}
        params['key'] = self.key
        data = {
            'SwitchType': SwitchType,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_修改名称(self, Scene, Val):
        """用户-修改名称"""
        url = self.interface_url + '/user/UpdateNickName'
        params = {}
        params['key'] = self.key
        data = {
            'Scene': Scene,
            'Val': Val,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def user_上传头像(self, Base64):
        """用户-上传头像"""
        url = self.interface_url + '/user/UploadHeadImage'
        params = {}
        params['key'] = self.key
        data = {
            'Base64': Base64,
        }
        response = requests.post(url, params=params, json=data, headers=headers).json()
        logger.debug(response)
        return response

    def ws_如果key有效则调用WebSocketHandler进行后续处理(self):
        """同步消息-如果 "key" 有效，则调用 WebSocketHandler 进行后续处理。"""
        url = self.interface_url + '/ws/GetSyncMsg'
        params = {}
        params['key'] = self.key
        response = requests.get(url, params=params, headers=headers).json()
        logger.debug(response)
        return response



if __name__ == "__main__":
    client = HttpClient(wxid='wxid_3mpvw4k0b2t722',api_url='http://47.111.150.238:9999',key='7abfc077-68d2-4f31-b5c7-eb4985832272')

    response = client.message_发送文本消息('测试','50175767449@chatroom',aters='wxid_d390bzvm4e3522')