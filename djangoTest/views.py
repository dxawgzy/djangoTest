#coding=utf8

__author__ = 'igis_gzy'

from django.http import HttpResponse

def index(request):
    return HttpResponse(u"欢迎")

