#coding=utf8
__author__ = 'igis_gzy'

import os,sys
import base64
reload(sys)
sys.setdefaultencoding('utf8')

#定义一个处理上传文件的函数
def handle_uploaded_file(f):
    #获取项目的基本路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        #将上传文件放于media路径下
        #注意： media前面的'/'与否取决于windows或linux平台
        path = os.path.join(BASE_DIR, 'media/')
        #如果没有这个路径则建立
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            file_name = str(path + f.name)
            #以二进制写方式打开，可以读、写文件， 如果文件不存在，创建该文件；如果文件已存在，先清空，再打开文件
            destination = open(file_name, 'wb+')
            #在UploadedFile.chunks()上循环而不是用read(),保证大文件不会大量使用你的系统内存。
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception, e:
        print e

    #返回文件名称及路径
    return f.name, path

def pic_base64(file):
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # try:
    #     #将上传文件放于media路径下
    #     #注意： media前面的'/'与否取决于windows或linux平台
    #     path = os.path.join(BASE_DIR, 'media/')
    #     #如果没有这个路径则建立
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     else:
    #         file_name = str(path + file.name)
    #         #以二进制写方式打开，可以读、写文件， 如果文件不存在，创建该文件；如果文件已存在，先清空，再打开文件
    #         des = open(file_name, 'wb+')
    f=open(file,'rb') #二进制方式打开图文件
    ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
    f.close()
    print ls_f
    return ls_f


