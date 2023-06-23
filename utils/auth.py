# coding=utf-8
# @Time : 2023/6/23 9:38 PM
# @Author : 王思哲
# @File : auth.py
# @Software: PyCharm
import hashlib
from uuid import uuid4, UUID

def encode_password(p: str):
    hash_object = hashlib.sha256(p.encode('utf-8'))
    return hash_object.hexdigest()


def verify_password(op: str, ep: str):
    return encode_password(op) == ep

def generate_udid(uuid: UUID):
    uuid = str(uuid)
    UD_LOC = [13, 7, 2, 11, 9, 29, 23, 26]
    return "".join([uuid.replace("-", "")[_] for _ in UD_LOC])


if __name__ == '__main__':
    a = uuid4()
    print(a)
    print(generate_udid(a))