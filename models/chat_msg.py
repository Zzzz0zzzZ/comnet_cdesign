# coding=utf-8
# @Time : 2023/7/11 3:42 PM
# @Author : 王思哲
# @File : chat_msg.py
# @Software: PyCharm
from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class ChatMsg(Model):
    id = fields.IntField(pk=True)
    chat_type = fields.CharField(max_length=255)
    uuid_from = fields.CharField(max_length=255)
    id_to = fields.CharField(max_length=255)
    msg_type = fields.CharField(max_length=255)
    content = fields.CharField(max_length=1000)
    time = fields.DatetimeField(default=datetime.now()) # 这里最好传入收到消息时，消息记录的发送时间
    is_read = fields.IntField(default=0)
    mid = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'chat_msg'
