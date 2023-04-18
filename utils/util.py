#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/2/24

import redis

r = redis.StrictRedis(
    host='120.***.**.***',
    port=6379,
    db=11,
    password='********'
)


# def read_text(file_name):
#     with open('../static/data/name2text.txt', "r") as f:
#         f.read()

def set_text(key, value):
    r.set(key, value)


def get_text(key):
    data = r.get(key)
    if not data:
        return None
    text = str(data, encoding="utf-8")
    # print(f"get {key}: {text}")
    return text


if __name__ == '__main__':
    # set_text('name', 12312)
    print(get_text('temp.jpg'))
