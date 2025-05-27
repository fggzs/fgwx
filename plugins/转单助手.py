from loguru import logger
from utils.pluginbase import *
import re
import sqlite3
import threading
from typing import Optional
from contextlib import contextmanager
import queue
import os

class DatabasePool:
    """数据库连接池"""
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = queue.Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        
        # 初始化连接池
        for _ in range(max_connections):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self.connections.put(conn)
        
        # 初始化数据库表
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS phone_mapping (
                    phone TEXT PRIMARY KEY,
                    sender TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        conn = None
        try:
            conn = self.connections.get(timeout=5)
            yield conn
        finally:
            if conn:
                self.connections.put(conn)

    def close_all(self):
        """关闭所有连接"""
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()

class 转单助手(PluginBase):
    """转单助手"""
    def __init__(self):
        self.metadata = {
            "name": "转单助手",
            "version": "1.0.0",
            "author": "fg",
            "description": "转单助手 - 根据手机号转发消息",
            "priority": 50,
            "block": False
        }
        # 数据库连接池
        self.db_pool = DatabasePool("data/phone_mapping.db")
        # 目标转发wxid
        self.load_forward_configs()
        # 确保data目录存在
        os.makedirs("data", exist_ok=True)
        self.enable()

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'db_pool'):
            self.db_pool.close_all()

    def add_mapping(self, phone: str, sender: str):
        """添加或更新映射关系"""
        with self.db_pool.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # 使用 REPLACE INTO 语句，如果手机号已存在则更新，不存在则插入
                cursor.execute(
                    "REPLACE INTO phone_mapping (phone, sender, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                    (phone, sender)
                )
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"添加映射关系失败: {e}")
                raise

    def get_sender(self, phone: str) -> Optional[str]:
        """获取手机号对应的发送人"""
        with self.db_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sender FROM phone_mapping WHERE phone = ?", (phone,))
            row = cursor.fetchone()
            return row['sender'] if row else None

    def extract_phone(self, text):
        """提取文本中的手机号"""
        # 匹配11位手机号
        pattern = r'1[3-9]\d{9}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    def load_forward_configs(self, config_file="data/转单配置.txt"):
        """从文本文件加载转发配置"""
        self.forward_configs = []
        try:
            if not os.path.exists(config_file):
                with open(config_file, "w", encoding="utf-8") as f:
                    f.write('关键词----转单wxid----开启')

            with open(config_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    parts = line.split("----")
                    if len(parts) >= 3:
                        keyword, wxid, status = parts
                        self.forward_configs.append({
                            "keyword": keyword.strip(),
                            "wxid": wxid.strip(),
                            "status": status.strip()
                        })
            logger.info(f"成功加载 {len(self.forward_configs)} 条转发配置")
        except Exception as e:
            logger.error(f"加载转发配置失败: {e}")
            # 默认配置
    async def process(self, msg: Msg):
        """处理消息"""
        try:
            # 获取消息内容
            content = msg.content
            sender = msg.sender

            # 检查消息是否来自配置的转发wxid
            for config in self.forward_configs:  # forward_configs是配置列表，格式如[{"keyword":"ibox自助", "wxid":"wxid_3dg486h47q5j22", "status":"开启"}]
                if config["status"] != "开启":
                    continue
                
                # 如果是来自配置的转发wxid的回复
                if sender == config["wxid"]:
                    # 提取手机号
                    phone = self.extract_phone(content)
                    if phone:
                        # 查找映射关系
                        target_sender = self.get_sender(phone)
                        if target_sender:
                            # 转发给原发送人
                            self.clinet.message_发送文本消息(content, target_sender)
                            logger.info(f"转发回复消息: {phone} -> {target_sender}")
                            return
                
                # 如果是客户发送的消息
                elif config["keyword"] in content:
                    # 提取手机号
                    phone = self.extract_phone(content)
                    if phone:
                        # 添加或更新映射关系
                        self.add_mapping(phone, sender)
                        
                        # 转发消息给配置的wxid
                        self.clinet.message_发送文本消息(content, config["wxid"])
                        logger.info(f"转发消息: {sender} -> {config['wxid']} (手机号: {phone})")
                        return

        except Exception as e:
            logger.error(f"处理消息失败: {e}")
        return

            
