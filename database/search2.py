#coding=utf8
__author__ = 'igis_gzy'

from django.shortcuts import render
from django.core.context_processors import csrf

#接收POST请求数据
def search_post(request):
    ctx = {}
    ctx.update(csrf(request))
    # if request.POST:
    if request.method == "POST":
        ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)


# 包含所有HTTP POST参数的类字典对象。参见QueryDict 文档。
#
# 服务器收到空的POST请求的情况也是有可能发生的。也就是说，
# 表单form通过HTTP POST方法提交请求，但是表单中可以没有数据。
# 因此，不能使用语句if request.POST来判断是否使用HTTP POST方法；
# 应该使用if request.method == "POST" (参见本表的method属性)。
#
# 注意: POST不包括file-upload信息。参见FILES属性。


