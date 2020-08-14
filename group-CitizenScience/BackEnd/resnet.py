# import torch
import  os
import json

import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests

import numpy as np



def softmax(x):
    x_exp = np.exp(x)
    x_sum = np.sum(x_exp, axis = 1, keepdims = True)
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

def get_prediction(input_tensor):
    outputs = resnet.forward(input_tensor)
    print('forward ok!')
    _, indices = outputs.sort(descending=True)
    percentage = softmax(outputs.detach().numpy())[0] * 100
    return [(classes[idx], percentage[idx].item()) for idx in indices[0][:10]]

def predict():
    file = img
    if file is not None:
        input_tensor = transform_image(file)
        return get_prediction(input_tensor)

resnet = models.resnet50(pretrained=True)
resnet.eval()

img_class_map = None
mapping_file_path = 'index_to_name.json'
if os.path.isfile(mapping_file_path):
    with open (mapping_file_path) as f:
        img_class_map = json.load(f)

with open('imagenet_classes.txt') as f:
  classes = [line.strip() for line in f.readlines()]

img = Image.open("dog.jpeg")

pred = predict()
print(pred)

import urllib.request
import urllib.parse
import json

'''
for res in pred:

    content = res[0]
    print(content)

    data = {
    'doctype': 'json',
    'type': 'EN2ZH_CN',
    'i':content
    }

    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    print(result['translateResult'][0][0]["tgt"])
'''



