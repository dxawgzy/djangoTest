#coding=utf8
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from database.forms import LoginForm, UserForm

__author__ = 'igis_gzy'

from django.http import HttpResponse
from django.shortcuts import render_to_response
from database.models import User
from database.models import Book

def login_form(request):
    return render_to_response('login02.html', context_instance=RequestContext(request))

# def login(request):
#     try:
#         m = User.objects.get(username=request.POST['username'])
#     except User.DoesNotExist:
#         # return HttpResponse("用户名不存在，请先注册！")
#         return render_to_response('username_not_exist.html',
#                                   {'username':request.POST['username']})
#     if m.password == request.POST['password']:
#         request.session['id'] = m.id
#         user_id = m.id
#         book_list = Book.objects.all()
#         context = {
#             'username':request.POST['username'],
#             'user_id':user_id,
#             'book_list':book_list,
#             # 'next':'/main_page'
#         }
#         # return render_to_response('login02.html', context, context_instance=RequestContext(request))
#         return render_to_response('main_page.html', context)
#     else:
#         return render_to_response('login_failure.html')


def login(request):
    context = {}
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            #获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                m = User.objects.get(username=username)
            except User.DoesNotExist:
                return render_to_response('username_not_exist.html', {'username':username})
            if m.password == password:
                request.session['id'] = m.id
                user_id = m.id
                book_list = Book.objects.all()
                context = {
                    'username':username,
                    'user_id':user_id,
                    'book_list':book_list,
                    'next':'/main_page'
                }
                return render_to_response('main_page.html', context)
            else:
                return render_to_response('login_failure.html')
    else:
        form = UserForm()
    return render_to_response('login02.html', {'form':form}, context_instance=RequestContext(request))



def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    # return HttpResponse("注销成功！")
    return render_to_response('logout.html')


def register_form(request):
    # return render_to_response('register.html')
    return render_to_response('register02.html')

def register(request):
    test1 = User(username=request.GET['username'],
        password=request.GET['password'],
        name=request.GET['name'],
        telephone=request.GET['telephone'],
        email=request.GET['email'],
        address=request.GET['address'])
    try:
        m = User.objects.get(username=request.GET['username'])
        return render_to_response('username_existed.html',
                                  {'username':request.GET['username']})
        # return HttpResponse("用户名已存在")
    except User.DoesNotExist:
        try:
            test1.save()
        except ValueError:
            return render_to_response('register_failure.html')
        return render_to_response('register_success.html')


def compare_username(request):
    try:
        m = User.objects.get(username=request.GET['username'])
        return HttpResponse("用户名已存在")
    except User.DoesNotExist:
        return HttpResponse()
        # return HttpResponse("用户名可注册")

def compare_password(request):
    password = request.GET['password']
    confirm_password = request.GET['confirm_password']
    if(confirm_password == password):
        return HttpResponse()
        # return HttpResponse("密码一致")
    else:
        return HttpResponse("密码不一致")



