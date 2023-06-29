# coding=utf-8
# @Time : 2023/6/28 9:13 PM
# @Author : 王思哲
# @File : user_relationship.py
# @Software: PyCharm
from tortoise import fields
from tortoise.models import Model


class UserRelationship(Model):
    id = fields.IntField(pk=True)
    uuid1 = fields.CharField(max_length=255)
    uuid2 = fields.CharField(max_length=255)

    class Meta:
        table = 'user_relationship'
