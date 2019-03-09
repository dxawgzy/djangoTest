#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'igis_gzy'

import urllib, urllib2, base64, json

def ocr():  #百度OCR文字识别
    access_token = "24.1d98c11fd6efc2b048a3cad8e2c6f0ed.2592000.1554689929.282335-10825062"
    # type = "general_basic"   # 通用文字识别
    type = "idcard"   # 身份证识别
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/%s?access_token=%s" % (type, access_token)
    # f = open(r'E:\\20180223085328.png', 'rb')   # 二进制方式打开图文件
    f = open(r'E:\\20180416105731.jpg', 'rb')
    img = base64.b64encode(f.read())   # 参数image：图像base64编码
    # params = {"image": img}   # 通用文字识别
    params = {"image": img, "id_card_side": "front"}   # 身份证识别
    # print params
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        # result = json.dumps(json.loads(content, encoding='utf-8'), ensure_ascii=False)
        # print(result)
        print(content)

# if __name__ == '__main__':
#     ocr()

# 引入文字识别OCR SDK
from aip import AipOcr
# 定义常量
APP_ID = '10825062'
API_KEY = 'lToSW42BhCMnYiqCLA0eDguK'
SECRET_KEY = 'MAjfTk2tawRWRheMCw3McnUAGsu8KnKE'
# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
# 初始化ApiOcr对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 调用通用文字识别接口
# result = aipOcr.basicGeneral(get_file_content('E:\\20180223085328.png'))

# 设置识别身份证正面参数
id_card_side = 'front'
# 调用身份证识别接口
result = aipOcr.idcard(get_file_content('E:\\20180416105731.jpg'), id_card_side)
print result
