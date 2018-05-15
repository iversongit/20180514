import datetime
import random
import time

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from shopper.filters import GoodsFilter
from shopper.models import Banner, Nav, MustBuy, Shop, MainProducts, UserModel, UserSession, Goods, OrderModel, \
    OrderGoodsModel, FoodTypes, CartModel
from shopper.serializers import GoodsSerializer
from django.core.urlresolvers import reverse


def home(request):
    banner = Banner.objects.all()
    nav = Nav.objects.all()
    mustbuy = MustBuy.objects.all()

    shop = Shop.objects.all()

    mainproducts = MainProducts.objects.all()

    data = {
        "banner":banner,
        "nav":nav,
        "mustbuy":mustbuy,
        "shop":shop,
        "mainproducts":mainproducts
    }
    return render(request,'home/home.html',data)

def login(request):
    if request.method == "GET":
        return render(request,'user/user_login.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("login-password:",password)
        # 一次只能一个用户登录
        if UserModel.objects.filter(username=username).exists(): #　如果用户名存在
            user = UserModel.objects.get(username=username)
            if password == user.password:  # 验证密码
                s = 'abcdefghijklmnopqrstuvwxyz1234567890'
                ticket = ""
                for i in range(15):
                    # 获取随机的字符串，每次获取一个字符
                    ticket += random.choice(s)
                now_time = int(time.time()) # 1970.1.1到现在的秒数
                ticket_value = 'TK_' + ticket + str(now_time)
                # 绑定令牌到cookie里面
                response = HttpResponseRedirect("/shopapp/home")
                response.set_cookie("ticket",ticket_value)
                # 存在数据库中
                expire_time = datetime.datetime.now() + datetime.timedelta(days=1)
                UserSession.objects.create(
                    session_key="ticket",
                    session_data=ticket_value,
                    expire_time= expire_time,
                    u_id=user.id
                )
                # user.ticket = ticket
                # user.save()
                return response
            else:
                return render(request,"user/user_login.html",{"errorpassword":"密码错误"})
        else:
            return render(request,"user/user_login.html",{"errorusername":"用户不存在"})

def regist(request):
    if request.method == "GET":
        return render(request,"user/user_register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("regist-password:",password)
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        if sex == '男':
            sex = 1
        elif sex == '女':
            sex = 0
        icon = request.FILES.get('icon')
        UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            sex=sex,
            icon=icon
        )
        return HttpResponseRedirect("/shopapp/login/")

def logout(request):
    if request.method == "GET":
        response = HttpResponseRedirect("/shopapp/login/")
        ticket = request.COOKIES.get("ticket")
        response.delete_cookie("ticket")
        UserSession.objects.get(session_data=ticket).delete()
        return response

def mine(request):
    user = request.user
    data = {}
    if user and user.id:
        orders = user.ordermodel_set.all()
        wait_pay,pay =0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1
            elif order.o_status == 1 or order.o_status == 2:
                pay += 1
        data = {
            "wait_pay":wait_pay,
            "pay":pay
        }
    return render(request,"mine/mine.html",data)

from rest_framework import mixins, viewsets
from rest_framework.response import Response
class GoodsEdit(mixins.ListModelMixin, # 获取所有信息
                mixins.RetrieveModelMixin, # 获取指定信息，可以通过id来查询
                mixins.UpdateModelMixin, # 修改指定信息，可以使用put/patch方法
                mixins.DestroyModelMixin, # 删除指定信息，可以使用delete方法
                mixins.CreateModelMixin, # 创建指定信息，可以使用post方法
                viewsets.GenericViewSet): # 可以调用get_queryset方法，处理queryset的结果
    # 查询所有信息
    queryset = Goods.objects.all()
    # 序列化queryset中的信息
    serializer_class = GoodsSerializer
    # 过滤
    filter_class = GoodsFilter

def market(request):
    return HttpResponseRedirect(reverse('shop:marketparam',args=('104749','0','0')))  # 大分类 详细分类 排序方式

def marketparam(request,typeid,cid,sortid):
    if request.method == "GET":
        # 获取所有大类
        goods_broad_types = FoodTypes.objects.all()

        # 获取商品
        if cid == '0':
            specific_broad_type_goods = Goods.objects.filter(categoryid=typeid)
        else:
            specific_broad_type_goods = Goods.objects.filter(categoryid=typeid,childcid=cid)

        # 获取所有细类
        childtypenames = FoodTypes.objects.filter(typeid=typeid).first().childtypenames
        first_divide_of_childtypenames = childtypenames.split('#')
        finish_divide = []
        for each in first_divide_of_childtypenames:
            second_divide_of_childtypenames = each.split(':')
            finish_divide.append(second_divide_of_childtypenames)

        # 按照指定排序规则重新排显示商品
        if sortid == '0': # 不排序，正常显示  （综合排序）
            pass
        elif sortid == '1': # 销量排序
            specific_broad_type_goods = specific_broad_type_goods.order_by('-productnum')
        elif sortid == '2': # 价格降序
            specific_broad_type_goods = specific_broad_type_goods.order_by('-price')

        elif sortid == '3': # 价格升序
            specific_broad_type_goods = specific_broad_type_goods.order_by('price')

        data = {
            'goods_broad_types':goods_broad_types,
            'specific_broad_type_goods':specific_broad_type_goods,
            'typeid':typeid,
            'cid':cid,
            'finish_divide':finish_divide, # 每个指定大类下属的所有小类
        }
        return render(request,"market/market.html",data)

def addgoods(request):
    if request.method == "POST":
        user = request.user
        data = {
            'msg': '请求成功',
            'code': '200',
        }
        if user and user.id:
            goods_id = request.POST.get("goods_id")
            price = Goods.objects.get(id=goods_id).price
            data["price"] = price
            # 去购物车数据表查看用户是否有购买该商品的订单
            specific_goods = CartModel.objects.filter(goods_id=goods_id).first()
            if specific_goods:
                specific_goods.c_num += 1
                data['c_num'] = specific_goods.c_num
                specific_goods.is_select = 1
                print(specific_goods.is_select,type(specific_goods.is_select))
                specific_goods.save()
            else:
                CartModel.objects.create(
                    user_id=user.id,
                    goods_id = goods_id,
                    c_num = 1
                )
                data['c_num'] = 1
        return JsonResponse(data)

def subgoods(request):
    if request.method == "POST":
        user = request.user
        goods_id = request.POST.get("goods_id")

        data = {
            'msg':'请求成功',
            'code':'200',
        }
        price = Goods.objects.get(id=goods_id).price
        data["price"] = price
        if user and user.id:
            # 查看购物车数据表中是否有用户减少的指定商品项
            specific_goods = CartModel.objects.filter(goods_id=goods_id).first()
            if specific_goods:
                # 存在，且商品的数量为1，则直接删除
                if specific_goods.c_num == 1:
                    specific_goods.delete()
                    data['c_num'] = 0
                else:
                # 存在，且商品的数量不为1，则减1
                    specific_goods.c_num -= 1
                    specific_goods.is_select = 1
                    specific_goods.save()
                    data['c_num'] = specific_goods.c_num
            return JsonResponse(data)

def cart(request):
    if request.method == "GET":
        user = request.user
        # 如果有用户登录，加载购物车数据
        if user and user.id:
            carts = CartModel.objects.filter(user_id=user.id)
            sum = 0
            for cart in carts:
                cart.is_select = 1 if cart.is_select == b'\x01' else 0
                if cart.is_select == 1:
                    price = Goods.objects.get(id=cart.goods_id).price
                    sum += (price * cart.c_num)
            data = {
                "carts": carts,
                "sum":round(sum,1),
            }
            return render(request,"cart/cart.html",data)
        else:
            # 没登陆，则返回登录页面
            return HttpResponseRedirect(reverse("shop:login"))

def changecartselect(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        # 处理全选
        flag = request.POST.get("flag")

        user = request.user
        data = {
            'msg':'请求成功',
            'code':'200',
        }
        if user and user.id:
            if flag != None:
                carts_list = []
                if flag == '1':
                    carts = CartModel.objects.all()
                    for cart in carts:
                        id_goodid = []
                        cart.is_select = 0
                        cart.save()
                        # 全选取消后的总价显示
                        total_price = 0
                        id_goodid.append(cart.id)  # 订单号
                        id_goodid.append(0)  # 是否被选中
                        id_goodid.append(total_price)
                        carts_list.append(id_goodid)
                else:
                    carts = CartModel.objects.all()
                    for cart in carts:
                        id_goodid = []
                        cart.is_select = 1
                        cart.save()
                        # 全选后的总价显示
                        c_num = cart.c_num
                        price = cart.goods.price
                        total_price = c_num * price

                        id_goodid.append(cart.id)
                        id_goodid.append(1)
                        id_goodid.append(total_price)
                        carts_list.append(id_goodid)
                data['carts'] = carts_list
                return JsonResponse(data)
            else:
                cart = CartModel.objects.filter(id=cart_id).first()
                c_num = cart.c_num
                price = cart.goods.price
                if cart.is_select == b'\x01':
                    cart.is_select = 0
                else:
                    cart.is_select = 1
                cart.save()
                data["c_num"] = c_num
                data["price"] = price
                data["is_select"] = cart.is_select
        return JsonResponse(data)

def generateorder(request):
    # 下单操作
    if request.method == "GET":
        user = request.user
        if user and user.id:
            # 获取购物车中is_select属性为1的商品
            goods = CartModel.objects.filter(is_select=True)

            # 创建订单（在axf_order表中添加数据）
            order = OrderModel.objects.create(
                user_id=user.id,
                o_status=0
            )

            # 创建订单详情（在axf_order_goods表中添加数据）
            for good in goods:
                OrderGoodsModel.objects.create(
                    goods = good.goods,
                    order = order,
                    goods_sum= good.c_num
                )
            goods.delete()
            # 订单创建完毕后进入支付页面
            # 元组只有一个元素，要加，号，否则会将数字拆来
            return HttpResponseRedirect(reverse("shop:payorder",args=(str(order.id),)))

def payorder(request,order_id):
    if request.method == "GET":
        # 根据订单号获取订单
        order = OrderModel.objects.filter(id=order_id).first()
        # 根据订单通过中介模型(ordergoodsmodel)获取其对应的所有商品(关系1:N)
        ordergoods = order.ordergoodsmodel_set.all()
        total_goods_to_order = []
        for ordergood in ordergoods:
            per_good_info = []
            good_img = ordergood.goods.productimg
            good_name = ordergood.goods.productlongname
            good_num = ordergood.goods_sum
            per_good_info.append(good_img)
            per_good_info.append(good_name)
            per_good_info.append(good_num)
            total_goods_to_order.append(per_good_info)
        data = {
            'order_id':order_id,
            'total_goods_to_order':total_goods_to_order,
        }
        return render(request,"order/order_info.html",data)

def orderpay(request,order_id):
    # 修改订单的付款状态 o_status=1,并返回mine页面
    if request.method == "GET":
        order = OrderModel.objects.filter(id=order_id).first()
        order.o_status = 1
        order.save()
        return HttpResponseRedirect(reverse("shop:mine"))

def orderwaitpay(request):
    if request.method == "GET":
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=0)
            total_orders_goods = {}
            for order in orders:
                ordergoods = order.ordergoodsmodel_set.all()
                one_order = []
                for ordergood in ordergoods:
                    one_goods = []
                    goods_img = ordergood.goods.productimg
                    goods_name = ordergood.goods.productlongname
                    goods_num = ordergood.goods_sum
                    one_goods.append(goods_img)
                    one_goods.append(goods_name)
                    one_goods.append(goods_num)
                    one_order.append(one_goods)
                total_orders_goods[order.id] = one_order

            data = {
                'total_orders_goods': total_orders_goods,
            }
            return render(request, "order/order_list_wait_pay.html", data)
        else:
            return HttpResponseRedirect("/shopapp/login/")


def orderwaitrecv(request):
    if request.method == "GET":
        user = request.user

        if user and user.id:
            orders = OrderModel.objects.filter(user=user).exclude(o_status=0)
            total_orders_goods = {}
            for order in orders:
                ordergoods = order.ordergoodsmodel_set.all()
                one_order = []
                for ordergood in ordergoods:
                    one_goods = []
                    goods_img = ordergood.goods.productimg
                    goods_name = ordergood.goods.productlongname
                    goods_num = ordergood.goods_sum
                    one_goods.append(goods_img)
                    one_goods.append(goods_name)
                    one_goods.append(goods_num)
                    one_order.append(one_goods)
                total_orders_goods[order.id] = one_order

            data = {
                'total_orders_goods': total_orders_goods,
            }
            return render(request, "order/order_list_payed.html", data)
        else:
            return HttpResponseRedirect("/shopapp/login/")

def deleterecord(request):
    if request.method == "POST":
        data = {
            'msg':'请求成功',
            'code': '200',
        }
        del_id = request.POST.get("del_id")
        if del_id:
            order = OrderModel.objects.get(id=del_id)
            ordergoods = order.ordergoodsmodel_set.all()
            for ordergood in ordergoods:
                ordergood.delete()
            order.delete()
        return JsonResponse(data)
