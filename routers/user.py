# coding=utf-8
# @Time : 2023/6/23 8:36 PM
# @Author : 王思哲
# @File : user.py
# @Software: PyCharm
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel
# from tortoise.contrib.pydantic import pydantic_model_creator

from models.user import User
from utils.auth import generate_udid, encode_password, verify_password
from utils.response import response_msg

# UserParams = pydantic_model_creator(User)

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    password: str
    avatar: str


class AuthUserRequest(BaseModel):
    username: str
    password: str


class UpdateUserPhoto(BaseModel):
    uuid: str
    url: str


class UpdateUserLoginStatus(BaseModel):
    uuid: str
    is_login: int


@router.post("/auth")
async def auth_user(user_params: AuthUserRequest):
    cur_user = await User.get_or_none(username=user_params.username)
    if not cur_user:
        return response_msg("e", "用户名或密码错误")

    if not verify_password(
            user_params.password,
            cur_user.password
    ):
        return response_msg("e", "用户名或密码错误")

    return response_msg("s", "登录成功", {
        "user": cur_user
    })


@router.post("")
async def create_user(user_params: CreateUserRequest):
    try:
        uuid = uuid4()
        newUser = User(
            uuid=uuid,
            username=user_params.username,
            password=encode_password(user_params.password),
            udid=generate_udid(uuid)
        )

        has_user = await User.filter(username=user_params.username)
        if has_user:
            return response_msg("e", "用户名已经存在")

        await newUser.save()
        return response_msg("s", "创建成功", {
            newUser
        })

    except Exception as e:
        raise {"msg": str(e), "data": None}


@router.delete("/{uuid}")
async def delete_user(uuid: str):
    deleted_count = await User.filter(uuid=uuid).delete()
    if not deleted_count:
        return response_msg("e", "User not found")

    return response_msg("s", "删除成功")


@router.post("/photo")
async def update_user_photo(user_params: UpdateUserPhoto):
    try:
        user = await User.get(uuid=user_params.uuid)
        user.avatar = user_params.url
        await user.save()
        return response_msg("s", "头像上传成功", user)
    except Exception as e:
        raise {"msg": str(e), "data": None}


@router.post("/status")
async def update_user_login_status(user_params: UpdateUserLoginStatus):
    try:
        user = await User.get(uuid=user_params.uuid)
        user.is_login = user_params.is_login
        await user.save()
        return response_msg("s", "登录状态更改成功", user)
    except Exception as e:
        raise {"msg": str(e), "data": None}
