#coding=utf8
from django import forms
from django.forms import ModelForm
from database.models import User

__author__ = 'igis_gzy'

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())


# class OrderForm():



