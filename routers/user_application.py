# coding=utf-8
# @Time : 2023/6/28 9:16 PM
# @Author : 王思哲
# @File : user_application.py
# @Software: PyCharm
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Query
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from models.user_application import UserApplication
from models.user import User
from models.user_relationship import UserRelationship
from utils.response import response_msg

UserApplicationParams = pydantic_model_creator(UserApplication)

router = APIRouter()


class ApplyRequest(BaseModel):
    uuid_from: str
    uuid_to: str
    apply_text: str


@router.post("", description="创建新用户请求")
async def create_application(apply_request: ApplyRequest):

    # 验证from和to是否存在，并且状态不为"FAILED"
    has_application = await UserApplication.filter(
        uuid_from=apply_request.uuid_from,
        uuid_to=apply_request.uuid_to
    ).exclude(apply_status="FAILED").exists()

    if has_application:
        return response_msg("e", "好友关系请求中/已经是好友关系")

    # 接下来创建请求
    new_application = UserApplication(
        uuid_from=apply_request.uuid_from,
        uuid_to=apply_request.uuid_to,
        apply_text=apply_request.apply_text,
        apply_status="PENDING"
    )

    await new_application.save()

    return response_msg("s", "创建请求成功")


@router.get("", description="查询用户新关系")
async def get_application(uuid: str = Query(...)):
    # 找出请求
    application_from_me = await UserApplication.filter(uuid_from=uuid)
    application_to_me = await UserApplication.filter(uuid_to=uuid)

    # 查信息
    for ap_from in application_from_me:
        ap_from.__dict__["uuid_from"] = await User.get(uuid=ap_from.__dict__["uuid_from"])
        ap_from.__dict__["uuid_to"] = await User.get(uuid=ap_from.__dict__["uuid_to"])
    for ap_to in application_to_me:
        ap_to.__dict__["uuid_from"] = await User.get(uuid=ap_to.__dict__["uuid_from"])
        ap_to.__dict__["uuid_to"] = await User.get(uuid=ap_to.__dict__["uuid_to"])

    return response_msg("s", "查询申请关系成功", data={
        "uuid": uuid,
        "application_from_me": [ap_from.__dict__ for ap_from in application_from_me],
        "application_to_me": [ap_to.__dict__ for ap_to in application_to_me]
    })


class UpdateRequest(BaseModel):
    application_id: str
    apply_status: str


@router.put("", description="更新好友关系状态")
async def update_application(up: UpdateRequest):
    ap_info = await UserApplication.get(id=up.application_id)
    ap_info.apply_status = up.apply_status
    ap_info.finish_time = datetime.today()
    await ap_info.save()
    # 添加到relationship表
    if ap_info.apply_status == "SUCCESS":
        await UserRelationship(
            uuid1 = ap_info.uuid_from,
            uuid2 = ap_info.uuid_to
        ).save()
        return response_msg("s", "已成功添加好友")

    return response_msg("s", "更新申请状态成功")
