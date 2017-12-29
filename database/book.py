# coding=utf8

__author__ = 'igis_gzy'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from database.models import Book, User, Order
from  django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext

def main_page(request):
    user_id = request.session['id']
    username = User.objects.get(id=user_id).username
    book_list = Book.objects.all()

    paginator = Paginator(book_list, 5)
    page_num = request.GET.get('page')
    try:
        book_list = paginator.page(page_num)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    context = {
        'username': username,
        'user_id': user_id,
        'book_list': book_list
    }
    return render_to_response('main_page.html', context)


#分页函数
def pagination(request, queryset, display_amount=3, after_range_num=5, before_range_num=4):
    #按参数分页
    try:
        #从提交来的页面获得page的值
        page = int(request.GET.get("page", 1))
        #如果page值小于1，那么默认为第一页
        if page < 1:
            page = 1
    #若报异常，则page为第一页
    except ValueError:
        page = 1
    #引用Paginator类
    paginator = Paginator(queryset, display_amount)
    #总计的数据条目
    count = paginator.count
    #合计页数
    num_pages = paginator.num_pages

    try:
        #尝试获得分页列表
        objects = paginator.page(page)
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except PageNotAnInteger:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    temp_range = paginator.page_range

    #如果页面很小
    if (page - before_range_num) <= 0:
        #如果总页面比after_range_num大，那么显示到after_range_num
        if temp_range[-1] > after_range_num:
            page_range = xrange(1, after_range_num + 1)
        #否则显示当前页
        else:
            page_range = xrange(1, temp_range[-1] + 1)
    #如果页面比较大
    elif (page + after_range_num) > temp_range[-1]:
        #显示到最大页
        page_range = xrange(page - before_range_num, temp_range[-1] + 1)
    #否则在before_range_num和after_range_num之间显示
    else:
        page_range = xrange(page - before_range_num + 1, page + after_range_num)
    #返回分页相关参数
    return objects, page_range, count, num_pages


# 点击 order 按钮一次只增加一本书
def order(request):
    # user_id=request.GET['user_id']
    # book_id=request.GET['book_id']
    # order1 = Order(user_id, book_id)
    # book_id 是从书籍列表页面得到的，说明书籍数量最少为1本，否则列表中无此书籍
    # 因此 Book.objects.get 不需要异常处理
    order1 = Order(user_id=request.GET['user_id'],
                   book_id=request.GET['book_id'])
    book1 = Book.objects.get(id=request.GET['book_id'])
    try:
        # Order.objects.get(user_id, book_id).update(quantity=request.GET['quantity']+1)
        # Order.objects.get(user_id=request.GET['user_id'],
        #       book_id=request.GET['book_id']).update(quantity=request.GET['quantity']+1)
        od = Order.objects.get(user_id=request.GET['user_id'],
                               book_id=request.GET['book_id'])
        od.quantity = od.quantity + 1
        od.save()
        book1.sum_quantity = book1.sum_quantity - 1
        book1.save()
        # if book1.sum_quantity == 0:  #当书籍数量为0时，直接禁用购买按钮即可
        #     book1.delete()
        # else:
        #     book1.sum_quantity = book1.sum_quantity -1
        #     book1.save()
        return HttpResponse("书籍《%s》再次购买一本" % book1.bookname)
    except Order.DoesNotExist:
        try:
            order1.save()
            return HttpResponse("书籍《%s》已添加至购物车" % book1.bookname)
        except ValueError:
            return HttpResponse("无法将书籍《%s》添加至购物车" % book1.bookname)


# 点击 delete 按钮一次只删一本书
def delete(request):
    try:
        od = Order.objects.get(user_id=request.GET['user_id'],
                               book_id=request.GET['book_id'])
        book1 = Book.objects.get(id=request.GET['book_id'])
        if (od.quantity > 1):
            od.quantity = od.quantity - 1
            od.save()
            book1.sum_quantity = book1.sum_quantity + 1
            book1.save()
            return HttpResponse("书籍《%s》数量减少一本" % book1.bookname)
        else:
            od.delete()
            return HttpResponse("书籍《%s》删除成功" % book1.bookname)
    except Order.DoesNotExist:
        # pass
        return HttpResponse("尚未购买此书籍，无法进行删除操作")


def shopcart(request):
    user_id = request.session['id']
    user1 = User.objects.get(id=user_id)
    order_list = Order.objects.filter(user_id=user_id).order_by('book_id')
    bk_list = []
    sum = 0
    if order_list:
        #判断数组 order_list 是否为空，若为空{}，for 中 Book.objects.get 会报错
        for od in order_list:
            bk = Book.objects.get(id=od.book_id)
            sum = sum + bk.price * od.quantity
            bk_dict = {'id': bk.id, 'bookname': bk.bookname, 'author': bk.author,
                       'press': bk.press, 'price': bk.price, 'quantity': od.quantity}
            bk_list.append(bk_dict)

    #将分页的信息传递到展示页面中去
    # bk_list, page_range, count, page_nums = pagination(request, bk_list)
    #建立context字典，将值传递到相应页面
    context = {
        # 'page_range': page_range,
        # 'count': count,
        # 'page_nums': page_nums,
        'user1': user1,
        'sum': sum,
        'bk_list': bk_list
    }
    #跳转到相应页面，并将值传递过去
    return render_to_response('shopcart.html', context, context_instance=RequestContext(request))
    # return HttpResponse(bk_list)


# 提交订单，进入 订单详情页面 order_detail.html
# 目前此代码很多与 def shopcart() 重复，如何通过修改减少重复
# 点 提交订单 按钮后，应该直接把购物车页面书籍信息通过某种方式传到订单页面
# def order_submit(request):
#     user_id = request.session['id']
#     user1 = User.objects.get(id=user_id)
#     order_list = Order.objects.filter(user_id = user_id).order_by('book_id')
#     bk_list = []
#     sum = 0
#     if order_list:
#         for od in order_list:
#             bk = Book.objects.get(id=od.book_id)
#             sum = sum + bk.price * od.quantity
#             bk_dict = {'id':bk.id, 'bookname':bk.bookname, 'author':bk.author,
#                        'press':bk.press, 'price':bk.price, 'quantity':od.quantity}
#             bk_list.append(bk_dict)
#     context = {
#         'user1':user1,
#         'bk_list':bk_list,
#         'sum':sum
#     }
#     #跳转到相应页面，并将值传递过去
#     return render_to_response('order_detail.html', context)



def order_submit(request):
    user_id = request.session['id']
    user1 = User.objects.get(id=user_id)
    # 接收POST请求数据
    if request.method == 'POST':
        bk_list1 = request.POST['bk_list']
        # bk_list1 = request.POST.get('bk_list')
        bk_list2 = bk_list1.strip('[{}]')  #删除字符串中开头、结尾处的 [{ 和 }] 字符
        # bk_list2 = bk_list1.strip('[]')
        # r = re.compile('},{')
        # bk_list3 = r.split(bk_list1)
        # bk_list = bk_list2.split("}")
        bk_list3 = bk_list2.split("}")

        booklist = []
        bookdict = {}
        for bk1 in bk_list3:
            bk2 = bk1.lstrip(',{').replace(':', ',').split(',')
            # return HttpResponse(bk2)
            bookdict = {'id': bk2[5], 'bookname': bk2[3], 'author': bk2[1],
                       'press': bk2[7], 'price': bk2[9], 'quantity': bk2[11]}
            # for i in range(0, len(bk2), 2):
            #     bookdict[bk2[i]] = bk2[i+1]

            booklist.append(bookdict)
            # return HttpResponse(booklist)

        sum = request.POST['sum']
        context = {
            'user1':user1,
            'sum':sum,
            'bk_list':booklist
        }
    # return HttpResponse(booklist)
    return HttpResponse(bk_list1)
    # return render_to_response('order_detail.html', context, context_instance=RequestContext(request))



