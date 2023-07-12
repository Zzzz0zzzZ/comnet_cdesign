from tortoise import fields
from tortoise.models import Model


class UserGroup(Model):
    id = fields.IntField(pk=True)
    uuid = fields.CharField(max_length=255, null=True)
    gid = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'user_group'
