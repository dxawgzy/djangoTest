Django使用


jqueryschool-国内最大的jquery原创分享社区  http://www.jq-school.com/

七步教你实现Django网站列表自动分页  http://www.django-china.cn/topic/53/

项目更新代码下载地址  https://github.com/erickpeirson/django-pagination

Bootstrap ACE后台管理界面模板(扁平化)  http://www.daimajiayuan.com/plus/download.php?open=0&aid=18152&cid=17

如果您不希望下载并存放 jQuery，那么也可以通过 CDN（内容分发网络） 引用它。
<script src="http://apps.bdimg.com/libs/jquery/1.11.1/jquery.min.js"></script>

日历插件文档地址  http://www.dynarch.com/jscal/

Bootstrap可视化布局系统  http://www.bootcss.com/p/layoutit/#

七.将bootstrap模板ACE引入django  http://blog.csdn.net/alex_chen_16/article/details/50877709
此章节中有误，应该将 ace 解压后的所有文件都放在 static 文件夹

重要文件 index.html （已将所有路径都改好了）

http://v3.bootcss.com/javascript/

Font Awesome 是一套完美的图标字体,主要目的是和 Bootstrap 搭配使用... 安装FontAwesome.otf 字体文件,然后在这个页面直接拷贝粘贴图标字符的代码就可以用于你的设计。  http://fontawesome.io/icons/

精心挑选12款优秀的 JavaScript 日历和时间选择插件
http://www.cnblogs.com/lhb25/archive/2012/10/16/jquery-calendar-timepicker-plugins.html

后台管理：
执行 python manage.py runserver 后，在浏览器输入 http://localhost:8000/admin  admin/1qaz@WSX

============================================================

E:\python\djangoTest>python manage.py makemigrations
System check identified some issues:

WARNINGS:
?: (1_8.W001) The standalone TEMPLATE_* settings were deprecated in Django 1.8 and the TEMPLATES dictionary takes precedence. You must put the values of the following settings into your default TEMPLATES dict: TEMPLATE_DIRS.
Migrations for 'database':
  0001_initial.py:
    - Create model Person

E:\python\djangoTest>

原因是升级之后不推荐使用单独的 TEMPLATES_DIR这样的设置了，使用TEMPLATE = ［］这种就好了
解决方法：将 settings.py 中的 TEMPLATE_DIRS = () 部分屏蔽掉，仅保留 TEMPLATES = [] 部分
    # TEMPLATE_DIRS = (
    #     os.path.join(BASE_DIR,  'templates'),
    # )

==============================================================

setting中数据库设置（屏蔽掉的是默认设置）：
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '10.127.1.32',
        'PORT': '3306',
    }
}

===============================================================

class User(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    name = models.CharField(max_length=40)

之前只有 username 和 password 两行，执行了 makemigrations 和 migrate 之后再数据库中新建了一张表，向表中填写了数据，现在在上述代码中加入了 name 这一行，执行 python manage.py makemigrations 更新数据表时时报错：
You are trying to add a non-nullable field 'name' to user without a default; we can't do that (the database needs something to populate existi
ng rows

意思是 name 字段为非空字段，需要填写默认值：
name = models.CharField(max_length=40, default='DEFAULT VALUE')  或设置该字段可以为空
name = models.CharField(max_length=40, null=True)

python manage.py makemigrations
You are trying to add a non-nullable field 'price_monthly' to product without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option:

{这个是因为之前已创建了表中的一条记录，之后模型中增加了一个非空的字段，但是原来已经存在的记录没有这个值}

网上的相同报错解决方法：
You are trying to add a non-nullable field 'new_field' to userprofile without a default
One option is to declare a default value for 'new_field':
new_field = models.CharField(max_length=140, default='DEFAULT VALUE')
another option is to declare 'new_field' as a nullable field:
new_field = models.CharField(max_length=140, null=True)
If you decide to accept 'new_field' as a nullable field you may want to accept 'no input' as valid input for 'new_field'. Then you have to add the blank=True statement as well:
new_field = models.CharField(max_length=140, blank=True, null=True)
Even with null=True and/or blank=True you can add a default value if necessary:
new_field = models.CharField(max_length=140, default='DEFAULT VALUE', blank=True, null=True)

=================================================================

上方的问题，删掉相应数据表，并删掉 migrations 文件夹中的 0002_user.py 文件后，执行 python manage.py makemigrations 成功，

Migrations for 'database':
  0002_user.py:
    - Create model User

随后执行 python manage.py migrate 失败，报错：
Running migrations:
  No migrations to apply

原因是在 django_migrations 数据表中有一条记录   17  database  0002_user  2016-07-07 06:43:34
使得 Django 认为数据表已创建，因而不再创建，删除掉这一行即可解决问题。

=================================================================

在 app calc 的模板文件夹中加入了 ajax.html 模板文件，执行 http://127.0.0.1:8000/ajax/ 时报错：
TemplateDoesNotExist at /ajax/
ajax.html
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/ajax/
Django Version: 	1.9.7
Exception Type: 	TemplateDoesNotExist
Exception Value: 	

......

Using engine django:

    django.template.loaders.app_directories.Loader: D:\python27\lib\site-packages\django\contrib\admin\templates\ajax.html (Source does not exist)
    django.template.loaders.app_directories.Loader: D:\python27\lib\site-packages\django\contrib\auth\templates\ajax.html (Source does not exist)
    django.template.loaders.app_directories.Loader: E:\python\djangoTest\learn\templates\ajax.html (Source does not exist)
    django.template.loaders.app_directories.Loader: E:\python\djangoTest\database\templates\ajax.html (Source does not exist)
    django.template.loaders.app_directories.Loader: E:\python\djangoTest\blog\templates\ajax.html (Source does not exist)

从最后三行可知，系统在blog、database、learn三个文件夹中查找ajax.html文件，而没有在 calc 中查找，说明 calc 这个APP未被系统识别，原因是：在 settings.py 的INSTALLED_APPS = [} 中未添加 'calc', 这个app

==================================================================

使用 objects.get() 得到的结果只能有且只有一条，不然是会报 DoesNotExist 或者 MultipleObjectsReturned 的错误
MultipleObjectsReturned at /login/
get() returned more than one User -- it returned 2!

修改方法，抛出 DoesNotExist 异常，也可使用 get_object_or_404 方法
try:
    m = User.objects.get(username=request.GET['username'])
except User.DoesNotExist:
    return HttpResponse("用户名不存在，请先注册！")

此外，在注册时要判断用户名是否已存在，若已存在，则无法注册，否则数据库中有相同用户名，报错  MultipleObjectsReturned
    try:
        m = User.objects.get(username=request.GET['username'])
    except User.DoesNotExist:  //抛出 DoesNotExist 异常时说明数据库中不存在该用户名，可以注册
        try:
            test1.save()
        except ValueError:
            return render_to_response('register_failure.html')
        return render_to_response('register_success.html')
    return render_to_response('username_existed.html', {'username':request.GET['username']})

=================================================================

注册时只填了用户名和密码，其他栏目没有填，报错：
ValueError at /register/
invalid literal for int() with base 10: ''
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/register/?username=&password=&confirm_password=&name=&telephone=&email=&address=&register=%E6%B3%A8%E5%86%8C

解决方法：抛出 ValueError 异常
def register(request):
    test1 = User(username=request.GET['username'],
        password=request.GET['password'],
        name=request.GET['name'],
        telephone=request.GET['telephone'],
        email=request.GET['email'],
        address=request.GET['address'])
    try:
        test1.save()
    except ValueError:
        return render_to_response('register_failure.html')
    return render_to_response('register_success.html')


==================================================================

20160711 问题：
使用 Ajax 局部即时刷新页面，注册时填写的用户名已存在时可以立即予以提示
注册栏目没有填写完全时在栏目右侧提示不能为空，注册按钮无法点击（按钮有颜色变化）
密码与确认密码两栏要相同，否则提示密码不一致

解决方法：使用 Ajax 局部即时刷新页面，注册时填写的用户名已存在时可以立即予以提示
在 customer.py 中编写代码，并在 urls.py 中配置该url
def compare_username(request):
    try:
        m = User.objects.get(username=request.GET['username'])
        return HttpResponse("用户名已存在")
        # return HttpResponse({"username_result":"用户名已存在"})
    except User.DoesNotExist:
        return HttpResponse()
        # return HttpResponse("用户名可注册")

url(r'^compare_username/$', customer.compare_username),

在 register02.html 文件头部（head）中加入代码（get 方法调用customer.py 中的 compare_username 方法用来判断用户名是否已存在）：
<script src="http://apps.bdimg.com/libs/jquery/1.11.1/jquery.min.js"></script>
<script>
    $(document).ready(function(){
{#        $('#username').mouseleave(function(){#}
        $('#username').keyup(function(){
            var username = $("#username").val();
            $.get("/compare_username",{'username':username}, function(ret) {
                $('#username_result').html(ret);
            })
        });
    });

</script>

而在body部分则写（get 方法调用customer.py 中的 register 方法用来实现注册功能）：
    <form name="registerForm" method="get" action="/register">

==================================================================

File "E:\python\djangoTest\database\models.py", line 30, in Book
    price = models.FloatField(max_digits=6, decimal_places=2)
TypeError: __init__() got an unexpected keyword argument 'max_digits'

将 FloatField 改为 DecimalField 即可解决问题：
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # price = models.FloatField(max_digits=6, decimal_places=2)

参数中限制 长度4，默认值1均未生效，实际创建表后，长度为11，无默认值（只能手动修改数据表）
quantity = models.IntegerField(max_length=4, default='1')

==================================================================

判断是否已登录（可不用判断，只有登录成功才会显示主页），获取主页上的用户名，并根据用户名找到对应的 user_id ，用于添加订单
每一本书籍后都有一个购买按钮，按钮 id 要能予以区分，在 id 中加上 book_id
购买后书籍剩余数量会减少，并且不能小于0

测试按钮是否生效（点击相应按钮后，会在 result: 显示 success ）：
    $(document).ready(function(){
        $(":button").click(function(){
{#        $("#choose_1").click(function(){#}
            $('#order_result_1').html("success");

<p>result:<span id="order_result_1"></span></p>

==================================================================

在浏览器输入如下地址会报错：http://127.0.0.1:8000/order/?user_id=3&book_id=3
ValueError at /order/
need more than 1 value to unpack
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/order/?user_id=3&book_id=3
Django Version: 	1.9.7	

修改文件（将 def order 中 user_id=request.GET['user_id'] 类似语句注释掉）后，插入Order表中不存在的数据组合成功，再次插入此数据（目的是测试代码中 quantity 数量增加功能）则报错：
AttributeError at /order/
'Order' object has no attribute 'update'
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/order/?user_id=1&book_id=6
Django Version: 	1.9.7	

将代码中 update 改为如下代码可以成功：
        od = Order.objects.get(user_id=request.GET['user_id'],
                               book_id=request.GET['book_id'])
        od.quantity = od.quantity + 1
        od.save()

将语句中的 Order.objects.get 改为 Order.objects.filter 后，插入Order表中不存在的数据组合时都会报错：
Order.objects.get(user_id=request.GET['user_id'],
              book_id=request.GET['book_id']).update(quantity=request.GET['quantity']+1)

MultiValueDictKeyError at /order/
"'quantity'"
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/order/?user_id=1&book_id=6
Django Version: 	1.9.7

==================================================================

    $(document).ready(function(){
        {% for bk in book_list %}
        $("#choose_{{ bk.id }}").click(function(){
{#            $('#order_result_{{ bk.id }}').html("success");#}
            var user_id = $("#{{ user_id }}").val();
            var book_id = $("#{{ bk.id }}").val();
            $.get("/order",{'user_id':user_id, 'book_id':book_id, function(ret) {
{#            $.get("/order",{'user_id':{{ user_id }}, 'book_id':{{ bk.id }}}, function(ret) {#}
                $("#order_result_{{ bk.id }}").html(ret);
            })
        });
        {% endfor %}
    });

在浏览器输入相应信息可以成功，直接点击页面购买按钮报错：
File "E:\python\djangoTest\database\book.py", line 21, in order
    user_id=request.GET['user_id']
  File "D:\python27\lib\site-packages\django\utils\datastructures.py", line 85, in __getitem__
    raise MultiValueDictKeyError(repr(key))
MultiValueDictKeyError: "'user_id'"
[13/Jul/2016 16:47:28] "GET /order/ HTTP/1.1" 500 14163

更改代码如下后，成功：
    $(document).ready(function(){
        {% for bk in book_list %}
        $("#choose_{{ bk.id }}").click(function(){
            $.get("/order",{'user_id':{{ user_id }}, 'book_id':{{ bk.id }}}, function(ret) {
                $("#order_result_{{ bk.id }}").html(ret);
            })
        });
        {% endfor %}
    });

==================================================================

其他按钮都正常，但 user_id=1 book_id=2 这个按钮点击之后报错：
Internal Server Error: /order/
Traceback (most recent call last):
  File "D:\python27\lib\site-packages\django\core\handlers\base.py", line 149, in get_response
    response = self.process_exception_by_middleware(e, request)
  File "D:\python27\lib\site-packages\django\core\handlers\base.py", line 147, in get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "E:\python\djangoTest\database\book.py", line 28, in order
    book_id=request.GET['book_id'])
  File "D:\python27\lib\site-packages\django\db\models\manager.py", line 122, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "D:\python27\lib\site-packages\django\db\models\query.py", line 391, in get
    (self.model._meta.object_name, num)
MultipleObjectsReturned: get() returned more than one Order -- it returned 2!
[14/Jul/2016 09:30:31] "GET /order/?user_id=1&book_id=2 HTTP/1.1" 500 14464

经查，原因是 Order 数据表中 user_id=1 book_id=2 有两条数据

==================================================================

在 def shopcart(request): 中下属语句报错：
order_list = Order.objects.get(user_id = 1)

MultipleObjectsReturned at /shopcart/
get() returned more than one Order -- it returned 6!
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/shopcart/
Django Version: 	1.9.7

原因是 objects.get 只能返回一个结果，而 user_id = 1 用户买了多本不同的书籍，一种书籍对应一条结果（此处有6条结果）
只有 objects.all 才可以返回多条（所有）结果，故应使用 objects.filter 过滤出所有 user_id = 1 的条目

==================================================================

m = User.objects.get(username=request.GET['username'])
request.session['id'] = m.id

然后在整个会话期间通过如下代码即可得到登陆的用户名
username = User.objects.get(id = request.session['id']).username

==================================================================

return HttpResponse("书籍 %s 数量减少一本"  % bk1.bookname) 报错（编码问题）：
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 3: ordinal not in range(128)
[15/Jul/2016 16:05:37] "GET /delete/?user_id=1&book_id=5 HTTP/1.1" 500 14183
Performing system checks..

解决方法：在 book.py 文件中加入如下三条语句即可：
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

==================================================================

注册时提示填写的用户名已存在，如何禁止此时 注册 按钮的点击 （若不做处理，在此时点击 注册 按钮会报错）
customer.py 中的 compare_username 方法是比较用户名是否存在，通过跳转到 username_existed.html 解决（目前尚不知如何禁止点击 注册 按钮）

==================================================================

在登录页面刷新后，登录框中会自动填写了 admin 用户和对应的密码，原因是浏览器记住了密码，解决方法：
在火狐浏览器地址栏前方与 后退<- 按钮之间的那个按钮（也可在页面鼠标右键 查看页面信息），选择 127.0.0.1 右方的箭头，进入详细页面信息，在安全栏点击查看已保存的密码，删掉 admin 即可

==================================================================

NoReverseMatch at /lists/node/
Reverse for 'edit' with arguments '(u'node', 1L)' and keyword arguments '{}' not found. 0 pattern(s) tried: []
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/lists/node/
Django Version: 	1.9.7
Error during template rendering
In template E:\python\djangoTest\echo\templates\node_list.html, error at line 0

网上有解释说是因为某个路径没有在 urls.py 中声明
The problem here is that one of your menu items uses the route xxx without having it declared in urls.py, so a NoReverseMatchError is raised. Does this route exist in your urls ? If you copy pasted from the README example, just comment this out :)
经查，在 res_list.html 中有如下两条信息，并配置了url,而在 urls.py 中没有这两个 url,可以先暂时屏蔽掉 res_list.html 中的相关代码，或在 urls.py 中配置该url，并在 views.py 中编写相应的方法。
<a href="{% url 'edit' table item.id %}" class="tooltip-success" data-rel="tooltip" title="修改信息">
<a href="{% url 'delete' table item.id %}" class="tooltip-error" data-rel="tooltip" title="删除信息">

==================================================================

获取数据库中的数据 id 和 pk
When writing django queries one can use both id/pk as query parameters.
Object.objects.get(id=1)
Object.objects.get(pk=1)
I know that pk stands for Primary Key and is just a shortcut, according to django's documentation. However it is not clear when one should be using id or pk.
It doesn't matter. pk is more independent from the actual primary key field i.e. you don't have to care whether the primary key field is called id or object_id or whatever.

==================================================================

点击列表删除按钮，弹出对话框，点击确定后对话框直接消失了，回到了原来的列表页面，并发送了如下请求：
[21/Jul/2016 15:47:07] "POST /lists/device/ HTTP/1.1" 200 36037
而执行删除操作的  POST delete 请求则未发送，说明点击对话框的确定按钮所对应的操作没有得到执行。

经查， modal_js.html 文件没有传进去（若传进去了，弹出的对话框的信息会被改掉，换成： 删除信息 确认删除该条目么？ 对话框的确定（submit）按钮会关联 rel="{% url 'delete' table item.id %} ，点击确定按钮即发送 POST /delete/node/1/ 请求），在 index.html 文件的 body 部分加入如下语句后解决：
{% block page_javascript %}{% endblock %}

在继承另外的 html 文件时，两个 html 文件中都要在相应的位置加上对应的 {% block %} {% endblock %} ，系统通过 block 标签名来在文件中执行替换操作。

点击对话框的确定按钮，发现无反应，控制台报错：
Internal Server Error: /delete/node/4/
Traceback (most recent call last):
  File "D:\python27\lib\site-packages\django\core\handlers\base.py", line 149, in get_response
    response = self.process_exception_by_middleware(e, request)
  File "D:\python27\lib\site-packages\django\core\handlers\base.py", line 147, in get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "E:\python\djangoTest\echo\views.py", line 184, in delete
    return JsonResponse(data)
  File "D:\python27\lib\site-packages\django\http\response.py", line 500, in __init__
    raise TypeError('In order to allow non-dict objects to be '
TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False
[22/Jul/2016 12:40:07] "POST /delete/node/4/ HTTP/1.1" 500 14602

将 views.py 中的 delete 方法的 return JsonResponse(data) 改为 return JsonResponse(data, safe=False)

==================================================================

在购物车页面点击提交订单按钮（使用 POST 方法），报错：
Forbidden (403)
CSRF verification failed. Request aborted.

将 def shopcart() 方法的 return render_to_response('shopcart.html', context)
改为  return render_to_response('shopcart.html', context, context_instance=RequestContext(request))

RuntimeError at /login
You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to 127.0.0.1:8000/login/ (note the trailing slash), or set APPEND_SLASH=False in your Django settings.
登录注册页面使用 POST 方法时，html 文件中 action="/login/" ，login后面有斜杠 / ，GET方法则没有，否则报错。

此外，POST 方法 html 中必须有 {% csrf_token %} ，对应的 views.py 中有 RequestContext ，否则报错：
总结 GET 改 POST 方法（假设为 login.html ）：
将 login.html 文件的 method 改为 POST ，将 action="/login" 改为 action="/login/" （加了反斜杠 / ），加 {% csrf_token %}
将 def login_form(request) 中的 return render_to_response('login.html')
改为 return render_to_response('login.html', context_instance=RequestContext(request))
将 def login(request) 中的所有 request.GET 改为 request.POST

不过有一问题：登录成功进入主页，页面 url 为 127.0.0.1:8000/login/ 而不是 127.0.0.1:8000/main_page/ ,只有点击进入购物车后再回到主页 url才显示正常。

==================================================================

在购物车页面点击提交订单按钮（使用POST方法），报错：
MultiValueDictKeyError at /order_submit/
"'user1'"
Request Method:     POST
Request URL:        http://127.0.0.1:8000/order_submit
Django Version: 	1.9.7
Exception Type: 	MultiValueDictKeyError

控制台错误日志：
Internal Server Error: /order_submit/
Traceback (most recent call last):
  File "D:\python27\lib\site-packages\django\core\handlers\base.py", line 149, in get_response
    response = self.process_exception_by_middleware(e, request)
  File "D:\python27\lib\site-packages\django\core\handlers\base.py", line 147, in get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "E:\python\djangoTest\database\book.py", line 207, in order_submit
    ctx['user1'] = request.POST['user1']
  File "D:\python27\lib\site-packages\django\utils\datastructures.py", line 85, in __getitem__
    raise MultiValueDictKeyError(repr(key))
MultiValueDictKeyError: "'user1'"
[27/Jul/2016 10:36:21] "POST /order_submit/ HTTP/1.1" 500 66595
D:\python27\lib\site-packages\django\template\defaulttags.py:499: RemovedInDjango110Warning: Reversing by dotted path is deprecated (database.book.shopcart).
  url = reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)

[27/Jul/2016 10:36:22] "GET /order_submit/ HTTP/1.1" 200 863

在 def order_submit(request) 中，加入 try 抛出异常，可以显示订单详情页面，但是没有 user1 bk_list sum 等数据的值
    if request.method == 'POST':
        try:
            context = {
                'user1':request.POST['user1'],
                'bk_list':request.POST['bk_list'],
                'sum':request.POST['sum']
            }
        except MultiValueDictKeyError:
            pass
说明是 request.POST['user1'] 有问题，即使用 POST 传值有问题（经查，是数据本身格式的问题）

通过在 def shopcart()  return HttpResponse(bk_list) 和 def order_submit()  return HttpResponse(request.POST.getlist('bk_list'))
比较打印出的值，发现 shopcart 的 bk_list 值格式为 {}{}{} 多个字典（字典之间无符号予以隔开），order_submit 的 bk_list 值格式为 [{},{},{}]，即将多个字典组成一个数组。def shopcart 中 bk_list.append(bk_dict)，其中 bk_dict = {},
再在 shopcart.html 和 order_submit.html 中加入 <td>{{ bk_list }}</td> <td>{{ bk }}</td> 等信息查看页面显示的结果

==================================================================

使用 echo/templates/regiatration/login.html 时，页面没有布局效果，控制台日志：
[29/Jul/2016 15:43:08] "POST /login/ HTTP/1.1" 200 5834
[29/Jul/2016 15:43:09] "GET /static/assets/css/bootstrap.min.css HTTP/1.1" 404 1697
[29/Jul/2016 15:43:09] "GET /static/assets/css/font-awesome.min.css HTTP/1.1" 404 1706
[29/Jul/2016 15:43:09] "GET /static/assets/css/ace.min.css HTTP/1.1" 404 1679
[29/Jul/2016 15:43:09] "GET /static/assets/css/ace-rtl.min.css HTTP/1.1" 404 1691
[29/Jul/2016 15:43:09] "GET /static/assets/js/jquery.min.js HTTP/1.1" 404 1682
[29/Jul/2016 15:43:09] "GET /login/ HTTP/1.1" 200 5710

即：部分js 及 css 文件找不到，这是因为这些文件为 min 版，min是压缩版,去除了注释和空格,主要是生产环境中使用,不带min是带有注释和空格的,方便阅读源码。而下载的 static 文件夹中非压缩版，不带 min ,因此将这些 文件的 min 去掉即可正常使用。

==================================================================

点击 实施步骤（任务处理-->编辑任务） 的某一条的删除按钮，弹出的对话框始终提示为删除第一条记录，而不是想要删除的那一条。能过删除成功说明删除功能正常，只是调用 modal_js.html 时出了问题，将  task_edit.html 中 
 <a id="modal_button_2" ...  content="确认删除内容为 {{ item.process_content }} 的记录么？" title="删除记录">删除</a>
id 改为  id="modal_button_{{ item.id }}"

==================================================================

                 urls.py               Response              登录按钮              urls.py               Response
浏览器 GET login -------> def login() ---------> login.html ----------> POST login -------> def login() ---------> index.html

def login() 会调用两次，其含有 if request.method == "POST" 语句，GET login 会执行 else 中的语句，跳转到登录 login.html 页面，而 POST login 会执行 if 下的语句，跳转到主页 index.html 。

==================================================================

在登录 login.html 中，用户名使用了 {{ form.username }} ，
request.GET 可以看成一个字典，用GET方法传递的值都会保存到其中，可以用 request.GET.get('key', None)来取值，没有时不报错。
request.POST 是一个类似字典的对象，让你可以通过关键字的名字获取提交的数据。 这个例子中，request.POST['choice'] 以字符串形式返回选择的Choice的ID。request.POST 的值永远是字符串。
上文意思可能是：request.POST 虽然是一个字典，但其中的每个键值对的值均是字符串，而实际上 bk_list 这个键的值是一个由多个字典组成的数组，即 [{},{},{}] ，因此想要遍历这个数组得到相应的数据是有问题的。

==================================================================
[{'author':+u'author',+'bookname':+u'Java+Web',+'id':+1L,+'press':+u'press_abc',+'price':+Decimal('45.50'),+'quantity':+2L},+{'author':+u'abc',+'bookname':+u'JSP',+'id':+2L,+'press':+u'def',+'price':+Decimal('99.80'),+'quantity':+4L},+{'author':+u'abc',+'bookname':+u'Java\u5b66\u4e60',+'id':+3L,+'press':+u'abc',+'price':+Decimal('33.30'),+'quantity':+3L},+{'author':+u'\u5916\u56fd\u4eba',+'bookname':+u'java\u7f16\u7a0b\u601d\u60f3',+'id':+4L,+'press':+u'\u5916\u56fd\u51fa\u7248\u793e',+'price':+Decimal('63.22'),+'quantity':+3L},+{'author':+u'\u7f16\u7a0b\u4e4b\u7f8e\u4f5c\u8005',+'bookname':+u'\u7f16\u7a0b\u4e4b\u7f8e',+'id':+5L,+'press':+u'\u7f16\u7a0b\u4e4b\u7f8e\u51fa\u7248\u793e',+'price':+Decimal('23.00'),+'quantity':+3L},+{'author':+u'\u9762\u5411\u5bf9\u8c61\u7a0b\u5e8f\u8bbe\u8ba1\u4f5c\u8005',+'bookname':+u'\u9762\u5411\u5bf9\u8c61\u7a0b\u5e8f\u8bbe\u8ba1',+'id':+6L,+'press':+u'\u9762\u5411\u5bf9\u8c61\u7a0b\u5e8f\u8bbe\u8ba1\u51fa\u7248\u793e',+'price':+Decimal('33.00'),+'quantity':+5L},+{'author':+u'234',+'bookname':+u'231',+'id':+7L,+'press':+u'42344',+'price':+Decimal('143.00'),+'quantity':+1L}]

==================================================================

点击“结束任务”按钮（将任务状态从“处理中”变为“已结单”）时，出错：
ValueError at /task_finish/7/
The view echo.views.task_finish didn't return an HttpResponse object. It returned None instead.
Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/task_finish/7/
Django Version: 	1.9.7

此处显示调用了 GET 方法，根据 def task_finish() 方法，GET方法确实无返回值，POST方法才有返回值，故点击这个按钮时应该让其调用 POST 方法才行。
将“结束任务”按钮改为如下配置，通过弹出对话框予以处理：

<a id="modal_button_{{ task.id }}" class="red" href="#modal_form" data-toggle="modal"
      rel="{% url 'task_finish' task.id %}" content="确认结束该任务么？" title="结束任务">
      <input class='btn btn-purple' type='button' value='结束任务'/></a>

==================================================================

每个网页页面头部标题设置方法： 在 index.html 中 <head> 下如下设置  <title>{{ head_title }}</title>
再在 views.py 中各个对应的方法中 context 中加入 'head_title' 这个键值对

百分比圆圈图标 easy-pie-chart 无法显示，在 index.html 中导入如下 jquery.easypiechart.js 文件即可
<script src="{%static 'assets/js/jquery.easypiechart.js'%}"></script>

在引入 The Coolest Calendar （jscal2）日历插件时，遇到过一问题，导致点击按钮时日历无法弹出，原因是需要导入的 js css 等文件的导入语句放在了日历的 script 语句的后面，需要先导入相应文件才可使用。

在日历中，由于 css 的原因，导致日历显示框后的日历弹出按钮另起一行，而不是紧挨着显示框，解决方法：使用 span 将 button 包围
<span class="input-group-addon">
    <button id="f_start_btn1" onclick="return false;">...</button>
</span>

task_list.html 文件中日期输入部分有 Datepicker，用来弹出日历的，但实际有问题导致无法使用。在 task_list.html 文件的 {% block container %} 中导入Datepicker需要的 js、css 文件，及 javascript 脚本后问题解决。导入文件及JS脚本位置不能随意变动？？？

导航栏下拉菜单在浏览器全屏时显示正常，浏览器非全屏时下拉菜单跑到了页面正中间，即位置有问题，经查是ACE模板的 ace-nav 样式的问题，将 index.html 文件约第90行处的 ul class="nav ace-nav" 改为 ul class="nav navbar-nav" 可以恢复正常，但是此时各按钮的颜色设置失效。

datatables 插件：在ACE中，我们引入datatables插件，这是一款展示表格，并通过js来实现个包括展示、分页、排序等各种表格功能的插件，而且是高度可定制化的一款插件。官方网站为：http://www.datatables.net/
当然，在我们的ACE模板中也有包含，并加入了ACE的CSS元素。

在 res_list.html 和 task_list.html 文件相应JavaScript脚本处导入如下 css 和 js 文件即可使用 datatables
   <link rel="stylesheet" href="//cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">
    <script src="//cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>

==================================================================

在 Windows下的 Apache 下部署Django 项目：
在 Apache的conf 文件夹下的 http.conf 文件中加入如下配置信息：

     #添加mod_wsgi.so 模块
LoadModule wsgi_module modules/mod_wsgi.so

    #指定myweb项目的wsgi.py配置文件路径
WSGIScriptAlias / E:/python/djangoTest/djangoTest/wsgi.py

    #指定项目路径
WSGIPythonPath E:/python/djangoTest

<Directory E:/python/djangoTest/djangoTest>
<Files wsgi.py>
    Require all granted
</Files>
</Directory>

    #设置静态文件的位置
Alias /static/ E:/python/djangoTest/static/

    #设置静态文件的权限
<Directory E:/python/djangoTest/static>
    Require all granted
</Directory>

pip install wheel 后，即可直接安装下载的 whl 文件，此处在之前已经搭建好Apache和Django的基础上，还需安装 mod_wsgi，下载mod_wsgi-4.4.23+ap24vc9-cp27-cp27m-win_amd64.whl ，使用 pin install 文件名 安装该文件后， 复制 python 安装目录下的 mod_wsgi.so 到 Apache24\modules 目录，修改 Django 项目的 urls.py 中 url(r'^$', echo_views.index, name='index'), 修改 settings.py 中 ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.127.1.32'] ，这样直接输入其中一个 host 都可以进入项目的 index.html 页面。

==================================================================

之前任务列表中，默认显示任务状态为“处理中”的任务，而不是“全部”，但是改为默认显示“全部”后，过滤时报错：
KeyError at /task_list/
'task_status'
Request Method: 	GET
Request URL: 	http://10.127.1.32/task_list/?
csrfmiddlewaretoken=534O5qehDD8kKAQt17Vuv7InVw5Te4BX&task_code=&task_title=&task_signer=&task_category=&task_sta
tus=%E5%85%A8%E9%83%A8&task_start=&task_end=
Django Version: 	1.9.7
Exception Type: 	KeyError
Exception Value: 	'task_status'

E:\python\djangoTest\echo\views.py in task_list  318行
    elif key == 'task_status':
        if value == U'处理中':
            kwargs['task_status'] = '处理中'
        if value == U'已结单':
            kwargs['task_status'] = '已结单'
        #如果选择了所有状态，即对任务状态不进行过滤，那么就删除task_status这个键值对
        if value == U'全部':
            del kwargs['task_status']
        #其余的则根据提交过来的键值对进行过滤
        else:
            kwargs[key + '__contains'] = value

直接屏蔽掉上述代码，问题解决。

==================================================================

在 res_list.html 和 task_list.html 中，使用的翻页和日历插件的css和js使用的是cdn链接直接从相应网站获取，
由于网络原因会导致每次打开相应页面时，翻页和日历插件加载较慢，甚至无法加载，
解决方法是将这些文件下载下来放在本地的static目录下新建的external目录

==================================================================

在任务列表页面，点击一个任务的编辑按钮，在跳转后的页面右上角文字变为了“用户选项”，而不是之前的“欢迎您，xxx”
说明：index.html 中
 <!--判断用户是否已经通过认证，如果通过则显示用户已登陆-->
{% if user.is_authenticated %}
    欢迎您， {{ user.username }}
{% else %}
    用户选项
{% endif %}

如果你使用is_authenticated()判断用户是否登录，那么意味着你采用了django的auth系统，
那么你的登陆最好使用django.contrib.auth中的login方法，该方法会为将user_id以及user_backend放入session中存储，
is_authenticated()通过判断session中是否有user_id 以及user_backend 来判断用户是否登陆。
如果，采用自己的登陆方法，那么有可能没将user_id 或者user_backend 放入session中保存。
所以你的user被django认为没有登录，虽然你已经登陆了。
最好的办法是利用django自己的登陆方法，结合该方法，判断用户是否登陆，从而决定用户的行为。

if语句判断出现了问题，原因是task_edit()中，最后返回context含有语句 'user': str(request.user),
导致认证失败，屏蔽此语句问题解决。但此时会引入新的问题：在编辑任务页面右侧的 处理过程列表中，每个过程
下的编辑、删除按钮消失，因为 task_edit.html 中
{% if user == item.process_signer and task.task_status == '处理中' %}
需要用到 user，而前文将其屏蔽，导致不满足if条件，按钮消失。
疑问：index.html中同样用到了user，但没有通过context参数传值，如何得到user值（根据前文解释是通过session，原理？），
如何在task_edit.html 中使用同样的方法？
解决方法：参考index.html，将task_edit.html 中 {% if user == item 改为  {% if user.username == item 即可

==================================================================

==================================================================



