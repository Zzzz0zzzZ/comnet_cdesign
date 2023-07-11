# coding=utf-8
# @Time : 2023/7/11 4:49 PM
# @Author : 王思哲
# @File : chatgroup_table.py
# @Software: PyCharm
from tortoise import fields
from tortoise.models import Model


class ChatGroup(Model):
    id = fields.IntField(pk=True)
    chatgroup_id = fields.CharField(max_length=255, null=True)
    chatgroup_name = fields.CharField(max_length=255, null=True)
    uuid = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'chatgroup_table'
