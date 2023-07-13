import json
from typing import Dict
from uuid import uuid4

from pydantic import BaseModel

from models.group import Group
from models.user import User
from models.msg_group import MsgGroup
from models.user_group import UserGroup
from fastapi import APIRouter
from utils.response import response_ws
from models.chat_msg import ChatMsg
from utils.types import ChatType
from utils.response import response_msg
from utils.pull_message import pull_single_message, pull_group_message

router = APIRouter()


class UpdateRead(BaseModel):
    mid: str
    is_read: int


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


@router.post("/update/read")
async def update_read(chatParam: UpdateRead):
    try:
        msg = await ChatMsg.get(mid=chatParam.mid)
        msg.is_read = chatParam.is_read
        await msg.save()
        return response_msg("s", "更改已读状态成功", msg)

    except Exception as e:
        raise {"msg": str(e), "data": None}
