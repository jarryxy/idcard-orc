from flask import Flask,request
from IdcardService import IdCardService
import nacos,requests,time,threading

app = Flask(__name__)
#处理乱码
app.config['JSON_AS_ASCII']=False

idCardService = IdCardService()


# Nacos服务器地址
serviceAddress = "106.13.204.178:8849"
# Nacos注册服务名
serviceName = 'idcardOcrService'
# Nacos注册服务ip
serviceIp = '127.0.0.1'
# Nacos注册服务端口
servicePort = 9000


@app.route('/api/ocr/idcard',methods=["POST"])
def idcard():
    r = {}
    if not request.files.get('image_file') or  not request.json.get('image_url'):
        return {'code':500, 'message':'缺少参数image_file或image_url', 'data': {}}

    try:
        image = request.files.get('image_file')
        if image:
            path = './{}.jpg'.format('tmp')
            # 保存图片
            with open(path, 'wb+') as f:
                f.write(image.read())
                f.close()
            r = idCardService.idcard(path)
        else:
            imgUrl = request.json['image_url']
            r = idCardService.idcard(imgUrl)
    except Exception as e:
        print(e)
        return {'code':500, 'message':str(e), 'data': {}}

    return {'code':200, 'message':'success', 'data': r}


#nacos注册中心信息
'''
    将服务注册到注册中心 注册说明：将http://127.0.0.1:8085/**这个服务上的所有服务注册到注册中心，
    并且起名叫做algorithm-service 其他微服务进行访问时，访问http://algorithm-service/**即可，即其他服务，
    使用algorithm-service去注册中心，寻找真实的ip地址 例如原本访问 post访问：http://127.0.0.1:8085/simulation/analysis
    此时变成 http://algorithm-service/simulation/analysis
'''
#nacos服务
def service_register():
    url = "http://{}/nacos/v1/ns/instance?serviceName={}&ip={}&port={}".format(serviceAddress,serviceName,serviceIp,servicePort)
    print(url)
    res = requests.post(url)
    print("向nacos注册中心，发起服务注册请求，注册响应状态： {}".format(res.raw))

#服务检测
def service_beat():
    while True:
        url = "http://{}/nacos/v1/ns/instance/beat?serviceName={}&ip={}&port={}".format(serviceAddress,serviceName,serviceIp,servicePort)
        res = requests.put(url)
        print("已注册服务，执行心跳服务，续期服务响应状态： {}".format(res))
        time.sleep(5)

#发布http服务，并且注册到nocos
if __name__ == '__main__':
    service_register()
    #5秒以后，异步执行service_beat()方法
    threading.Timer(5,service_beat).start()
    # 指定port, 运行app
    app.run(debug=True, port=servicePort)