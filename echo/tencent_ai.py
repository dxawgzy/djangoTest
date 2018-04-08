#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'igis_gzy'

import time, urllib, urllib2, hashlib, requests, json, base64
from random import Random

def random_str(randomlength=10):  #用于生成指定长度随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def tencent_chat():  #腾讯AI-智能闲聊
    str = raw_input("Enter your input: ")
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    app_key = "xxx"
    params = {
        'app_id': '1106664443',
        'time_stamp': int(time.time()),  #获取当前时间戳，保留整数
        'nonce_str': random_str(),  # 随机字符串
        'session': '腾讯AI开放平台',
        'question': str,
        # 'sign': '',  #此条目不不参加get_sign中的计算
    }
    pa = sorted(params.items()) #按字典key首字母升序排列
    pa.append(('app_key',app_key))
    str1 = urllib.urlencode(pa).encode()
    sha = hashlib.md5()
    sha.update(str1)
    md5text = sha.hexdigest().upper()
    params['sign'] = md5text
    r = requests.post(url, data=params)
    respond = json.loads(r.text)
    if respond['ret'] ==0:
        result = respond['data']['answer']
    else:
        result = respond['msg']
    print u"机器人回复：" + result

def tencent_card():  #腾讯AI-身份证识别
    src = r'E:\\776986996205527761.jpg'
    f = open(src, 'rb')
    img = base64.b64encode(f.read())  # 图像base64编码
    url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_idcardocr"
    app_key = "xxx"
    params = {
        'app_id': '1106664443',
        'time_stamp': int(time.time()),  #获取当前时间戳，保留整数
        'nonce_str': random_str(),  # 随机字符串
        # 'sign': '',  #此条目不不参加get_sign中的计算
        'image': img,
        'card_type': 1   # 身份证图片类型，0-正面，1-反面
    }
    pa = sorted(params.items()) #按字典key首字母升序排列
    pa.append(('app_key',app_key))
    str1 = urllib.urlencode(pa).encode()
    sha = hashlib.md5()
    sha.update(str1)
    md5text = sha.hexdigest().upper()
    params['sign'] = md5text
    # r = requests.post(url, data=params)
    # respond = json.loads(r.text)
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    response = urllib2.urlopen(request)
    respond = response.read()
    # text = json.loads(respond)
    print respond
    # if respond['ret'] ==0:
    #     result = respond['data']
    # else:
    #     result = respond['msg']
    # print result

if __name__ == '__main__':
    # tencent_chat()
    tencent_card()
