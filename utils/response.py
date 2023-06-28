# coding=utf-8
# @Time : 2023/6/28 9:30 PM
# @Author : 王思哲
# @File : response.py
# @Software: PyCharm

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