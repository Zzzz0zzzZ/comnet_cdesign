# coding=utf-8
# @Time : 2023/6/29 6:15 PM
# @Author : 王思哲
# @File : user_relationship.py
# @Software: PyCharm

from fastapi import APIRouter, Query

from models.user import User
from models.user_relationship import UserRelationship
from utils.response import response_msg

router = APIRouter()


@router.get("", description="查询用户好友")
async def get_user_friends(uuid: str = Query(...)):
    friends1 = await UserRelationship.filter(uuid1=uuid).values("uuid2")
    friends2 = await UserRelationship.filter(uuid2=uuid).values("uuid1")

    result_set = set()

    for f1 in friends1:
        result_set.add(f1["uuid2"])
    for f2 in friends2:
        result_set.add(f2["uuid1"])

    res = []
    for rs in result_set:
        u_info = await User.get_or_none(uuid=rs)
        res.append(u_info.__dict__)

    return response_msg("s", "查询好友关系成功", data={
        "friends": res
    })


