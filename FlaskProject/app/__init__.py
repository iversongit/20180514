from flask import Flask
from app.views import bp

def create_app():
    # 初始化  __name__：主模块名或者包
    app = Flask(__name__)  # app: flask对象
    # print("init...",__name__) # __name__ == app 即包名
    app.register_blueprint(blueprint=bp)  # 绑定蓝图对象，操纵指定模块中的url
    return app