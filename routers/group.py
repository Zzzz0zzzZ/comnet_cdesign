from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from models.group import Group
from models.user_group import UserGroup
from models.user import User
from utils.auth import generate_udid, encode_password, verify_password
from utils.response import response_msg
from utils.group import *

UserParams = pydantic_model_creator(Group)
UserGroupParams = pydantic_model_creator(UserGroup)

router = APIRouter()


class CreateGroup(BaseModel):
    uuid_from: str
    gname: str
    uuid_to: list


@router.post("/create")
async def create_group(group_params: CreateGroup):
    try:
        gid = uuid4()
        newGroup = Group(
            gid=gid,
            gname=group_params.gname
        )
        await newGroup.save()
        add_group_members(group_params.uuid_to, str(gid))
        users = []
        for uuid in group_params.uuid_to:
            user = await User.get(uuid=uuid)
            users.append(user)

        return response_msg("s", "创建成功", {
            "gid": gid,
            "uuid_from": group_params.uuid_from,
            "gname": group_params.gname,
            "members": users
        })
    except Exception as e:
        raise {"msg": str(e), "data": None}
