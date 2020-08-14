<<<<<<< HEAD
import requests
import base64
import urllib.parse
import urllib.request
import os
import json
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
import numpy as np
from backend.models import *

access_token = '24.5bbcba88bded78fc95f89b51526d7b5a.2592000.1592619946.282335-19977604'
request_url = {
    "general": "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general",
    "animal": "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal",
    "plant": "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant",
    "dish": "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish",  # 菜品
    # 以下五个没有baike_info，暂时先别用
    "ingredient": "https://aip.baidubce.com/rest/2.0/image-classify/v1/classify/ingredient",  # 果蔬
    "logo": "https://aip.baidubce.com/rest/2.0/image-classify/v2/logo",
    "landmark": "https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark",
    "redwine": "https://aip.baidubce.com/rest/2.0/image-classify/v1/redwine",
    "currency": "https://aip.baidubce.com/rest/2.0/image-classify/v1/currency",
}
'''
currency:
{'log_id': 8013274640577737558, 'result': {'currencyName': '美元', 'hasdetail': 1, 'currencyCode': 'USD', 'year': '2006年', 'currencyDenomination': '100'}}
{'log_id': 841374876085343670, 'result': {'currencyName': '中国人民币', 'hasdetail': 1, 'currencyCode': 'CNY', 'year': '-', 'currencyDenomination': '100'}}
landmark:
{"log_id": 3450013152046070669, "result": {"landmark": "狮身人面像"}}
'''

dir = r'/home/CitizenScience/backend/backend'
# resnet = models.resnet50(pretrained=False)
# resnet.load_state_dict(torch.load(os.path.join(dir, 'resnet50-19c8e357.pth')))
# resnet.eval()
mobilenet = models.mobilenet_v2(pretrained=False)
mobilenet.load_state_dict(torch.load(
    os.path.join(dir, 'mobilenet_v2-b0353104.pth')))
mobilenet.eval()
with open(os.path.join(dir, 'index_to_name.json')) as f:
    index_to_en_name_strdict = json.load(f)
index_to_en_name = []
for key in index_to_en_name_strdict:
    index_to_en_name.append(index_to_en_name_strdict[key][1])

with open(os.path.join(dir, 'imagenet_classes_ch.txt'), encoding='UTF-8') as f:
    imagenet_classes_ch = [line.strip().split(' ')
                           for line in f.readlines()]
# print(imagenet_classes_ch)
index_to_ch_class = []
for one in imagenet_classes_ch:
    index_to_ch_class.append(one[3])
# print(index_to_ch_class)
print('torch准备完毕！')


def softmax(x):
    x_exp = np.exp(x)
    x_sum = np.sum(x_exp, axis=1, keepdims=True)
    s = x_exp / x_sum
    return s


def transform_image(infile):
    input_transforms = [transforms.Resize(255),
                        transforms.CenterCrop(224),
                        transforms.ToTensor(),
                        transforms.Normalize([0.485, 0.456, 0.406],
                                             [0.229, 0.224, 0.225])]
    my_transforms = transforms.Compose(input_transforms)
    timg = my_transforms(infile)
    timg.unsqueeze_(0)
    return timg


def rm_underline(astring):
    return astring.replace('_', ' ')


def predict(img_path, model):
    file = Image.open(img_path)
    if file is not None:
        input_tensor = transform_image(file)
        print('transform ok!')
        outputs = model.forward(input_tensor)
        print('forward ok!')
        _, indices = outputs.sort(descending=True)
        percentage = softmax(outputs.detach().numpy())[0]
        # print('softmax ok!')
        return [(rm_underline(index_to_en_name[idx]), index_to_ch_class[idx], percentage[idx].item()) for idx in indices[0][:10]]


'''
功能名称：志愿者上传图片的识别
input：project_id, data_title, 图片绝对路径, 选用api类别(可选，默认为general)
过程：调用api，满足以下两个条件则为合格：1)root在该输入框的root_pool中; 2)score>0.2
output：若图片不合格，则返回0；若图片合格，则返回score(必定大于0.2)  ---这个score可用来排序
'''


def volunteer_image_ai(project_id, data_title, img_path, api_type="general"):
    img_path = "/home/CitizenScience/file/image/dataimage/" + img_path
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img, "baike_num": 5}
    this_request_url = request_url["general"] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    while True:
        try:
            response = requests.post(
                this_request_url, data=params, headers=headers)
        except:
            print('百度api连接错误')
        if response:
            project = Project.query.filter_by(project_id=project_id).first()
            data_format = json.loads(project.data_format)
            torch_predict_first = predict(img_path, mobilenet)[0]
            torch_score = torch_predict_first[2]
            torch_root = torch_predict_first[1]
            print('torch识别完毕')
            # baidu api broken
            if 'error_code' in response.json() and 'error_msg' in response.json():
                if 'root_list' not in data_format[data_title]:
                    return -1, ''
                root_list = data_format[data_title]['root_list']
                if torch_root in root_list and float(torch_score) > 0.1:
                    return torch_root, ''
                else:
                    return -1, ''
            this_score = response.json()['result'][0]['score']
            this_root = response.json()['result'][0]['root']
            # 获取baike_info，用细分类型的api
            if api_type != "general":
                api_again = True
                info_request_url = request_url[api_type] + \
                    "?access_token=" + access_token
                while api_again:
                    try:
                        info_response = requests.post(
                            info_request_url, data=params, headers=headers)
                    except:
                        print('百度api连接错误')
                    if info_response:
                        api_again = False
            else:
                info_response = response
            # baike_info = json.dumps(info_response.json()[
            #                         'result'][0]['baike_info'])
            baike_info = info_response.json()['result'][0]['baike_info']
            print("百科："+str(baike_info))
            # baike_info['description'] = baike_info['description'].encode('utf-8').decode('unicode_escape')
            # for key in baike_info:
            #     print("key="+str(key))
            #     baike_info[key] = baike_info[key].encode('utf-8').decode('unicode_escape')
            if 'root_list' not in data_format[data_title]:
                return -1, baike_info
            root_list = data_format[data_title]['root_list']
            # 规则：1)api的this_root不在root_list或this_score<0.1; 2)torch的ch_class不在root_list
            # 若1) 2)同时成立，则认为不合法
            api_ok = this_root in root_list and float(this_score) > 0.2
            torch_ok = torch_root in root_list and float(torch_score) > 0.1
            if api_ok:
                return round(this_score, 2), baike_info
            if torch_ok:
                return round(torch_score, 2), baike_info
            return round(0.00, 2), ''


'''
功能名称：科学家上传示例图片
input：图片绝对路径, 选用api类别(可选，默认为general)
过程：调用api，获取root信息
output：score>0.4的root_list
'''


def scientist_image_ai(img_path, api_type="general"):
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    this_request_url = request_url["general"] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    root_list = []
    while True:
        try:
            response = requests.post(
                this_request_url, data=params, headers=headers)
        except:
            print('百度api连接错误')
        if response:
            torch_predict = predict(img_path, mobilenet)
            for result in torch_predict:
                torch_root = result[1]
                torch_score = result[2]
                if float(torch_score) > 0.1:
                    root_list.append(torch_root)
            root_list = list(set(root_list))
            # baidu api broken
            if 'error_code' in response.json() and 'error_msg' in response.json():
                return root_list
            for result in response.json()['result']:
                this_root = result['root']
                this_score = result['score']
                if float(this_score) > 0.2:
                    root_list.append(this_root)
            root_list = list(set(root_list))
            return root_list


if __name__ == "__main__":
    img_path = r"D:\_Study\SoftwareEngineering\小组作业\图片\人民币新100.jpg"
    api_type = "ingredient"

    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img, "baike_num": 5}
    this_request_url = request_url[api_type] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(this_request_url, data=params, headers=headers)
    if response:
        print(response.json())
        print(response.json()['result'][0]['baike_info'],
              response.json()['result'][0]['root'])
        # print(response.json()['result'][0]['score'], response.json()['result'][0]['name'])

    # f = open(img_path, 'rb')
    # img = base64.b64encode(f.read())
    # params = {"image": img, "baike_num": 5}
    # this_request_url = request_url[api_type] + "?access_token=" + access_token
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    # while True:
    #     response = requests.post(this_request_url, data=params, headers=headers)
    #     if response:
    #         print(response.json())
    #         this_score = response.json()['result'][0]['score']
    #         this_root = response.json()['result'][0]['root']
    #         root_pool = ['植物-树']
    #         if this_root not in root_pool:
    #             print(0)
    #         if this_score < 0.2:
    #             print(0)
    #         print(this_score)
    #     exit()
    #
=======
import requests
import base64
from backend.models import *

access_token = '24.5bbcba88bded78fc95f89b51526d7b5a.2592000.1592619946.282335-19977604'
request_url = {
    "general": "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general",
    "animal": "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal",
    "plant": "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant",
    "dish": "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish",  # 菜品
    # 以下五个没有baike_info，暂时先别用
    "ingredient": "https://aip.baidubce.com/rest/2.0/image-classify/v1/classify/ingredient",  # 果蔬
    "logo": "https://aip.baidubce.com/rest/2.0/image-classify/v2/logo",
    "landmark": "https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark",
    "redwine": "https://aip.baidubce.com/rest/2.0/image-classify/v1/redwine",
    "currency": "https://aip.baidubce.com/rest/2.0/image-classify/v1/currency",
}
'''
currency: 
{'log_id': 8013274640577737558, 'result': {'currencyName': '美元', 'hasdetail': 1, 'currencyCode': 'USD', 'year': '2006年', 'currencyDenomination': '100'}}
{'log_id': 841374876085343670, 'result': {'currencyName': '中国人民币', 'hasdetail': 1, 'currencyCode': 'CNY', 'year': '-', 'currencyDenomination': '100'}}
landmark:
{"log_id": 3450013152046070669, "result": {"landmark": "狮身人面像"}}
'''

'''
功能名称：志愿者上传图片的识别
input：project_id, data_title, 图片绝对路径, 选用api类别(可选，默认为general)
过程：调用api，满足以下两个条件则为合格：1)root在该输入框的root_pool中; 2)score>0.2
output：若图片不合格，则返回0；若图片合格，则返回score(必定大于0.2)  ---这个score可用来排序
'''
def volunteer_image_ai(project_id, data_title, img_path, api_type="general"):
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img, "baike_num": 5}
    this_request_url = request_url["general"] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    while True:
        response = requests.post(this_request_url, data=params, headers=headers)
        if response:
            this_score = response.json()['result'][0]['score']
            this_root = response.json()['result'][0]['root']
            project = Project.query.filter_by(project_id=project_id).first()
            data_format = json.loads(project.data_format)
            # data_entry = Data.query.filter_by(data_id=data_id).first()
            # data_title = data_entry.data_title
            root_pool = data_format[data_title]['root_pool']
            # 如果不在root_pool或score<0.2，则认为不合法
            if this_root not in root_pool:
                return 0
            if this_score < 0.2:
                return 0
            # 获取baike_info，用细分类型的api
            if api_type != "general":
                api_again = True
                info_request_url = request_url[api_type] + "?access_token=" + access_token
                while api_again:
                    info_response = requests.post(info_request_url, data=params, headers=headers)
                    if info_response:
                        api_again = False
            else:
                info_response = response
            baike_info = json.dumps(info_response['result'][0]['baike_info'])
            # data_entry.info = json.dumps(info_response['result'][0]['baike_info'])
            # db.commit()
            return this_score, baike_info


'''
功能名称：科学家上传示例图片
input：图片绝对路径, 选用api类别(可选，默认为general)
过程：调用api，获取root信息
output：score>0.4的root_list
'''
def scientist_image_ai(img_path, api_type="general"):
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    this_request_url = request_url["general"] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    root_list = []
    while True:
        response = requests.post(this_request_url, data=params, headers=headers)
        if response:
            # project = Project.query.filter_by(project_id=project_id).first()
            # data_format = json.loads(project.data_format)
            # data_format[data_name].setdefault('root_pool', [])
            # data_format[data_name].setdefault('examples', [])
            # 添加examples
            # data_format[data_name]['examples'].append(img_path.split('/')[-1])
            # 添加root_pool
            for result in response.json()['result']:
                this_root = result['root']
                # if this_root > 0.4 and this_root not in data_format[data_name]['root_pool']:
                #     data_format[data_name]['root_pool'].append(this_root)
                if this_root > 0.4:
                    root_list.append(this_root)
            # project.data_format = json.dumps(data_format)
            # db.commit()
            return root_list


if __name__ == "__main__":
    img_path = r"D:\_Study\SoftwareEngineering\小组作业\图片\人民币新100.jpg"
    api_type = "ingredient"

    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img, "baike_num": 5}
    this_request_url = request_url[api_type] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(this_request_url, data=params, headers=headers)
    if response:
        print(response.json())
        print(response.json()['result'][0]['baike_info'], response.json()['result'][0]['root'])
        # print(response.json()['result'][0]['score'], response.json()['result'][0]['name'])

    # f = open(img_path, 'rb')
    # img = base64.b64encode(f.read())
    # params = {"image": img, "baike_num": 5}
    # this_request_url = request_url[api_type] + "?access_token=" + access_token
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    # while True:
    #     response = requests.post(this_request_url, data=params, headers=headers)
    #     if response:
    #         print(response.json())
    #         this_score = response.json()['result'][0]['score']
    #         this_root = response.json()['result'][0]['root']
    #         root_pool = ['植物-树']
    #         if this_root not in root_pool:
    #             print(0)
    #         if this_score < 0.2:
    #             print(0)
    #         print(this_score)
    #     exit()
    #
>>>>>>> a58bb7cb0cf6db351fa2af4022c663cfd459e8fb
