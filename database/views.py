#coding=utf8
from django.http import HttpResponse
from django.shortcuts import render
from database.models import Person
# Create your views here.

def testdb(request):   #添加数据
    test1 = Person(name='gzy',  age='24')
    test1.save()
    return HttpResponse("<p>数据添加成功</p>")


# def testdb(request):   #获取数据
#
#     # 初始化
#     response = ""
#     response1 = ""
#
#     # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
#     list = Person.objects.all()
#
#     # filter相当于SQL中的WHERE，可设置条件过滤结果
#     response2 = Person.objects.filter(id=1)
#
#     # 获取单个对象
#     response3 = Person.objects.get(id=1)
#
#     # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
#     Person.objects.order_by("name")[0:2]
#
#     #数据排序
#     Person.objects.order_by("id")
#
#     # 上面的方法可以连锁使用
#     Person.objects.filter(name="gzy").order_by("id")
#
#     # 输出所有数据
#     for var in list:
#         response1 += var.name + var.age + "\n"
#     response = response1
#     return HttpResponse("<p>" + response + "</p>")


# def testdb(request):   #更新数据  修改数据可以使用 save() 或 update():
#
#     # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
#     test1 = Person.objects.get(id=1)
#     test1.name = 'w3cschool菜鸟教程'
#     test1.save()
#
#     #另一种方式
#     # Person.objects.filter(id=1).update(name='w3cschool菜鸟教程')
#
#     #修改所有的列
#     Person.objects.all().update(name='w3cschool菜鸟教程')
#
#     return HttpResponse("<p>修改成功</p>")


# def testdb(request):   #删除数据
#
#     #删除id=1的数据
#     test1 = Person.objects.get(id=5)
#     test1.delete()
#
#     #另一种方式
#     # Person.objects.filter(id=2).delete()
#
#     #删除所有数据
#     # Person.objects.all().delete()
#
#     return HttpResponse("<p>删除成功</p>")


