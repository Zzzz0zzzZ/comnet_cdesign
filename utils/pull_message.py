import json
from typing import Dict
from models.group import Group
from models.user import User
from models.user_group import UserGroup
from models.msg_group import MsgGroup
from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from utils.response import response_ws
from models.chat_msg import ChatMsg
from utils.types import ChatType
from utils.response import response_msg


async def pull_single_message(uuid: str):
    single_messages = []
    messages = await ChatMsg.filter(id_to=uuid, chat_type=ChatType.SINGLE.value)
    id_from_single = set()
    for message in messages:
        id_from_single.add(message.uuid_from)

    for uuid_from in id_from_single:
        data = []
        messages = await ChatMsg.filter(uuid_from=uuid_from, id_to=uuid, chat_type=ChatType.SINGLE.value)
        user_from = await User.get(uuid=uuid_from)
        user_to = await User.get(uuid=uuid)
        for message in messages:
            if message.chat_type == ChatType.SINGLE.value:
                data.append({
                    "from": uuid_from,
                    "to": uuid,
                    "time": message.time,
                    "type": message.chat_type,
                    "text": message.content,
                    "msg_type": message.msg_type
                })
            await message.delete()
        data = sorted(data, key=lambda x: x['time'])
        single_messages.append(
            {"user_from": user_from,
             "user_to": user_to,
             "data": data
             }
        )
    return single_messages


async def pull_group_message(uuid: str):
    group_messages = []
    all_groups = await UserGroup.filter(uuid=uuid)  # 该用户所在的所有群组
    all_gid = set()
    for group in all_groups:
        all_gid.add(group.gid)
    data = []
    for gid in all_gid:
        group_to = await Group.get(gid=gid)
        msgGroups = await MsgGroup.filter(gid=gid)
        if len(msgGroups) != 0:
            for msgGroup in msgGroups:
                mid = msgGroup.mid
                message = await ChatMsg.get(mid=mid)
                uuid_from = message.uuid_from
                user_from = await User.get(uuid=uuid_from)
                data.append({
                    "from": uuid_from,
                    "to": gid,
                    "time": message.time,
                    "type": message.chat_type,
                    "text": message.content,
                    "msg_type": message.msg_type,
                    "user_from": user_from
                })
                await msgGroup.delete()
                await message.delete()

            data = sorted(data, key=lambda x: x['time'])
            group_messages.append({
                "group": group_to,
                "data": data
            })
    return group_messages
