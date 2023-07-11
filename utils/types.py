# coding=utf-8
# @Time : 2023/7/11 4:25 PM
# @Author : 王思哲
# @File : types.py
# @Software: PyCharm

"""
使用方法： classname.type.value
如：  print(ChatType.SINGLE.value) ---> "SINGLE"  是正确的
而：  print(ChatType.SINGLE) ---> "ChatType.SINGLE"   是错误的
"""

from enum import Enum


# 聊天类型：私聊/群聊
class ChatType(Enum):
    SINGLE: str = "SINGLE"
    GROUP: str = "GROUP"


# 聊天消息的类型：文本/图片/视频/文件
class ChatMsgType(Enum):
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"
    VIDEO: str = "VIDEO"
    FILE: str = "FILE"


# 好友关系申请状态：成功/申请中/失败
class UserRelationApplyStatus(Enum):
    SUCCESS: str = "SUCCESS"
    PENDING: str = "PENDING"
    FAILED: str = "FAILED"
