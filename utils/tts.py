#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/2/23

from aip import AipSpeech
from setting import APP_ID, API_KEY, SECRET_KEY
from utils.query_result import query
from utils.creat_task import send
from utils.util import get_text, set_text
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def speech(text, vol=5, per=0):
    try:
        # 从缓存中查询
        url_in_redis = get_text(text)
        if url_in_redis:
            return url_in_redis
        # 发送请求, 获取进程id
        task_id = send(text)
        # 使用进程id查询 语音url
        speech_url = query(task_id)
        set_text(text, speech_url)
    except Exception as e:
        return {"code": 11, "message": str(e)}

    return speech_url


# def speech_short(text, vol=5, per=0):
#     call_times = 1
#     if len(text) < 60:
#         from math import ceil
#         # 计算所需调用次数
#         call_times = ceil(len(text) / 60)
#
#     for _ in range(call_times):
#         data = client.synthesis(text, 'zh', 1, {
#             'vol': vol,
#             'per': per,
#         })
#         print(data)
#         if not isinstance(data, dict):
#             with open('../static/temp.mp3', 'wb') as f:
#                 f.write(data)
#         return rf"http://localhost:5000/temp.mp3"


if __name__ == '__main__':
    from utils.orc import recognition

    text_ = recognition(1)
    speech(text_)
