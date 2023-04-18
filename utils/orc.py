#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author LeoWang
# @date 2023/2/23
from aip import AipOcr
from setting import APP_ID, API_KEY, SECRET_KEY
from utils.util import set_text, get_text

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def recognition(fp):
    # text_res = {
    #     'words_result': [{'words': '接口说明'}, {'words': '语音合成'}, {'words': '接口描述'},
    #                      {'words': '基于该接☐，开发者可以轻讼的获取语音合成萌能力'}], 'words_result_num': 4, 'log_id': 1628698723534206639
    # }
    # text_res = {
    #     'words_result'    : [{'words': '外'}, {'words': '拔毒膏说明书'}, {'words': '请仔细阅读说明书并在医师指导下使用'},
    #                          {'words': '本品含轻粉、红粉'}, {'words': '【药品名称】'}, {'words': '【不良反应】尚不明确'}],
    #     'words_result_num': 49,
    #     'log_id'          : 1628702350592654178
    # }
    # 返回数据
    res = {
        "code": 0,
        "message": '',
        "text": ''
    }
    try:
        # redis中有该文件名, 则直接返回, 减少调用api次数
        # file_name = fp.headers[0][1].split('=')[-1][:-1].strip("\"")
        file_name = fp.filename
        text = get_text(file_name)

    except Exception as e:
        res["code"] = 12
        res['message'] = str(e)
        return res

    if text:
        res['text'] = text
        return res

    try:
        text_res = client.basicGeneral(fp.read())
    except Exception as e:
        res["code"] = 11
        res['message'] = str(e)
        return res
    # 错误处理
    # err: {'log_id': 1628710374968356946, 'error_msg': 'empty image', 'error_code': 216200}
    # print(text_res)
    if 'error_code' in text_res:
        res["code"] = text_res['error_code']
        res['message'] = text_res['error_msg']
        return res

    # 拼接文本
    for item in text_res.get('words_result'):
        res['text'] += f"{item.get('words')}\n"
    set_text(file_name, res['text'])

    return res


import re

# 汉字
zh_reg = r'[\u4e00-\u9fa5]'


def get_drug_name_(content):
    drug_name = content
    # 从文本中提取药品名称
    res = re.findall(r'.*药品名称.?(.*?) ', content)
    print(f"{res=}")
    if res:
        drug_name = res[0].strip()
    return drug_name


def get_drug_name_by_ext(content):
    # 从文本中提取药品名称 通过扩展名
    drug_name = content
    # 从文本中提取包含 药片 胶囊 的文本
    res = re.findall(rf'({zh_reg}*[胶囊|片|剂])', content)
    print(f"{res=}")
    if res:
        # drug_name = ','.join([item.strip() for item in res])
        drug_name = res[0].strip()
    return drug_name


if __name__ == '__main__':
    # with open('../static/fp/temp.jpg', 'rb') as f:
    #     print(recognition(f))
