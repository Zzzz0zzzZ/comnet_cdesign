# coding=utf-8
# @Time : 2023/6/28 6:51 PM
# @Author : 王思哲
# @File : ws.py
# @Software: PyCharm
import json
from typing import Dict

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from utils.response import response_ws

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
        # manager.broadcast(f"用户-{user_connection}-离开")
        print(self.active_connections)

    async def send_personal_message(self, message: Dict, ws_from: WebSocket):
        # 发送个人消息
        try:
            ws = self.active_connections[message["to"]]

            await ws.send_text(response_ws("c", "新消息", data=message))
            # await ws.send_text(f"来自{message['from']}的消息:  {message['text']}")
            await ws_from.send_text(response_ws("s", "已发送新消息", data=message))
            # await ws_from.send_text(f"已发送新消息: {message}")
        except Exception as e:
            await ws_from.send_text(response_ws("w", "对方不在线, 你的消息未发出", data=message))
            # await ws_from.send_text(f"对方不在线, 你的消息{message}未发出")


    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):

    await manager.connect(websocket)

    # await manager.broadcast(f"用户{user}进入聊天室")

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)  # 解析接收到的消息为JSON对象

            if data["type"] == "single":
                await manager.send_personal_message(data, websocket)

            elif data["type"] == "group":
                pass
            else:
                # await manager.broadcast(f"消息类型不支持")
                pass

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"用户-{user}-离开")