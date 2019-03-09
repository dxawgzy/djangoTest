#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'igis_gzy'

import urllib, urllib2, base64
def ocr():  #百度OCR文字识别
    access_token = "24.1d98c11fd6efc2b048a3cad8e2c6f0ed.2592000.1554689929.282335-10825062"
    # url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + access_token
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
    # 二进制方式打开图文件
    f = open(r'E:\\20180223085328.png', 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    print params
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        print(content)

if __name__ == '__main__':
    ocr()
