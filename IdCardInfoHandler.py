import re
import json
import string
from datetime import datetime


class IdCardInfoHandler:
    """
        身份证信息识别处理器
        说明：
            from IdCardInfoHandler import IdCardInfoHandler
            txt1 = "待处理的字符串"
            txt2 = "待处理的字符串"
            postprocessing = IdCardInfoHandler()
            postprocessing.idcard1(txt1) # 获取人像面处理结果
            postprocessing.idcard2(txt2) # 获取国徽处理结果
    """
    # 识别人像面
    def idcard1(self,data):
        # txt = "姓名张三性别男民族汉出生1992年09月26日住址湖北省黄石市下陆区公民身份号码42022219920926124X"
        
        # 去除数据中的所有空格 且将这些特殊字符转换为空字符 string.punctuation = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        txt = data.replace(" ", "").translate(str.maketrans("", "", string.punctuation))

        r = re.findall(r'^姓名(\S+)性别(\S)民族(\S+)出生(\S+)住址(\S+)公民身份号码(\w{18})$',txt)

        if(len(r) == 1):
            result = {}
            result['name'] = r[0][0]
            result['gender'] = r[0][1]
            result['nation'] = r[0][2]
            result['birth'] = r[0][3]
            result['addr'] = r[0][4]
            result['idcard'] = r[0][5]
            # return json.dumps( result, ensure_ascii = False )
            return result
        else:
            print("识别错误：", txt, r)
            return {}

    # 识别国徽面
    def idcard2(self,data):
            # txt = '中华人民共和国居民身份证签发机关黄石市公安局有效期限2022.05.21-长期'

            # 去除数据中的所有空格
            txt = data.replace(" ", "").translate(str.maketrans("", ""))

            r = re.findall(r'有效期限([0-9,.]+)-(\S+)',txt)

            if(len(r) == 1):
                result = {}

                # 注册时间
                result['regTime'] = str(datetime.strptime(r[0][0].translate(str.maketrans("", "",".")), r'%Y%m%d').date())
                # 过期时间
                result['expTime'] = str(datetime.strptime(r[0][1].translate(str.maketrans("", "",".")), r'%Y%m%d').date())

                # return json.dumps( result, ensure_ascii = False )
                return result
            else:
                print("识别错误：", txt, r)
                return {}
