# -*- coding: UTF-8 -*-
from django.contrib import admin
from echo.models import Node, Line, Device, Employee

# Register your models here.

# 对NodeAdmin进行个性化配置
class NodeAdmin(admin.ModelAdmin):
    #在list页面上显示指定的字段
    list_display = ('node_name','node_address','node_signer')
    #在编辑、新增页面上排除node_signer的选项
    exclude = ['node_signer']
    #对保存函数进行更改，将登录用户设置为登记人
    def save_model(self, request, obj, form, change):
        obj.node_signer = request.user
        obj.save()


class LineAdmin(admin.ModelAdmin):
    list_display = ('line_code','line_local','line_spname')
    #在编辑、新增页面上排除line_signer的选项
    exclude = ('line_signer',)
    #对保存函数进行更改，将登录用户设置为登记人
    def save_model(self, request, obj, form, change):
        obj.line_signer = request.user
        obj.save()

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_caption','device_type','device_vendor', 'device_ip')
    #在编辑、新增页面上排除device_signer的选项
    exclude = ('device_signer',)
    #对保存函数进行更改，将登录用户设置为登记人
    def save_model(self, request, obj, form, change):
        obj.device_signer = request.user
        obj.save()


admin.site.register(Node,NodeAdmin)
admin.site.register(Line,LineAdmin)
admin.site.register(Device,DeviceAdmin)
admin.site.register(Employee)

