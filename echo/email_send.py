#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'igis_gzy'

from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from models import EmailVerifyRecord  # 邮箱验证model
from djangoTest.settings import EMAIL_FROM   # setting.py添加的的配置信息
from djangoTest.settings import ALLOWED_HOSTS as host   # setting.py添加的的配置信息


# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def send_email(email, username, send_type):
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.username = username
    email_record.send_type = send_type
    email_record.save()
    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "用户 %s 注册成功，请点击链接激活: http://%s/active/{0}".format(code) % (username, host[-1])
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "重置密码链接"
        email_body = "请点击链接重置用户 %s 的密码: http://%s/forget/{0}".format(code) % (username, host[-1])
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
