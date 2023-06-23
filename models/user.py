from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    uuid = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    register_time = fields.DatetimeField(auto_now_add=True)
    login_time = fields.DatetimeField(null=True)
    logout_time = fields.DatetimeField(null=True)
    is_login = fields.IntField(default=0)
    udid = fields.CharField(max_length=8)
    avatar = fields.CharField(max_length=1000, null=True)

    class Meta:
        table = "user"