from xmlrpc.client import MININT
from flask import Flask,request,render_template,redirect,url_for,send_file
from mininet.net import Mininet
from subprocess import  call
import re
from flask_cors import CORS
from mininet.cli import CLI
from mininet.log import setLogLevel, info,error
from mininet.link import Intf
from mininet.topolib import TreeTopo
from mininet.util import quietRun
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from urllib import request as rettt
from urllib import parse 
import requests
import json

app = Flask(__name__)
CORS(app,supports_credentials = True)

# welcome page
@app.route('/')
def hello_world():
    return 'Hello World'

# print
@app.route('/print',methods = ['POST','GET'])
def print_nodes():
    node = request.get_json()["node"]
    # node = request.args.get("node",type=str)
    
    print("----------------------------")
    
    if node == None:
        print(net.nameToNode)
    else:
        print(f'key : {net.nameToNode[node]}')
        print(f'type : {type(net.nameToNode[node])}')
        
    print("----------------------------")
    net.start()
    return "print nodes"
    
# pingall
@app.route('/pingall',methods = ['POST','GET'])
def ping_all():

    print("----------------------------")
    
    net.pingAll()
        
    print("----------------------------")
    net.start()
    return "pingall"


# default graph
@app.route("/default",methods = ['POST','GET'])
def default_graph():
    c1 = net.addController(name="c1",controller=RemoteController)
    
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    h3 = net.addHost("h3")
    h4 = net.addHost("h4")
    
    s1 = net.addSwitch("s1",cls=OVSKernelSwitch)
    s2 = net.addSwitch("s2",cls=OVSKernelSwitch)
    
    
    net.addLink(h1,s1)
    net.addLink(h2,s1)
    net.addLink(h3,s2)
    net.addLink(h4,s2)
    net.addLink(s1,s2)
    
    h1.setIP("10.0.0.1",8)
    h2.setIP("10.0.0.2",8)
    h3.setIP("10.0.0.3",8)
    h4.setIP("10.0.0.4",8)
    
    net.build()

    
    net.get("s1").start([net.nameToNode["c1"]])
    net.get("s2").start([net.nameToNode["c1"]])
    
    net.start()
    net.waitConnected()
    
    print(net.nameToNode)###
    
    return "success"
    
    
# add host
@app.route("/host/add",methods = ['POST'])
def add_host():
    hostName = request.get_json()["hostName"]
    ip = request.get_json()["ip"]
    default = request.get_json()["defaultSwitch"]
    
    # args #
    # hostName = request.args.get("hostName",type=str)
    # ip = request.args.get("ip",type=str)
    # default = request.args.get("defaultSwitch",type=str)
    
    #todo
    host = net.addHost(hostName) 
    switch = net.nameToNode[default]
    
    net.addLink(host,switch)
    host.setIP(ip,8)
    
    
    net.start()  # 启动net
    net.pingAll()
    
    print(net.nameToNode)###

    # CLI(net)     # 等待键入命令
    # net.stop()   # 关闭net
    return "add host success"
    

# delete host
@app.route("/host/del",methods = ['POST'])
def del_host():
    hostName = request.get_json()["hostName"]
    # args #
    # hostName = request.args.get("hostName",type=str)
    net.delHost(net.nameToNode[hostName])
    net.start()  # 启动net
    net.pingAll()
    print(net.nameToNode)###

    return "del host success"

# add switch
@app.route("/switch/add",methods = ['POST'])
def add_switch():
    switchName = request.get_json()["switchName"]
    
    # args #
    # switchName = request.args.get("switchName",type=str)
    
    switch = net.addSwitch(switchName,cls=OVSKernelSwitch)
    
    net.get(switchName).start([net.nameToNode["c1"]])
    
    net.start()  # 启动net
    net.pingAll()
    print(net.nameToNode)###

    return "add switch success"

# delete switch
@app.route("/switch/del",methods = ['POST'])
def del_switch():
    switchName = request.get_json()["switchName"]
    
    # args #
    # switchName = request.args.get("switchName",type=str)
    
    net.delSwitch(net.nameToNode[switchName])
    
    net.start()  # 启动net
    net.pingAll()
    print(net.nameToNode)###
    #todo
    return "del switch success"

# add link
@app.route("/link/add",methods = ['POST'])
def add_link():
    nameA = request.get_json()["nameA"]
    nameB = request.get_json()["nameB"]
    ip = request.get_json()["ip"]
    
    # args #
    # nameA = request.args.get("nameA",type=str)
    # nameB = request.args.get("nameB",type=str)
    # ip = request.args.get("ip",type=str)
    
    net.addLink(net.nameToNode[nameA],net.nameToNode[nameB])
    if ip != None:
        net.nameToNode[nameA].setIP(ip,8)
    
    net.start()  # 启动net
    net.pingAll()
    print(net.nameToNode)###
    return "add link success"

# del link
@app.route("/link/del",methods = ['POST'])
def del_link():
    nameA = request.get_json()["nameA"]
    nameB = request.get_json()["nameB"]
    
    # args #
    # nameA = request.args.get("nameA",type=str)
    # nameB = request.args.get("nameB",type=str)
    
    net.delLinkBetween(net.nameToNode[nameA],net.nameToNode[nameB])
    
    net.start()  # 启动net
    net.pingAll()
    print(net.nameToNode)###
    return "del link success"


# input file
@app.route("/topo/file")
def input_file():
    filePath = request.args.get("filePath",type=str)
    #todo
    pass

# show topo
@app.route("/topo/view")
def show_route():
    net.build()
    #todo
    pass

# add flow
@app.route("/stream/add",methods = ['POST'])
def add_flow():

    json_str = request.get_json()['json']
    # print(type(dicts))
    json_data = json.loads(json_str)
    print(json_data)
    url = 'http://127.0.0.1:8080/stats/flowentry/add'
    print(url)
    # 如果正确添加，则返回200OK
    response = requests.post(url=url, json=json_data)
    if response.status_code == 200:
        print('Successfully Add!')
    else:
        print('Fail!')
    return ''

# delete flow
@app.route("/stream/del",methods = ['POST'])
def del_flow():
    switchName = request.get_json()['switchName']
    url = f'http://127.0.0.1:8080/stats/flowentry/clear/{switchName}'
    response = requests.delete(url=url)
    if response.status_code == 200:
        print('Successfully Clear!')
    else:
        print('Fail!')
    print(url)
    #todo
    return ''

# select flow
@app.route("/stream/select",methods = ['POST'])
def sel_flow():
    switchName = request.get_json()['switchName']
    url = f'http://127.0.0.1:8080/stats/flow/{switchName}'
    print(url)
    word = str(switchName)
    # params = parse.quote(word)
    full_url = url
    # 2.发请求保存到本地
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
    req = rettt.Request(url=full_url,headers=headers)
    res = rettt.urlopen(req)
    html = res.read().decode('utf-8')
    # 3.保存文件至当前目录
    filename = 'SDN/again/front-main/managerpages/static/'+ word + '.json'
    with open(filename,'w',encoding='utf-8') as f:
        f.write(html)

    
    #todo
    return word



if __name__ == '__main__':
    net = Mininet(build=False)
    app.run(port= 5001,debug=True)
