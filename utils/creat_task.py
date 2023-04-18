#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import base64
import time

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode

    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# 填写百度控制台中相关开通了“语音合成”接口的应用的的API_KEY及SECRET_KEY
from setting import API_KEY, SECRET_KEY

# API_KEY = '****'
# SECRET_KEY = '****'


"""  获取请求TOKEN start 通过开通语音合成接口的百度应用的API_KEY及SECRET_KEY获取请求token"""


class DemoError(Exception):
    pass


TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    params = {
        'grant_type'   : 'client_credentials',
        'client_id'    : API_KEY,
        'client_secret': SECRET_KEY
    }
    post_data = urlencode(params)
    if IS_PY3:
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if IS_PY3:
        result_str = result_str.decode()

    #    print(result_str)
    result = json.loads(result_str)
    #    print(result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if SCOPE in result['scope'].split(' '):
            return result['access_token']
            # print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        raise DemoError('scope is not correct')
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  获取鉴权结束，TOKEN end """


def send(text):
    """  发送语音合成请求 """

    # 待进行合成的文本，需要为UTF-8编码；输入多段文本时，文本间会插入1s长度的空白间隔
    # text = [
    #     "东风夜放花千树，更吹落，星如雨。宝马雕车香满路。凤箫声动，玉壶光转，一夜鱼龙舞",
    #     "蛾儿雪柳黄金缕，笑语盈盈暗香去。众里寻他千百度，蓦然回首，那人却在，灯火阑珊处"
    # ]

    url = 'https://aip.baidubce.com/rpc/2.0/tts/v1/create'  # 创建长文本语音合成任务请求地址

    body = {
        "text"  : text,
        "format": "mp3-16k",  # 音频格式，支持"mp3-16k","mp3-48k", "wav", "pcm-8k","pcm-16k"
        "voice" : 0,  # 音库，度小宇=1，度小美=0，度逍遥（基础）=3，度丫丫=4；度逍遥（精品）=5003，度小鹿=5118，度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5
        "lang"  : "zh"  # 语言选择,目前只有中英文混合模式，填写固定值"zh"
    }

    # token = {"access_token":"24.19fd456ac888cb1d1cdef56fcb1b567a.2592000.1579157900.282828-11778899"}

    token = {"access_token": fetch_token()}

    headers = {'content-type': "application/json"}

    response = requests.post(url, params=token, data=json.dumps(body), headers=headers)

    # 返回请求结果信息，获得task_id，通过长文本语音合成查询接口，获取合成结果
    print(response.text)
    # text: {"log_id": 16771490845266483, "task_status": "Created", "task_id": "63f7439cb44e12000124a767"}

    # 返回响应头
    # print(response.status_code)

    # 获取task_id
    task_id = json.loads(response.text).get("task_id")
    return task_id


if __name__ == '__main__':
    send("test")
