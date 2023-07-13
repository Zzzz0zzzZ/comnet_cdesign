from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel
# from tortoise.contrib.pydantic import pydantic_model_creator

from models.group import Group
from models.user_group import UserGroup
from models.user import User
from utils.auth import generate_udid, encode_password, verify_password
from utils.response import response_msg
from utils.group import *

# UserParams = pydantic_model_creator(Group)
# UserGroupParams = pydantic_model_creator(UserGroup)

router = APIRouter()


class CreateGroup(BaseModel):
    uuid_from: str
    gname: str
    uuid_to: list


@router.post("")
async def create_group(group_params: CreateGroup):
    try:
        gid = uuid4()
        newGroup = Group(
            gid=gid,
            gname=group_params.gname
        )
        await newGroup.save()
        group_params.uuid_to.append(group_params.uuid_from)
        await add_group_members(group_params.uuid_to, str(gid))
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


@router.delete("/{gid}")
async def delete_group(gid: str):
    try:
        delete_members = await UserGroup.filter(gid=gid).delete()
        delete_group = await Group.filter(gid=gid).delete()
        if not delete_members or not delete_group:
            return response_msg("e", "删除失败")
        return response_msg("s", "删除成功")
    except Exception as e:
        raise {"msg": str(e), "data": None}


@router.post("/{uuid}")
async def get_groups(uuid: str):
    try:
        groups_info = []
        groups = await UserGroup.filter(uuid=uuid)
        for group in groups:
            gid = group.gid
            cur_group = await Group.get(gid=gid)
            members = await UserGroup.filter(gid=gid)
            members_info = []
            for member in members:
                user = await User.get(uuid=member.uuid)
                members_info.append(user)
            groups_info.append({
                "group": cur_group,
                "members": members_info
            })
        return response_msg("s", "获取成功", {
            "uuid": uuid,
            "groups": groups_info
        })
    except Exception as e:
        raise {"msg": str(e), "data": None}
