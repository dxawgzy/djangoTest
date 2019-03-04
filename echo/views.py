# -*- coding: UTF-8 -*-
import json, time, hashlib, urllib, urllib2, base64, requests
from django.contrib.auth import views, authenticate, login as auth_login, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from echo.models import Node, Line, Device, Task, Process, Upload, EmailVerifyRecord
from echo.upload import handle_uploaded_file, pic_base64
from echo.forms import NodeForm, LineForm, DeviceForm, TaskForm, ProcessForm, UploadFileForm, LoginForm, CaptchaForm, RegisterForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.cache import cache_page
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from email_send import send_register_email

# Create your views here.

def login02(request):  #用户登陆
    #extra_context是一个字典，它将作为context传递给template，这里告诉template成功后跳转的页面将是/index
    template_response = views.login(request, extra_context={'next': '/index'})
    return template_response

def login(request):
    form = CaptchaForm()
    if request.method == 'GET':
        if request.GET.get('newsn') == '1':  #刷新验证码
            csn = CaptchaStore.generate_key()
            cimageurl = captcha_image_url(csn)
            return HttpResponse(cimageurl)
        return render(request, 'login.html', {'form': form})
    else:
        login_param = dict()
        code_param = dict()
        login_param['username'] = request.POST.get('username', None)  #如果不存在则默认值为None
        login_param['password'] = request.POST.get('password', None)
        code_param['captcha_0'] = request.POST.get('captcha_0', None)
        code_param['captcha_1'] = request.POST.get('captcha_1', None)
        login_form = LoginForm(login_param)
        code_form = CaptchaForm(code_param)
        if code_form.is_valid():
            if login_form.is_valid():
                user = authenticate(**login_form.cleaned_data)
                if user:
                    if user.is_active:
                        auth_login(request, user)
                        return HttpResponseRedirect('/index')
                    else:
                        return render(request, 'login.html',
                                      {'username': login_param['username'], 'form': form,
                                       'err_message': u'用户未激活'})
                else:
                    return render(request, 'login.html',
                                  {'username': login_param['username'], 'form': form,
                                   'err_message': u'用户名密码错误'})
            else:
                return render(request, 'login.html',
                              {'form': form, 'err_message': u'用户名密码格式错误'})
        else:
            return render(request, 'login.html',
                          {'username': login_param['username'], 'form': form,
                           'err_message': u'验证码错误'})

def logout(request):  #用户退出
    #logout_then_login表示退出即跳转至登陆页面，login_url为登陆页面的url地址
    template_response = views.logout_then_login(request, login_url='/login')
    return template_response

def password_change12(request):  #密码更改
    #post_change_redirect表示密码成功修改后将跳转的页面.
    template_response = views.password_change(request, post_change_redirect='/index')
    return template_response

def password_change(request):  #修改密码
    if request.method == 'POST':
        username = request.user  #获取当前登录的用户名
        user = User.objects.get(username=username)
        passwd = user.password  #获取数据库中保存的用户密码
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if check_password(old_password, passwd):  #判断输入的原密码是否和数据库中的密码一致
            if new_password1 == new_password2:
                user.password = make_password(new_password1)  #更改密码
                user.save()
                # update_session_auth_hash(request, username)
                return HttpResponseRedirect('/index')
            else:
                return render(request, 'password_change.html', {'err_message': u'新密码与确认密码不一致'})
        else:
            return render(request, 'password_change.html', {'err_message': u'原密码错误'})
    context = {
        'head_title': '修改密码'
    }
    return render(request, 'password_change.html', context)

@login_required  #登录的强制认证（在进入主页前自动跳转到登录页面）
# @cache_page(60 * 15)  #秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def index(request):  #显示首页
    node_number = Node.objects.count()
    line_number = Line.objects.count()
    device_number = Device.objects.count()
    task_number = Task.objects.count()
    if task_number == 0:
        task_complete = 0
        task_complete_percent = 0
    else:
        task_complete = Task.objects.filter(task_status='已结单').count()  #获取已结单的数量,用于计算任务完成率
        task_complete_percent = round(float(task_complete)/task_number*100,2) #用float可以保留小数，round保留小数点2位
    context = {  #将相关参数传递给dashboard页面
        'node_number': node_number,
        'line_number': line_number,
        'device_number': device_number,
        'task_number': task_number,
        'task_complete': task_complete,
        'task_complete_percent': task_complete_percent,
        'head_title': '信息汇总'
    }
    return render(request, 'dashboard.html', context)

@login_required
# @cache_page(60 * 15)
def lists(request, table):  #显示各列表信息
    if table == 'node':  #从根据不同的请求，来获取相应的数据,并跳转至相应页面
        raw_data = Node.objects.all()
        list_template = 'node_list.html'
        sub_title = '节点列表'
    if table == 'line':
        raw_data = Line.objects.all()
        list_template = 'line_list.html'
        sub_title = '线路列表'
    if table == 'device':
        raw_data = Device.objects.all()
        list_template = 'device_list.html'
        sub_title = '设备列表'
    if request.method == 'GET':  #通过GET方法从提交的URL来获取相应参数
        kwargs = {}  #建立一个空的参数的字典
        query = ''  #建立一个空的查询语句
        for key, value in request.GET.iteritems():  #提交过来的GET值是一个迭代的键值对
            if key != 'csrfmiddlewaretoken' and key != 'page':  #刨去其中的token和page选项
                #由于线路和设备的外键均与node表格有关，当查询线路中的用户名称或设备信息中的使用部门时，可以直接通过以下方式跨表进行查找
                if key == 'node':
                    kwargs['node__node_name__contains'] = value
                    query += '&' + key + '=' + value  #该query用于页面分页跳转时，能附带现有的搜索条件
                else:  #其余的选项均通过key来辨别
                    kwargs[key + '__contains'] = value
                    query += '&' + key + '=' + value
        data = raw_data.filter(**kwargs)  #通过原始数据进行过滤，过滤条件为健对值的字典
    else:  #如果没有从GET提交中获取信息，那么data则为原始数据
        data = raw_data
    # data_list, page_range, count, page_nums = pagination(request, data)  #将分页的信息传递到展示页面中去
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
    return render(request, list_template, context)  #跳转到相应页面，并将值传递过去

@login_required
def add(request, table):
    if table == 'node':  #根据提交的请求不同，获取来自不同Form的表单数据
        form = NodeForm(request.POST or None)
        sub_title = '添加节点'
    if table == 'line':
        form = LineForm(request.POST or None)
        sub_title = '添加线路'
    if table == 'device':
        form = DeviceForm(request.POST or None)
        sub_title = '添加设备'
    if form.is_valid():
        instance = form.save(commit=False)
        if table == 'node':
            instance.node_signer = request.user  #将登录用户作为登记人
        if table == 'line':
            instance.line_signer = request.user
        if table == 'device':
            instance.device_signer = request.user
        instance.save()
        return redirect('lists', table=table)  #跳转至列表页面,配合table参数，进行URL的反向解析
    context = {
        'form': form,
        'table': table,
        'sub_title': sub_title,
        'head_title': sub_title
    }
    return render(request, 'res_add.html', context)  #如果没有有效提交，则仍留在原来页面

@login_required
def edit(request, table, pk):  #修改数据,函数中的pk代表数据的id
    if table == 'line':
        #这是Django的一个快捷方法,通过pk去line表中取值，如果有值则返回，如果无值则抛出http404的异常
        #具体信息可参考https://docs.djangoproject.com/en/1.9/topics/http/shortcuts/
        table_ins = get_object_or_404(Line, pk=pk)
        form = LineForm(request.POST or None, instance=table_ins)  #通过instance来将Form的数据做填充
        sub_title = '修改线路信息'
    if table == 'node':
        table_ins = get_object_or_404(Node, pk=pk)
        form = NodeForm(request.POST or None, instance=table_ins)
        sub_title = '修改节点信息'
    if table == 'device':
        table_ins = get_object_or_404(Device, pk=pk)
        form = DeviceForm(request.POST or None, instance=table_ins)
        sub_title = '修改设备信息'
    if form.is_valid():
        instance = form.save(commit=False)  #创建实例，需要做些数据处理，暂不做保存
        #将登录用户作为登记人,在修改时，一定要使用str强制,因为数据库中以charfield方式存放了登记人
        if table == 'node':
            instance.node_signer = str(request.user)
        if table == 'line':
            instance.line_signer = str(request.user)
        if table == 'device':
            instance.device_signer = str(request.user)
        instance.save()  #保存该实例
        return redirect('lists', table=table)  #跳转至列表页面,配合table参数，进行URL的反向解析
    context = {
        'table': table,
        'form': form,
        'sub_title': sub_title,
        'head_title': sub_title
    }
    return render(request, 'res_add.html', context)  #与res_add.html用同一个页面，只是edit会在res_add页面做数据填充

@login_required
def delete(request, table, pk):  #删除操作
    if table == 'line':  #选择相应的表格
        table_ins = get_object_or_404(Line, pk=pk)  #通过id值获取相应表格的实例，有值则返回，无值则抛出异常
    if table == 'node':
        table_ins = get_object_or_404(Node, pk=pk)
    if table == 'device':
        table_ins = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':  #接收通过AJAX提交过来的POST
        try:
            table_ins.delete()
            data = 'success'  #删除成功,则data信息为success
        except IntegrityError:
            data = 'error'  #如因外键问题，或其他问题，删除失败，则报error
        #将最后的data值传递至JS页面，进行后续处理，safe是将对象序列化，否则会报TypeError错误
        return JsonResponse(data, safe=False)

# def pagination(request, queryset, display_amount=5, after_range_num = 5, before_range_num = 4):  #分页函数
#     try:  #按参数分页
#         page = int(request.GET.get("page", 1))  #从提交来的页面获得page的值
#         if page < 1:  #如果page值小于1，那么默认为第一页
#             page = 1
#     except ValueError:  #若报异常，则page为第一页
#             page = 1
#     paginator = Paginator(queryset, display_amount)  #引用Paginator类
#     count = paginator.count  #总计的数据条目
#     num_pages = paginator.num_pages  #合计页数
#     try:
#         objects = paginator.page(page)  #尝试获得分页列表
#     except EmptyPage:  #如果页数不存在
#         objects = paginator.page(paginator.num_pages)  #获得最后一页
#     except PageNotAnInteger:  #如果不是一个整数
#         objects = paginator.page(1)  #获得第一页
#     temp_range = paginator.page_range  #根据参数配置导航显示范围
#     if (page - before_range_num) <= 0:  #如果页面很小
#         if temp_range[-1] > after_range_num:  #如果总页面比after_range_num大，那么显示到after_range_num
#             page_range = xrange(1, after_range_num+1)
#         else:  #否则显示当前页
#             page_range = xrange(1, temp_range[-1]+1)
#     elif (page + after_range_num) > temp_range[-1]:  #如果页面比较大
#         page_range = xrange(page-before_range_num,temp_range[-1]+1)  #显示到最大页
#     else:  #否则在before_range_num和after_range_num之间显示
#         page_range = xrange(page-before_range_num+1, page+after_range_num)
#     return objects, page_range, count, num_pages  #返回分页相关参数

@login_required
def task_list(request):  #任务列表
    if request.method == 'GET':  #如果通过GET来获取了相应参数，那么进行查询
        kwargs = {}  # 建立过滤条件的键值对
        # kwargs['task_status'] = '处理中'  #默认显示处理中的任务
        query = ''  # 用于分页显示的query
        for key, value in request.GET.iteritems():
            if key != 'csrfmiddlewaretoken' and key != 'page':  #除去token及page的参数
                #如果查询的是与处理过程相关的，那么需要通过外键跳转至process表格，使用 process__ 实现
                if key == 'process_content':
                    if value !='':  # __contains 的意思是包含，类似于 like '%aaa%'
                        kwargs['process__process_content__contains'] = value
                elif key == 'process_signer':
                    if value !='':
                        kwargs['process__process_signer__contains'] = value
                elif key == 'task_start':  #定义任务的开始与结束时间
                    if value != '':       # __gte 大于等于  __lte 小于等于
                        kwargs['task_signtime__gte'] = value
                elif key == 'task_end':
                    if value != '':
                        kwargs['task_signtime__lte'] = value
                # elif key == 'task_status':  #定义任务的状态
                #     if value == U'处理中':
                #         kwargs['task_status'] = '处理中'
                #     if value == U'已结单':
                #         kwargs['task_status'] = '已结单'
                #     #如果选择了所有状态，即对任务状态不进行过滤，那么就删除task_status这个键值对
                #     if value == U'全部':
                #         # del kwargs['task_status']
                #         kwargs['task_status'] = ''
                else:  #其余的则根据提交过来的键值对进行过滤
                    kwargs[key + '__contains'] = value
                query += '&' + key + '=' + value  #建立用于分页的query
        data = Task.objects.filter(**kwargs).order_by('task_signtime')  #按照登记时间排序
    else:  #如果没有GET提交过来的搜索条件，那么默认按照登记时间排序，并只显示处理中的任务
        # data = Task.objects.filter(task_status='处理中').order_by('task_signtime')
        data = Task.objects.all().order_by('task_signtime')
    # data_list, page_range, count, page_nums = pagination(request, data)  #将分页的信息传递到展示页面中去
    context = {
        # 'data': data_list,
        'data': data,
        'query': query,
        # 'page_range': page_range,
        # 'count': count,
        # 'page_nums': page_nums,
        'sub_title': '任务列表',
        'head_title': '任务列表'
    }
    return render(request, 'task_list.html', context)  #跳转到相应页面，并将值传递过去

@login_required
def task_add(request):  #新建任务
    form = TaskForm(request.POST or None)  #从TaskForm获取相关信息
    if form.is_valid():
        task_ins = Task()  #建立一个task实例
        task_ins.task_code = str(int(time.time()))  #通过时间来建立一个任务流水
        task_ins.task_title = form.cleaned_data.get('task_title')  #获取task的相关信息
        task_ins.task_category = form.cleaned_data.get('task_category')
        task_ins.task_contacts = form.cleaned_data.get('task_contacts')
        task_ins.task_status = '处理中'  #task建立后默认变成处理中的状态
        task_ins.task_signer = request.user  #通过登录用户来辨别任务登记人
        task_ins.save()  #保存task实例
        member_task = Task.objects.get(id = task_ins.id)  #通过当前task_id获取task对象，并将其赋给member_task
        members = form.cleaned_data.get('task_member')  #获取members集合
        for member in members:  #获取members集合中的member,并将其添加到member_task中,增添相应实施人员
            member_task.task_member.add(member)
        process_task = Task.objects.get(id = task_ins.id)  #通过task_id获取task对象
        process_ins = Process()  #建立一个process的实施步骤实例
        process_ins.task = process_task  #将process实例与task绑定
        process_ins.process_content = form.cleaned_data.get('process_content')  #获取process相关信息
        process_ins.process_signer = request.user
        process_ins.save()
        return redirect('task_list')
    context = {
        'form': form,
        'sub_title': '新建任务',
        'head_title': '新建任务'
    }
    return render(request, 'task_add.html', context)

@login_required
def task_edit(request, pk):  #编辑任务
    task_ins = get_object_or_404(Task, pk=pk)  #获取相关任务实例
    if request.method == 'POST':
        task_ins.task_contacts = request.POST['task_contacts']  #任务联系人为可编辑选项，并填充原先的任务联系人
        task_ins.save()
        process_task = Task.objects.get(id = task_ins.id)  #通过所在task_id获取task对象
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
    return render(request, 'task_edit.html', context)

@login_required
def task_delete(request, pk):  #删除任务
    task_ins = get_object_or_404(Task, pk=pk)  #获取选定的task实例
    if request.method == 'POST':
        try:
            task_ins.delete()
            data = 'success'  #删除成功,则data信息为success
        except IntegrityError:
            data = 'error'  #如因外键问题，或其他问题，删除失败，则报error
        #将最后的data值传递至JS页面，进行后续处理，safe是将对象序列化，否则会报TypeError错误
        return JsonResponse(data, safe=False)

@login_required
def process_edit(request, pk):  #实施步骤的修改（编辑任务页面右侧处理过程下方的编辑按钮）
    process_ins = get_object_or_404(Process, pk=pk)  #获取相应的实施步骤
    if request.method == 'POST':
        form = ProcessForm(request.POST)  #调用process的form
        if form.is_valid():
            process_ins.process_content = request.POST['process_content'].strip(' ')
            process_ins.process_signtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            process_ins.save()
            return redirect('task_edit', pk=process_ins.task_id)
    form = ProcessForm(initial={'process_content': process_ins.process_content})  #将之前的process内容放入processform
    context = {
        'id': process_ins.task_id,
        'form': form,
        'sub_title': '编辑实施步骤',
        'head_title': '编辑实施步骤'
    }
    return render(request, 'process_edit.html', context)

@login_required
def process_delete(request, pk):  #实施步骤删除（编辑任务页面右侧处理过程下方的“删除”按钮）
    process_ins = get_object_or_404(Process, pk=pk)  #获取相应的实施步骤
    if request.method == 'POST':
        try:
            process_ins.delete()
            data = 'success'  #删除成功,则data信息为success
        except IntegrityError:
            data = 'error'  #如因外键问题，或其他问题，删除失败，则报error
        #将最后的data值传递至JS页面，进行后续处理，safe是将对象序列化，否则会报TypeError错误
        return JsonResponse(data, safe=False)

@login_required
def upload_file(request, pk):  #上传附件
    task_ins = get_object_or_404(Task, pk=pk)  #获得一个任务的实例
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  #获取form表单，request.FILES是存放文件的地方
        if form.is_valid():
            uf = handle_uploaded_file(request.FILES['file'])  #通过处理上传文件函数来获得返回值
            upload_ins = Upload()  #获取上传文件的实例，并补充相应信息至数据库中
            upload_ins.task_id = task_ins.id   #绑定相应的task id
            upload_ins.upload_title = uf[0]  #记录相应的文件名
            upload_ins.upload_path = uf[1]  #记录相应的上传路径
            upload_ins.save()  #保存upload的实例
            return redirect('task_edit', pk=task_ins.id)
    else:
        form = UploadFileForm()
    context = {
        'form': form,
        'sub_title': '上传文件',
        'head_title': '上传文件'
    }
    return render(request, 'upload.html', context)

@login_required
def task_finish(request, pk):  #结束任务
    task_ins = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        try:
            task_ins.task_status = '已结单'  #将task的状态置为已结单
            task_ins.save()
            process_task = Task.objects.get(id = task_ins.id)  #在process增加一条记录，标识某人结束了该项任务
            process_ins = Process()
            process_ins.task = process_task
            process_ins.process_content = str(request.user) + u'完成了该任务并结单'
            process_ins.process_signer = request.user
            process_ins.save()
            data = 'success'  #返回JSON值，success
        except IntegrityError:
            data = 'error'  #返回JSON值，error
        return HttpResponse(json.dumps(data), content_type = "application/json")  #通过json形式返回相关数值

class RegisterView(View):   #用户注册
    def get(self, request):
        register_form = RegisterForm()
        if request.GET.get('newsn') == '1':  #刷新验证码
            csn = CaptchaStore.generate_key()
            cimageurl = captcha_image_url(csn)
            return HttpResponse(cimageurl)
        return render(request, 'register_echo.html', {'register_form':register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username", "")
            email = request.POST.get("email", "")
            password1 = request.POST.get("password", "")
            password2 = request.POST.get("repeat_password", "")
            is_user_exist = User.objects.filter(username=user_name)  #判断用户是否已经存在
            if is_user_exist:
                return render(request, 'register_echo.html', {'register_form': register_form, 'msg': u'用户名已存在'})
            if password2 != password1:
                return render(request, 'register_echo.html', {'register_form': register_form, 'msg': u'密码不一致'})
            user_profile = User()  #实例化用户，然后赋值
            user_profile.username = user_name
            user_profile.email = email
            user_profile.is_active = False  #新建用户为非活跃用户，可通过验证变为活跃用户
            user_profile.password = make_password(password1)  #将密码明文转换为密文
            user_profile.save()  # 保存到数据库
            send_register_email(email, user_name, "register")  #此处加入了邮箱验证的手段
            # form = CaptchaForm()
            # return render(request, 'login.html', {'username': user_name, 'form': form})
            return render(request, 'registered_success.html')
        else:
            # form表单验证失败，将错误信息传给前端
            return render(request, 'register_echo.html', {'register_form': register_form, 'msg': u'注册失败'})

class ActiveUserView(View):  #注册的用户通过邮件激活
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  #用code在数据库中过滤出信息
        if all_records:
            for record in all_records:
                username = record.username
                user = User.objects.get(username=username)
                user.is_active = True  #激活用户
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'active_success.html')

def ajax_val(request):  #动态验证验证码（焦点离开验证码输入框时验证）
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(response=request.GET['response'],
                                         hashkey=request.GET['hashkey'])
        if cs:
            json_data={'status':1}
        else:
            json_data = {'status':0}
        return JsonResponse(json_data)
    else:
        json_data = {'status':0}
        return JsonResponse(json_data)

def forget_passwd(request):
    return render(request, 'forget_passwd.html')

def map(request):  #百度地图
    if request.method == 'GET':
        address =  request.GET.get('address')
    context = {
        'head_title': '百度地图',
        'address': address
    }
    return render(request, 'baidu_map.html', context)

def ocr(request):  #百度OCR文字识别
    access_token = "24.32402e8a9da4394ab059726faeec2f60.2592000.1521953175.282335-10825062"
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + access_token
    # url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
    # params = {
    #     'image': '',
    #     # 'language_type': 'CHN_ENG',
    #     # 'detect_direction': 'false',
    #     # 'detect_language': 'false',
    #     # 'probability': 'false',
    # }
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)  #获取form表单，request.FILES是存放文件的地方
        # if form.is_valid():
            # f = open(request.FILES['file'], 'rb')
            # uf = pic_base64(request.FILES['file'])  #通过处理上传文件函数来获得返回值
            # img = base64.b64encode(f.read())
        img = request.POST.get("base64_output", "")
        params = {"image": img}
        params = urllib.urlencode(params)
        request1 = urllib2.Request(url, params)
        request1.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request1)
        content = response.read()
        print (content)
        result = content['words_result']
        # r = requests.post(url, data=params)
        # respond = json.loads(r.text)
        # result = respond['words_result']
        return render(request, 'baidu_ocr.html', {'reply_message': content})
    else:
        form = UploadFileForm()
    context = {
        'head_title': '百度OCR',
        'form': form,
    }
    return render(request, 'baidu_ocr.html', context)

from random import Random  #用于生成指定长度随机字符串
def random_str(randomlength=10):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def tencent(request):  #腾讯AI
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    app_key = "8RiXkm6qaiKP1pTc"
    if request.method == 'POST':
        params = {
            'app_id': '1106664443',
            'time_stamp': int(time.time()),  #获取当前时间戳，保留整数
            'nonce_str': random_str(),  # 随机字符串
            'session': '腾讯AI开放平台',
            'question': request.POST.get('message'),
            # 'sign': '',  #此条目不不参加get_sign中的计算
        }
        pa = sorted(params.items()) #按字典key首字母升序排列
        pa.append(('app_key',app_key))
        str1 = urllib.urlencode(pa).encode()
        sha = hashlib.md5()
        sha.update(str1)
        md5text = sha.hexdigest().upper()
        params['sign'] = md5text
        r = requests.post(url, data=params)
        respond = json.loads(r.text)
        if respond['ret'] ==0:
            result = respond['data']['answer']
        else:
            result = respond['msg']
        return render(request, 'tencent_ai.html', {'reply_message': result})
    context = {
        'head_title': '腾讯AI',
    }
    return render(request, 'tencent_ai.html', context)

def faq(request):  #图灵机器人
    tuling_key = "5b50e5980c24483088a1129f18abec58"
    url = "http://www.tuling123.com/openapi/api"
    if request.method == 'POST':
        msg =  request.POST.get('message')
        # username = request.user  #获取当前登录的用户名
        # user_id = username.replace('@', '')[:30]
        user_id = "123sfdfdfs"
        body = {'key': tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
        r = requests.post(url, data=body)
        respond = json.loads(r.text)
        result = ''
        if respond['code'] == 100000:
            result = respond['text'].replace('<br>', '  ')
            result = result.replace(u'\xa0', u' ')
        elif respond['code'] == 200000:
            result = respond['text'].replace('<br>', '  ') +": " + respond['url']
        elif respond['code'] == 302000:
            for k in respond['list']:
                result = result + u"【" + k['source'] + u"】 " +\
                    k['article'] + "\t" + k['detailurl'] + "\n"
        elif respond['code'] == 308000:
            for k in respond['list']:
                result = result + u"【" + k['name'] + u"】 " +\
                    k['icon'] + u" k['name'] " + "\t" + k['detailurl'] + "\n"
        else:
            result = respond['text'].replace('<br>', '  ')
            result = result.replace(u'\xa0', u' ')
        return render(request, 'faq.html', {'reply_message': result})
    context = {
        'head_title': '图灵FAQ',
    }
    return render(request, 'faq.html', context)

@login_required
def user_list(request):  #用户列表
    if request.method == 'GET':  #如果通过GET来获取了相应参数，那么进行查询
        kwargs = {}  # 建立过滤条件的键值对
        query = ''  # 用于分页显示的query
        for key, value in request.GET.iteritems():
            if key != 'csrfmiddlewaretoken' and key != 'page':  #除去token及page的参数
                kwargs[key + '__contains'] = value
                query += '&' + key + '=' + value  #建立用于分页的query
        data = User.objects.filter(**kwargs)
    else:
        data = User.objects.all().order_by('username')
    context = {
        'data': data,
        'query': query,
        'sub_title': '用户列表',
        'head_title': '用户列表'
    }
    return render(request, 'user_list.html', context)

@login_required
def user_profile(request, pk):  #用户详情
    user_ins = get_object_or_404(User, pk=pk)
    context = {
        'user_ins': user_ins,
        'sub_title': '用户详情',
        'head_title': '用户详情'
    }
    return render(request, 'user_profile.html', context)

@login_required
def user_delete(request, pk):  #删除用户
    user_ins = get_object_or_404(User, pk=pk)
    try:
        record = EmailVerifyRecord.objects.get(username=user_ins.username)
        record.delete()  #同步删除注册时的激活链接数据
    except ObjectDoesNotExist:  # 如果没有链接数据，不做处理
        pass
    if request.method == 'POST':
        try:
            user_ins.delete()
            data = 'success'
        except IntegrityError:
            data = 'error'  #如因外键问题，或其他问题，删除失败，则报error
        #将最后的data值传递至JS页面，进行后续处理，safe是将对象序列化，否则会报TypeError错误
        return JsonResponse(data, safe=False)

@login_required
def user_forbidden(request, pk):  #用户下拉菜单——冻结用户
    user_ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        try:
            user_ins.is_active = False
            user_ins.save()
            data = 'success'
        except IntegrityError:
            data = 'error'  #如因外键问题，或其他问题失败，则报error
        #将最后的data值传递至JS页面，进行后续处理，safe是将对象序列化，否则会报TypeError错误
        return JsonResponse(data, safe=False)

@login_required
def user_active(request, pk):  #用户下拉菜单——激活用户
    user_ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        try:
            user_ins.is_active = True
            user_ins.save()
            data = 'success'
        except IntegrityError:
            data = 'error'  #如因外键问题，或其他问题失败，则报error
        #将最后的data值传递至JS页面，进行后续处理，safe是将对象序列化，否则会报TypeError错误
        return JsonResponse(data, safe=False)
