from tortoise import fields
from tortoise.models import Model


class MsgGroup(Model):
    id = fields.IntField(pk=True)
    gid = fields.CharField(max_length=255)
    msg_id = fields.IntField()

    class Meta:
        table = 'msg_group'
