from __future__ import unicode_literals
# 主要用来处理业务逻辑
import uuid
from flask import render_template
from flask import Blueprint
from flask import send_file

bp = Blueprint('first',__name__)  # 初始化Blueprint -- 管理、规划url
# print("Blueprint...",__name__)  # __name__ == app.views 即当前所在的模块

@bp.route('/',methods=['GET','POST']) # 指定路由地址，默认(127.0.0.1:5000) methods:指定请求方式
def hi(): # 视图函数
    return 'hi,how are you?'

@bp.route('/hello/<name>') # name: str类型，可以接收各种类型的参数
def hello_man(name):
    print(name)  #  -- name
    print(type(name)) # -- 'str'
    return 'hello %s' % name

@bp.route('/helloint/<int:id>/') # 指定了参数类型，只能接收int类型的参数
def hello_int(id):
    print(id) # -- id
    print(type(id)) # -- 'int'
    a = "yusir"
    # 1/0
    return 'hello int: %s' %(id)

@bp.route('/index/')
def indexing():
    # 返回指定页面 如果不加../  则会找本级目录下的templates
    return send_file("../templates/hello.html")
    # return render_template("../templates/hello.html")

@bp.route('/getfloat/<float:price>/')
def hellofloat(price):
    return 'float: %s' % price

@bp.route('/getname/<string:name>/')
def helloname(name):
    return 'name: %s' % name

@bp.route('/getpath/<path:url_path>/')
# 紧挨着路由的视图函数将被调用，且其形参名必须
# 与url中的变量名保持一致
def hellopath(url_path):
    return 'path path path!! -- %s' % url_path
def test():
    return 'just a test!!'

@bp.route('/getuuid/')
def getuuid():
    a = uuid.uuid4()
    # print("uuid",type(a))
    return str(a)  # uuid类型的数据不能被直接打印，需要转换成string类型再打印

@bp.route('/getbyuuid/<uuid:uu>/')  # 如果不能输入正确格式的uuid数据，将会报错
def hellouuid(uu):
    return 'uu:%s' % uu