import json
from typing import Dict
from models.group import Group
from models.user import User
from models.user_group import UserGroup
from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from utils.response import response_ws
from models.chat_msg import ChatMsg
from utils.types import ChatType
from utils.response import response_msg


async def pull_single_message(uuid: str):
    single_messages = []
    messages = await ChatMsg.filter(id_to=uuid)
    id_from_single = set()
    for message in messages:
        if message.__dict__['chat_type'] == ChatType.SINGLE.value:
            id_from_single.add(message.__dict__['uuid_from'])

    for uuid_from in id_from_single:
        data = []
        messages = await ChatMsg.filter(uuid_from=uuid_from, id_to=uuid)
        user_from = await User.get(uuid=uuid_from)
        user_to = await User.get(uuid=uuid)
        for message in messages:
            data.append({
                "from": uuid_from,
                "to": uuid,
                "time": message.__dict__['time'],
                "type": message.__dict__['chat_type'],
                "text": message.__dict__['content'],
                "msg_type": message.__dict__['msg_type']
            })
        data = sorted(data, key=lambda x: x['time'])
        single_messages.append(
            {"user_from": user_from,
             "user_to": user_to,
             "data": data
             }
        )
    return single_messages


async def pull_group_message(uuid: str):
    pass
