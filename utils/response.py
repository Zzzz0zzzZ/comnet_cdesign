# coding=utf-8
# @Time : 2023/6/28 9:30 PM
# @Author : 王思哲
# @File : response.py
# @Software: PyCharm
import json
from typing import Dict


def response_msg(
        msg_type: str,
        msg: str,
        data=None
):

    return {
        "msg_type": "error" if msg_type == "e" else "success",
        "msg": msg,
        "data": data
    }

def response_ws(
        msg_type: str,
        msg: str = None,
        data: Dict = None
):
    return json.dumps({
        "msg_type": msg_type,
        "msg": msg,
        "data": data
    })