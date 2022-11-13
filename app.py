# 导入flask
from flask import Flask,request

# __name__代表当前app.py这个模块
# 1.帮助定位bug
# 2.需找模板文件，有个相对路径
app = Flask(__name__)

# 创建一个路由和视图函数的映射
@app.route('/')
def hello_world():
    return 'Hello World'

# 路径参数
@app.route("/user/<int:id>")
def getIdByPath(id):
    return f"获取到的id为{id}"

# get参数
@app.route("/list")
def getIdByParam():
    page = request.args.get("page",default=1,type=int)
    return f"获取到id{page}"

#
if __name__ == '__main__':
    app.run()
