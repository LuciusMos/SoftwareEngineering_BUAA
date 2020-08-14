import pdb
from flask import Flask, request, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet, IMAGES, patch_request_class
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from sqlalchemy import or_
# from backend.models import *
import os

import sys
from PIL import Image

# app = Flask(__name__)
# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp, app.after_request(after_request)
# app.after_request(after_request)

# CORS(app, supports_credentials=True, resources={r'/*':{'origins': '*'}})
# app.config.from_object(Config)
# app.upload_set_config()

file_url = "/home/CitizenScience/file"
file_dir = "image"

real_file_url = os.path.join(file_url, file_dir)

from flask import Blueprint, request
from flask_uploads import UploadSet, IMAGES, ARCHIVES
from io import BytesIO
import datetime
import random


profile = UploadSet("profile", IMAGES)
photo = UploadSet("photo", IMAGES)
feedback = UploadSet("feedback", IMAGES)
proofphoto = UploadSet("proofphoto", IMAGES)
dataimage = UploadSet("dataimage", IMAGES)
datazip = UploadSet("datazip", ARCHIVES)



'''
filename 是不带文件后缀的名字
path 是文件完整路径（包括文件名）
'''
def compress_image(filename, path):
    new_filename = filename+"_cmprs.jpg"

    new_path = os.path.join(os.path.dirname(path), new_filename)
    print("new_path="+new_path)
    compress = "ffmpeg -i {} {}".format(path, new_path)
    try:
        isRun = os.system(compress)
        print("压缩完成")
    except e:
        print("图片压缩失败"+e)
        return False

    try:
        os.remove(path)
        print('原图已删除')
    except e:
        print("原图删除失败"+e)
        return False

    return new_filename

def upload_profile(user_id, img):

    file_rename = str(user_id) + "_" + str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
    file_rename_suffix = file_rename + '.jpg'

    img_fs = FileStorage(
        stream=BytesIO(img),
        filename=file_rename_suffix)

    filename = profile.save(img_fs, name=file_rename_suffix)

    # pdb.set_trace()

    file_url = profile.url(filename)
    basename = profile.get_basename(filename)
    path = profile.path(filename)

    new_filename = compress_image(file_rename, path)

    return new_filename



def upload_photo(user_id, img):

    file_rename = str(user_id) + "_" + str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
    file_rename_suffix = file_rename + '.jpg'

    img_fs = FileStorage(
        stream=BytesIO(img),
        filename=file_rename_suffix)


    # complt_url = os.path.join(real_file_url, "personal_photo", file_rename_suffix)
    # print(complt_url)
    # if os.path.exists(complt_url):
    #     os.remove(complt_url)
    #     print('old image has removed')

    filename = photo.save(img_fs, name=file_rename_suffix)

    # pdb.set_trace()

    file_url = photo.url(filename)
    basename = photo.get_basename(filename)
    path = photo.path(filename)

    new_filename = compress_image(file_rename, path)

    return new_filename



def upload_feedback_photo(user_id, img):

    file_rename = str(user_id) + str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
    file_rename_suffix = file_rename + '.jpg'

    img_fs = FileStorage(
        stream=BytesIO(img),
        filename=file_rename_suffix)


    # complt_url = os.path.join(real_file_url, "feedback", file_rename)
    # print(complt_url)
    # if os.path.exists(complt_url):
    #     os.remove(complt_url)
    #     print('old image has removed')

    filename = feedback.save(img_fs, name=file_rename_suffix)

    # pdb.set_trace()

    file_url = feedback.url(filename)
    basename = feedback.get_basename(filename)
    path = feedback.path(filename)

    new_filename = compress_image(file_rename, path)

    return new_filename


def upload_proof_photo(user_id, index, apply_time, img):


    file_rename = str(user_id) + "_" + apply_time + "_" + str(index)
    file_rename_suffix = file_rename + '.jpg'

    img_fs = FileStorage(
        stream=BytesIO(img),
        filename=file_rename_suffix)


    # complt_url = os.path.join(real_file_url, "proofphoto", file_rename)
    # print(complt_url)
    # if os.path.exists(complt_url):
    #     os.remove(complt_url)
    #     print('old image has removed')

    filename = proofphoto.save(img_fs, name=file_rename_suffix)

    # pdb.set_trace()

    file_url = proofphoto.url(filename)
    basename = proofphoto.get_basename(filename)
    path = proofphoto.path(filename)

    new_filename = compress_image(file_rename, path)

    return new_filename


def upload_data_image(user_id, project_id, submit_id, seq, img):

    # dataimage = UploadSet("dataimage", IMAGES)

    file_rename = str(user_id) + "_" + str(submit_id) + "_" + seq + "_" + str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
    file_rename_suffix = file_rename + '.jpg'

    img_fs = FileStorage(
        stream=BytesIO(img),
        filename=file_rename_suffix)


    # complt_url = os.path.join(real_file_url, "dataimage", file_rename)
    # print(complt_url)
    # if os.path.exists(complt_url):
    #     os.remove(complt_url)
    #     print('old image has removed')

    filename = dataimage.save(img_fs, name=file_rename_suffix)

    # pdb.set_trace()

    file_url = dataimage.url(filename)
    basename = dataimage.get_basename(filename)
    path = dataimage.path(filename)

    new_filename = compress_image(file_rename, path)

    return new_filename


# def upload_data_video(user_id, project_id, submit_id, seq, video):
#     pdb.set_trace()
#     file_share_name = str(user_id) + "_" + str(submit_id) + "_" + seq \
#         + "_" + str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))

#     zipFilePath = os.path.join(file_url, video_dir, "datavideo", file_share_name)

#     zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)

#     file_rename = file_share_name + ".MOV"

#     video_fs = FileStorage(
#         stream=BytesIO(video),
#         filename=file_rename)

#     # complt_url = os.path.join(real_file_url, "datazip", str(project_id), file_rename)
#     # print(complt_url)
#     # if os.path.exists(complt_url):
#     #     os.remove(complt_url)
#     #     print('old video has removed')

#     zipFile.write(video_fs)
#     filename = datazip.save(zipFile, name=file_share_name + ".zip")

#     # pdb.set_trace()

#     file_url = datazip.url(filename)
#     basename = datazip.get_basename(filename)
#     path = datazip.path(filename)

#     return basename
