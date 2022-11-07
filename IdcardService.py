from paddleocr import PaddleOCR, draw_ocr
from IdCardInfoHandler import IdCardInfoHandler
from PIL import Image
import logging,re,time
import requests,os
from io import BytesIO

# logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
# logging.disable(logging.WARNING)  # 关闭WARNING日志的打印

class IdCardService():
    """
        PaddleOCR(use_angle_cls=True, lang="ch")
        字段	说明	默认值
        use_gpu	是否使用GPU	TRUE
        gpu_mem	初始化占用的GPU内存大小	8000M
        image_dir	通过命令行调用时执行预测的图片或文件夹路径	
        det_algorithm	使用的检测算法类型	DB
        det_model_dir	检测模型所在文件夹。传参方式有两种，1. None: 自动下载内置模型到 ~/.paddleocr/det；2.自己转换好的inference模型路径，模型路径下必须包含model和params文件	None
        det_max_side_len	检测算法前向时图片长边的最大尺寸，当长边超出这个值时会将长边resize到这个大小，短边等比例缩放	960
        det_db_thresh	DB模型输出预测图的二值化阈值	0.3
        det_db_box_thresh	DB模型输出框的阈值，低于此值的预测框会被丢弃	0.5
        det_db_unclip_ratio	DB模型输出框扩大的比例	2
        det_east_score_thresh	EAST模型输出预测图的二值化阈值	0.8
        det_east_cover_thresh	EAST模型输出框的阈值，低于此值的预测框会被丢弃	0.1
        det_east_nms_thresh	EAST模型输出框NMS的阈值	0.2
        rec_algorithm	使用的识别算法类型	CRNN
        rec_model_dir	识别模型所在文件夹。传参方式有两种，1. None: 自动下载内置模型到 ~/.paddleocr/rec；2.自己转换好的inference模型路径，模型路径下必须包含model和params文件	None
        rec_image_shape	识别算法的输入图片尺寸	"3,32,320"
        rec_char_type	识别算法的字符类型，中英文(ch)、英文(en)、法语(french)、德语(german)、韩语(korean)、日语(japan)	ch
        rec_batch_num	进行识别时，同时前向的图片数	30
        max_text_length	识别算法能识别的最大文字长度	25
        rec_char_dict_path	识别模型字典路径，当rec_model_dir使用方式2传参时需要修改为自己的字典路径	./ppocr/utils/ppocr_keys_v1.txt
        use_space_char	是否识别空格	TRUE
        use_angle_cls	是否加载分类模型	FALSE
        cls_model_dir	分类模型所在文件夹。传参方式有两种，1. None: 自动下载内置模型到 ~/.paddleocr/cls；2.自己转换好的inference模型路径，模型路径下必须包含model和params文件	None
        cls_image_shape	分类算法的输入图片尺寸	"3, 48, 192"
        label_list	分类算法的标签列表	['0', '180']
        cls_batch_num	进行分类时，同时前向的图片数	30
        enable_mkldnn	是否启用mkldnn	FALSE
        use_zero_copy_run	是否通过zero_copy_run的方式进行前向	FALSE
        lang	模型语言类型,目前支持 中文(ch)和英文(en)	ch
        det	前向时使用启动检测	TRUE
        rec	前向时是否启动识别	TRUE
        cls	前向时是否启动分类, 此参数仅存在于代码使用模式	FALSE
    """
    def __init__(self):
        # 初始化ocr模型和后处理模型 只需要运行一次就可以下载并将模型加载到内存中
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    # 判断字符串包含
    def is_in(self, full_str, sub_str):
        r = re.findall(sub_str, full_str)
        if r:
            return True
        else:
            return False

    def idcard(self,img_path):

        # 定义文件路径
        # img_path = "/Users/jiaxiaoyu/Desktop/PaddleOCR/ouput/2.jpg"

        # 获取模型检测结果
        result = self.ocr.ocr(img_path, cls=True)

        # 将检测到的文字放到一个列表中
        # txts = [line[1][0] for line in result]
        txts = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                # 判断可信度
                # if line[1][1] >= 0.8:
                txts.append(line[1][0])
                # else: 
                #     raise Exception('可信度小于0.8',line[1])

        # 将文本列表合成一个字符串
        txt = ''.join(txts)
        # 处理字符串
        postprocessing = IdCardInfoHandler()
        # 将结果送入到后处理模型中
        id_result = {}
        if(self.is_in(txt,r'(姓|名|性|别|族|出|生|住|址)')):
            id_result = postprocessing.idcard1(txt)
        else:
            id_result = postprocessing.idcard2(txt)

        # 图片识别结果 保存到./result目录中
        result = result[0]
        image = object
        if "http" in img_path:
            response = requests.get(img_path)
            response = response.content
            BytesIOObj = BytesIO()
            BytesIOObj.write(response)
            image = Image.open(BytesIOObj)
        else:
            image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        if not os.path.exists('result'):
            os.mkdir('result')
        im_show.save('./result/' + str(int(time.time())) + '.jpg')

        return id_result

