from models.user_group import UserGroup
from utils.response import response_msg


def add_group_members(uuid_to: list, gid: str):
    try:
        for uuid in uuid_to:
            newUserGroup = UserGroup(
                uuid=uuid,
                gid=gid
            )
            await newUserGroup.save()
    except Exception as e:
        raise {"msg": str(e), "data": None}
