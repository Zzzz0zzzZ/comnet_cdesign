# coding=utf-8
# @Time : 2023/7/11 4:49 PM
# @Author : 王思哲
# @File : group.py
# @Software: PyCharm
from tortoise import fields
from tortoise.models import Model


class Group(Model):
    id = fields.IntField(pk=True)
    gid = fields.CharField(max_length=255, null=True)
    gname = fields.CharField(max_length=255, null=True)
    uuid = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'group'
