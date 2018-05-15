from flask_script import Manager
from app import create_app
# 负责项目启动任务

app = create_app()

manager= Manager(app=app)

if __name__ == "__main__":
    # 启动应用
    # debug=True -- 启用debug模式
    # port:指定端口，默认5000
    # host:ip地址  0.0.0.0 --> 所有主机都可以访问
    # import sys
    # args = sys.argv
    # print(args)
    # app.run(debug=True, port=argv[2], host=argv[1]

    # app.run(debug=True,port='8000',host='0.0.0.0')
    manager.run()