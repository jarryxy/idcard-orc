from flask import Flask,request
from IdcardService import IdCardService

app = Flask(__name__)

idCardService = IdCardService()

@app.route('/ocr/idcard',methods=["POST"])
def idcard():
    r = {}
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



if __name__ == '__main__':
    # 指定port, 运行app
    app.run(debug=True, port='9000')