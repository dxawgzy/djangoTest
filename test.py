#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'igis_gzy'

from django.contrib.auth.hashers import make_password
import os

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoTest.settings")

def test1():
    print "please input password:"
    passwd = input()
    # passwd = "123"
    password = make_password(passwd)
    print password

import base64
def test2():
    str1 = 'djhui'
    str2 = base64.b64encode(str1)
    str3 = base64.b64decode(str2)
    hex_format_string = "%%0%ix" % (4 * 2)
    # str1 += b'\x00' * 2
    str1 += b'\x00\x00\x00'
    print str1
    print str2
    print str3
    print hex_format_string


import hashlib
def test3():
    hash = hashlib.sha256()
    hash.update('admin'.encode('utf-8'))
    print hash.hexdigest()
    print hash.digest_size
    print hash.block_size

import urllib, urllib2, base64
def ocr():  #百度OCR文字识别
    access_token = "24.32402e8a9da4394ab059726faeec2f60.2592000.1521953175.282335-10825062"
    # url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + access_token
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
    # 二进制方式打开图文件
    f = open(r'E:\\20180223085328.png', 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        print(content)

if __name__ == '__main__':
    ocr()

