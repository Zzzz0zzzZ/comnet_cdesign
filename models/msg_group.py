from tortoise import fields
from tortoise.models import Model


class MsgGroup(Model):
    id = fields.IntField(pk=True)
    gid = fields.CharField(max_length=255)
    mid = fields.CharField(max_length=255)

    class Meta:
        table = 'msg_group'
