#coding=utf8
from django.shortcuts import render

# Create your views here.

from blog.models import BlogsPost
from django.shortcuts import render_to_response

def blog(request):
    blog_list = BlogsPost.objects.all()  #获取数据库里面所拥有BlogPost对象
    #render_to_response()返回一个页面(ajax.html)，
    # 顺带把数据库中查询出来的所有博客内容（blog_list）也一并返回。
    return render_to_response('blog.html',{'blog_list':blog_list})
    # return render(request, 'index.html',{'blog_list':blog_list})

