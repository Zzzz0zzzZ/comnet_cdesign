import json
from typing import Dict
from uuid import uuid4

from models.group import Group
from models.user import User
from models.msg_group import MsgGroup
from models.user_group import UserGroup
from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from utils.response import response_ws
from models.chat_msg import ChatMsg
from utils.types import ChatType
from utils.response import response_msg
from utils.pull_message import pull_single_message, pull_group_message

router = APIRouter()


@router.post("/pull/{uuid}")
async def pull_message(uuid: str):
    try:
        single_msg = await pull_single_message(uuid)
        group_msg = await pull_group_message(uuid)
        return_info = {
            "single_msg": single_msg,
            "group_msg": group_msg
        }
        return response_msg("s", "获取成功", return_info)

    except Exception as e:
        raise {"msg": str(e), "data": None}
