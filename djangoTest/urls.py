#coding=utf8
"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from calc import views as calc_views
from blog import views as blog_views
from database import views as database_views
from database import search, search2, customer, book
from echo import views as echo_views
from echo.views import RegisterView, ActiveUserView

urlpatterns = [
    # url(r'^$', echo_views.index, name='index'),
    url(r'^ajax/$', calc_views.ajax, name='ajax'),
    url(r'^add1/$', calc_views.add1, name='add1'),  # 127.0.0.1:8000/add/?a=3&b=5
    #url(r'^add2/(\d+)/(\d+)/$', calc_views.add2, name='add2'),  # 127.0.0.1:8000/add2/3/5/
    url(r'^add2/(\d+)/(\d+)/$', calc_views.old_add2_redirect),   #/add2/3/5/ 自动跳转至 /new_add/3/5/
    url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
    url(r'^blog/$', blog_views.blog, name='blog'),
    url(r'^testdb/$', database_views.testdb, name='testdb'),
    url(r'^search-form/$', search.search_form),
    url(r'^search/$', search.search),
    url(r'^search-post/$', search2.search_post),
    url(r'^login02/$', customer.login),
    url(r'^login_form/$', customer.login_form),
    url(r'^logout02/$', customer.logout),
    # url(r'^register/$', customer.register),
    url(r'^register_form/$', customer.register_form),
    url(r'^compare_username/$', customer.compare_username),
    url(r'^compare_password/$', customer.compare_password),
    url(r'^main_page/$', book.main_page),
    url(r'^order/$', book.order),
    url(r'^delete_book/$', book.delete),
    url(r'^shopcart/$', book.shopcart),
    url(r'^order_submit/$', book.order_submit),
    url(r'^admin/', admin.site.urls),

    url(r'^lists/(?P<table>\w+)/$', echo_views.lists, name='lists'),
    url(r'^add/(?P<table>\w+)/$', echo_views.add, name='add'),
    # url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', echo_views.month_archive),
    # url(r'^articles/([0-9]{4})/$', echo_views.year_archive, name='news-year-archive'),
    url(r'^index/', echo_views.index, name='index'),
    url(r'^edit/(?P<table>\w+)/(?P<pk>\d+)/$', echo_views.edit, name='edit'),
    url(r'^delete/(?P<table>\w+)/(?P<pk>\d+)/$', echo_views.delete, name='delete'),
    url(r'^task_list/', echo_views.task_list, name='task_list'),
    url(r'^task_add/', echo_views.task_add, name='task_add'),
    url(r'^task_edit/(?P<pk>\d+)/$', echo_views.task_edit, name='task_edit'),
    url(r'^task_delete/(?P<pk>\d+)/$', echo_views.task_delete, name='task_delete'),
    url(r'^process_edit/(?P<pk>\d+)/$', echo_views.process_edit, name='process_edit'),  #实施步骤
    url(r'^process_delete/(?P<pk>\d+)/$',echo_views.process_delete, name='process_delete'),
    url(r'^login/', echo_views.login, name='login'),
    url(r'^logout/', echo_views.logout, name='logout'),
    url(r'^password_change/', echo_views.password_change, name='password_change'),
    url(r'^register_echo/', RegisterView.as_view(), name='register_echo'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),  # 提取出active后的所有字符赋给active_code
    url(r'^upload_file/(?P<pk>\d+)/$', echo_views.upload_file, name='upload_file'),  #上传附件
    url(r'^task_finish/(?P<pk>\d+)/$', echo_views.task_finish, name='task_finish'),  #结束任务
    url(r'^captcha/', include('captcha.urls')),  #验证码模块
    url('^ajax_val/', echo_views.ajax_val, name='ajax_val'),  #动态验证验证码
    url('^forget_passwd/', echo_views.forget_passwd, name='forget_passwd'),  #找回密码
    url('^map/', echo_views.map, name='map'),  #百度地图
    url('^ocr/', echo_views.ocr, name='ocr'),  #百度OCR文字识别
    url('^tencent/', echo_views.tencent, name='tencent'),  #腾讯AI
    url('^faq/', echo_views.faq, name='faq'),  #图灵机器人
    url(r'^user_list/', echo_views.user_list, name='user_list'),
    url(r'^user_profile/(?P<pk>\d+)/$', echo_views.user_profile, name='user_profile'),
    url(r'^user_delete/(?P<pk>\d+)/$', echo_views.user_delete, name='user_delete'),

]

