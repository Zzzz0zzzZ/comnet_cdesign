# coding=utf-8
# @Time : 2023/6/28 6:51 PM
# @Author : 王思哲
# @File : ws.py
# @Software: PyCharm
import json
from typing import Dict

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        # uuid
        user_connection = ws.path_params["user"]

        self.active_connections[user_connection] = ws
        print(ws)
        print(self.active_connections)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        user_connection = ws.path_params["user"]
        del self.active_connections[user_connection]
        manager.broadcast(f"用户-{user_connection}-离开")
        print(self.active_connections)

    async def send_personal_message(self, message: str, ws_str: str):
        # 发送个人消息
        ws = self.active_connections[ws_str]
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):

    await manager.connect(websocket)

    await manager.broadcast(f"用户{user}进入聊天室")

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)  # 解析接收到的消息为JSON对象

            if data["type"] == "single":
                await manager.send_personal_message(f"新消息: {data}", data["to"])
                await manager.send_personal_message(f"已发送新消息: {data}", user)
            elif data["type"] == "group":
                pass
            else:
                await manager.broadcast(f"消息类型不支持")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户-{user}-离开")