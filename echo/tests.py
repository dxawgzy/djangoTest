# -*- coding: UTF-8 -*-

from django.test import TestCase

# Create your tests here.

from echo.models import Node, Line, Device, Task, Process, Upload
from django.shortcuts import render

#显示各列表信息
def test_lists(request, table):
    #从根据不同的请求，来获取相应的数据,并跳转至相应页面
    if table == 'node':
        # data = Node.objects.all()
        #将原先的data更名为raw_data
        raw_data = Node.objects.all()
        list_template = 'node_list.html'
        sub_title = '节点列表'
    if table == 'line':
        # data = Line.objects.all()
        raw_data = Line.objects.all()
        list_template = 'line_list.html'
        sub_title = '线路列表'
    if table == 'device':
        # data = Device.objects.all()
        raw_data = Device.objects.all()
        list_template = 'device_list.html'
        sub_title = '设备列表'
    #通过GET方法从提交的URL来获取相应参数
    if request.method == 'GET':
        #建立一个空的参数的字典
        kwargs = {}
        #建立一个空的查询语句
        query = ''
        #提交过来的GET值是一个迭代的键值对
        for key, value in request.GET.iteritems():
            #刨去其中的token和page选项
            if key != 'csrfmiddlewaretoken' and key != 'page':
                #由于线路和设备的外键均与node表格有关，当查询线路中的用户名称或设备信息中的使用部门时，可以直接通过以下方式跨表进行查找
                if key == 'node':
                    kwargs['node__node_name__contains'] = value
                    #该query用于页面分页跳转时，能附带现有的搜索条件
                    query += '&' + key + '=' + value
                #其余的选项均通过key来辨别
                else:
                    kwargs[key + '__contains'] = value
                    #该query用于页面分页跳转时，能附带现有的搜索条件
                    query += '&' + key + '=' + value
        #通过元始数据进行过滤，过滤条件为健对值的字典
        data = raw_data.filter(**kwargs)
    #如果没有从GET提交中获取信息，那么data则为元始数据
    else:
        data = raw_data
    #将分页的信息传递到展示页面中去
    # data_list, page_range, count, page_nums = pagination(request, data)
    #建立context字典，将值传递到相应页面
    context = {
        # 'data': data_list,
        'data': data,
        'table': table,
        'query': query,
        # 'page_range': page_range,
        # 'count': count,
        # 'page_nums': page_nums,
        'sub_title': sub_title,
        'head_title': sub_title
    }
    #跳转到相应页面，并将值传递过去
    return render(request, list_template, context)


from django.shortcuts import render, redirect, get_object_or_404
from forms import UploadFileForm
from echo.upload import handle_uploaded_file
# def testpage1(request, pk):
#     #获得一个任务的实例
#     task_ins = get_object_or_404(Task, pk=pk)
#     #如果获取到了POST的提交
#     if request.method == 'POST':
#         #获取form表单，request.FILES是存放文件的地方
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             #通过处理上传文件函数来获得返回值
#             uf = handle_uploaded_file(request.FILES['file'])
#             #获取上传文件的实例，并补充相应信息至数据库中
#             upload_ins = Upload()
#             #绑定相应的task id
#             upload_ins.task_id = task_ins.id
#             #记录相应的文件名
#             upload_ins.upload_title = uf[0]
#             #记录相应的上传路径
#             upload_ins.upload_path = uf[1]
#             #保存upload的实例
#             upload_ins.save()
#             return redirect('task_edit', pk=task_ins.id)
#     else:
#         form = UploadFileForm()
#     #构建相应的context，传递至上传文件页面
#     context = {
#         'form': form,
#         'sub_title': '上传文件',
#         'head_title': '上传文件'
#     }
#     return render(request,'testpage1.html',context)

from django.contrib.auth.decorators import login_required
@login_required
def testpage1(request, pk):
    #获取相关任务实例
    task_ins = get_object_or_404(Task, pk=pk)
    #如果收到了相应的POST提交
    if request.method == 'POST':
        #任务联系人为可编辑选项，并填充原先的任务联系人
        task_ins.task_contacts = request.POST['task_contacts']
        task_ins.save()
        #通过所在task_id获取task对象
        process_task = Task.objects.get(id = task_ins.id)
        #如果获取的实施步骤内容不为空,建立process对象，并增加相关信息
        if request.POST['process_content'].strip(' ') != '':
            process_ins = Process()
            process_ins.task = process_task
            process_ins.process_content = request.POST['process_content'].strip(' ')
            process_ins.process_signer = request.user
            process_ins.save()
        return redirect('task_edit', pk=task_ins.id)
        # return redirect('task_list')
    context = {
        'task': task_ins,
        # 'user': str(request.user),
        'sub_title': '编辑任务',
        'head_title': '编辑任务'
    }
    return render(request, 'testpage1.html', context)


