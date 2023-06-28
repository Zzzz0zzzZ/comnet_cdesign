# coding=utf-8
# @Time : 2023/6/28 9:14 PM
# @Author : 王思哲
# @File : user_application.py
# @Software: PyCharm
from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class UserApplication(Model):
    id = fields.IntField(pk=True)
    uuid_from = fields.CharField(max_length=255, null=False, collation="utf8mb4_general_ci")
    uuid_to = fields.CharField(max_length=255, null=False, collation="utf8mb4_general_ci")
    apply_text = fields.CharField(max_length=255, null=True, collation="utf8mb4_general_ci")
    apply_status = fields.CharField(max_length=255, null=False, collation="utf8mb4_general_ci")
    apply_time = fields.DatetimeField(default=datetime.today())
    finish_time = fields.DatetimeField(null=True)

    class Meta:
        table = "user_application"
