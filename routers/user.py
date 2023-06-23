# coding=utf-8
# @Time : 2023/6/23 8:36 PM
# @Author : 王思哲
# @File : user.py
# @Software: PyCharm
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from models.user import User
from utils.auth import generate_udid, encode_password, verify_password

UserParams = pydantic_model_creator(User)

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    password: str
    avatar: str


class AuthUserRequest(BaseModel):
    username: str
    password: str

@router.post("/auth")
async def auth_user(user_params: AuthUserRequest):
    cur_user = await User.get_or_none(username=user_params.username)
    if not cur_user:
        return {"msg": "用户名或密码错误", "data": None}

    if not verify_password(
        user_params.password,
        cur_user.password
    ):
        return {"msg": "用户名或密码错误", "data": None}

    return {
        "msg": "登录成功",
        "data": {
            "user": cur_user
        }
    }

@router.post("")
async def create_user(user_params: CreateUserRequest):

    try:
        uuid = uuid4()
        newUser = User(
            uuid=uuid,
            username=user_params.username,
            password=encode_password(user_params.password),
            udid = generate_udid(uuid)
        )

        has_user = await User.filter(username=user_params.username)
        if has_user:
            return {"msg": "用户名已经存在", "data": None}

        await newUser.save()
        return {
            "msg": "创建成功",
            "data": newUser
        }

    except Exception as e:
        raise {"msg": str(e), "data": None}


@router.delete("/{uuid}")
async def delete_user(uuid: str):
    deleted_count = await User.filter(uuid=uuid).delete()
    if not deleted_count:
        raise {"msg": "User not found", "data": None}

    return {
            "msg": "删除成功",
            "data": None
        }


