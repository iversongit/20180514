from django.conf.urls import url
from shopper import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter() # 定义一个路由
router.register(r'goods',views.GoodsEdit)

urlpatterns = [
    url(r'^home/',views.home,name="home"),
    url(r'^login/',views.login,name="login"),
    url(r'^regist/',views.regist,name="regist"),
    url(r'^logout/',views.logout,name="logout"),
    url(r'^mine/',views.mine,name="mine"),
    url(r'^cart/',views.cart,name="cart"),
    # 闪购
    url(r'^market/$',views.market,name="market"), # 不加$将无法匹配到marketparam方法
    url(r'^market/(\d+)/(\d+)/(\d+)',views.marketparam,name="marketparam"),

    # 添加购物车商品
    url(r'^addgoods/',views.addgoods,name="addgoods"),
    # 减少购物车商品
    url(r'^subgoods/',views.subgoods,name="subgoods"),

    # 购物车
    url(r'^cart/',views.cart,name="cart"),
    # 修改购物车商品的选项
    url(r'^changecartselect/',views.changecartselect,name="changecartselect"),

    # 下单
    url(r'^generateorder/',views.generateorder,name='generateorder'),
    # 付款
    url(r'^payorder/(\d+)/',views.payorder,name='payorder'),
    # 确认付款
    url(r'^orderpay/(\d+)/',views.orderpay,name='orderpay'),

    # 待付款订单显示
    url(r'^orderwaitpay/',views.orderwaitpay,name='orderwaitpay'),

    # 待收获订单显示
    url(r'^orderwaitrecv/',views.orderwaitrecv,name='orderwaitrecv'),

    # 删除记录
    url(r'^deleterecord/',views.deleterecord,name='deleterecord')
]

urlpatterns += router.urls # 将路径与对应的类都添加到urlpatterns中