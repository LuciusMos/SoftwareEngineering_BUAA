import base64
import datetime
import json
import os
import random
from datetime import date  # 不知道用啥 全部导入就可以
from datetime import datetime
from enum import IntEnum

from flask import Flask, request, Blueprint, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import configure_uploads, UploadSet, IMAGES, patch_request_class
from sqlalchemy import or_, and_
from config import Config
from backend.admin_user import *
from backend.admin_project import *
from backend.models import *
import zipfile
from backend.image_classification import scientist_image_ai
<<<<<<< HEAD
from backend.upload import dataimage
import csv
import shutil
from backend.upload import compress_image
=======

>>>>>>> a58bb7cb0cf6db351fa2af4022c663cfd459e8fb

app = Flask(__name__)
'''
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app.after_request(after_request)
CORS(app, supports_credentials=True, resources={r'/*':{'origins': '*'}})
'''
app.config.from_object(Config)
file_url = "/home/CitizenScience/file/"
file_dir = "image"
real_file_url = file_url + file_dir+'/'
projectmainimage = UploadSet('projectmainimage', IMAGES)

admin = Blueprint("admin", __name__)
CORS(admin)
ROLEMAP = {
    "2": ["assistant"],
    "3": ["scientist"],
    "4": ["admin"],
}


@admin.route('/')
@admin.route('/admin/user_login', methods=['POST', 'GET'])
def admin_user_login():
    tj = json.loads(request.data.decode())
    user_email = tj['user_email']
    user_password = tj['password']
    user = User.query.filter_by(user_email=user_email).first()
    # if user_email == "admin":
    #     return str('admin-token')
    if user is None:
        return "该邮箱尚未注册"
    elif not user.check_password(user_password):
        return "密码错误"
    elif user.user_identity == 1:
        return "您无权访问管理端"
    else:
        return user.generate_auth_token()
        # return json.dumps({
        #         "roles": ROLEMAP[str(user.user_identity)],
        #         "introduction": "成功登录",
        #         "avatar": user.profile_url,
        #         "name": user.user_realname,
        #         "token": user.generate_auth_token()
        #     })


@admin.route('/admin/user_info', methods=['POST', 'GET'])
def user_info():
    if request.method == 'POST':
        res_token = json.loads(request.data.decode())['token']
        print(res_token)
        current_user = User.verify_auth_token(res_token)
        if current_user is not None:
            print(current_user)
            return json.dumps({
                "roles": ROLEMAP[str(current_user.user_identity)],
                "introduction": "成功登录",
                "avatar": current_user.profile_url,
                "name": current_user.user_realname
            })
        else:
            return "networkError"


@admin.route('/admin/user_logout', methods=['POST', 'GET'])
def user_logout():
    if request.method == 'POST':
        return 'success'


@admin.route('/admin/get_data/all_research', methods=['POST', 'GET'])
def gd_all_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        ups = UserProject.query.filter_by(user_identity=3).all()
        j = []
        for up in ups:
            print(up)
            print(up.user.user_id)
            print(up.user.user_realname)
            if up.project.project_status != ProjectStatus.NOT_DIS:
                up.project.project_status = get_current_project_status(
                    up.project)
                db.session.commit()
                j.append({"project_id": up.project_id,
                          "prev_id": up.project.previous_project_id,
                          "project_title": up.project.project_title,
                          "user_id": up.user_id,
                          "user_realname": up.user.user_realname,
                          "is_public": "公开" if up.project.is_public else "非公开",
                          "project_start_time": up.project.start_time.strftime('%Y-%m-%d'),
                          "status": PROJECTSTATUSMAP[str(up.project.project_status)]})
        j = sorted(j, key=lambda keys: keys['project_id'], reverse=True)
        return json.dumps(j)


@admin.route('/admin/get_data/my_research', methods=['POST', 'GET'])
def gd_my_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        ups = UserProject.query.filter_by(user_id=cu['id']).all()
        j = []
        for up in ups:
<<<<<<< HEAD
            print(up)
            if up.project.project_status == ProjectStatus.NOT_DIS:
                continue
=======
>>>>>>> a58bb7cb0cf6db351fa2af4022c663cfd459e8fb
            if up.user_identity == 4 or up.user_identity == 1:
                continue
            if up.user_identity == 3:
                uid = up.user_id
                urn = up.user.user_realname
            elif up.user_identity == 2:
                up2 = UserProject.query.filter_by(
                    project_id=up.project_id, user_identity=3).first()
                uid = up2.user_id
                urn = up2.user.user_realname
            up.project.project_status = get_current_project_status(up.project)
            db.session.commit()
            j.append({"project_id": up.project.project_id,
                      "project_title": up.project.project_title,
                      "user_id": uid,
                      "user_realname": urn,
                      "prev_id": up.project.previous_project_id,
                      "is_public": "公开" if up.project.is_public else "非公开",
                      "project_start_time": up.project.start_time.strftime('%Y-%m-%d'),
                      "status": PROJECTSTATUSMAP[str(up.project.project_status)]})
        j = sorted(j, key=lambda keys: keys['project_id'], reverse=True)
        return json.dumps(j)


@admin.route('/admin/get_data/review_research', methods=['POST', 'GET'])
def review_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        ups = UserProject.query.filter_by(user_identity=3).all()
        j = []
        for up in ups:
            if up.project.project_status == ProjectStatus.TO_BE_VERIFIED or\
                    up.project.project_status == ProjectStatus.RE_SUBMIT:
                j.append({"project_id": up.project_id,
                          "project_title": up.project.project_title,
                          "user_id": up.user_id,
                          "prev_id": up.project.previous_project_id,
                          "user_realname": up.user.user_realname,
                          "is_public": "公开" if up.project.is_public else "非公开",
                          "project_start_time": up.project.start_time.strftime('%Y-%m-%d'),
                          "status": PROJECTSTATUSMAP[str(up.project.project_status)]})
        j = sorted(j, key=lambda keys: keys['project_id'], reverse=True)
        return json.dumps(j)


@admin.route('/admin/upload/accept_research', methods=['POST', 'GET'])
def accept_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        rd = request.form.to_dict()
        p = Project.query.filter_by(project_id=rd['project_id']).first()
        if p.project_status == ProjectStatus.RE_SUBMIT:
            ups = UserProject.query.filter_by(
                project_id=p.previous_project_id,user_identity=UserIdentity.ASSISTANT).all()
            for up in ups:
                db.session.delete(up)
            db.session.commit()
            print(p.previous_project_id)
            p2 = Project.query.filter_by(
                project_id=p.previous_project_id).first()
            ups = UserProject.query.filter_by(
                project_id=p.project_id,user_identity=UserIdentity.ASSISTANT).all()
            for up in ups:
                up.project_id = p.previous_project_id
            db.session.commit()
            p2.project_title = p.project_title
            p2.start_time = p.start_time
            p2.data_start_time = p.data_start_time
            p2.data_end_time = p.data_end_time
            p2.end_time = p.end_time
            p2.project_introduction = p.project_introduction 
            p2.way_of_participation = p.way_of_participation
            p2.precautions = p.precautions 
            p2.background_knowledge = p.background_knowledge
            p2.is_public = p.is_public
            p2.project_main_image_url = p.project_main_image_url
            p2.category = p.category
            p2.branch = p.branch
            db.session.commit()
            p2.project_status = get_current_project_status(p2)
            p2.data_format = p.data_format
            p2.data_format_description = p.data_format_description
            db.session.commit()
            ups = UserProject.query.filter_by(
                project_id=p.project_id).all()
            for up in ups:
                db.session.delete(up)
            db.session.delete(p)
            db.session.commit()

        p.project_status = ProjectStatus.VERIFIED
        db.session.commit()
        n = Notification(
            user_id=rd['user_id'],
            notification_type=NotificationType.APPLICATION_PASSED,
            notification_content=cu['name'] + '通过了您的项目申请：' +
            p.project_title + '（ID:' + rd['project_id'] + ')',
            project_id=rd['project_id'],
            notification_time=datetime.datetime.now(),
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return 'success'


@admin.route('/admin/upload/refuse_research', methods=['POST', 'GET'])
def refuse_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        rd = request.form.to_dict()
        p = Project.query.filter_by(project_id=rd['project_id']).first()
        if p.project_status == ProjectStatus.RE_SUBMIT:
            prev_id = p.previous_project_id
            ups = UserProject.query.filter_by(
                project_id=rd['project_id']).all()
            for up in ups:
                db.session.delete(up)
            db.session.commit()
            db.session.delete(p)
            db.session.commit()
            p = Project.query.filter_by(project_id=prev_id).first()
            p.project_status = get_current_project_status(p)
            p.content = rd['content']
            db.session.commit()
        else:
            p.project_status = ProjectStatus.FAILED
            p.content = rd['content']
            db.session.commit()
        n = Notification(
            user_id=rd['user_id'],
            notification_type=NotificationType.APPLICATION_FAILED,
            notification_content=cu['name'] + '拒绝了您的项目申请：' +
            p.project_title + '（ID:' + rd['project_id'] + ')，拒绝理由为：'
            + rd['content'],
            project_id=rd['project_id'],
            notification_time=datetime.datetime.now(),
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return 'success'


def get_current_project_status(p):
    now = datetime.datetime.now()
    if p.project_status == ProjectStatus.TO_BE_VERIFIED or \
        p.project_status == ProjectStatus.FAILED or \
            p.project_status == ProjectStatus.RE_SUBMIT or \
                p.project_status == ProjectStatus.CLOSED:
        return p.project_status

    if now > p.start_time and now <= p.data_start_time:
        return ProjectStatus.VERIFIED
    elif now > p.data_start_time and now <= p.data_end_time:
        return ProjectStatus.DATA_COLLECTING
    elif now > p.data_end_time and now <= p.end_time:
        return ProjectStatus.ANALYSISING
    elif now > p.end_time:
        return ProjectStatus.CLOSED


@admin.route('/admin/upload/research_pic', methods=['POST', 'GET'])
def upload_pic():
<<<<<<< HEAD
    if request.method == 'POST':
        # cu = User.get_id_name(request.headers.get('token'))
        # if cu is None:
        #     return "networkError"
        file_rename = "project_pic_" + \
            str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
        projectmainimage.save(request.files['file'], name=file_rename + '.jpg')
        new_name = compress_image(file_rename, os.path.join(
            real_file_url, 'projectmainimage', file_rename+'.jpg'))
        return json.dumps({'pic_url': new_name})
=======
    global temp_file_name
    print(real_file_url)
    temp_file_name = str(currentUserId) + '_project_pic_' + str(global_file_index) + '.png'
    print(real_file_url + 'projectmainimage/' + temp_file_name)
    if os.path.exists(real_file_url + 'projectmainimage/' + temp_file_name):
        print('i\'m removed')
        os.remove(real_file_url+'projectmainimage/' + temp_file_name)
    projectmainimage.save(request.files['file'], name=temp_file_name)
    return "success"
>>>>>>> a58bb7cb0cf6db351fa2af4022c663cfd459e8fb


@admin.route('/admin/upload/img_example', methods=['POST', 'GET'])
def upload_img_example():
<<<<<<< HEAD
    # cu = User.get_id_name(request.headers.get('token'))
    # if cu is None:
    #     return "networkError"
    temp_file_name = "example_" + \
        str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
    temp_file_path = real_file_url + 'dataimage/' + temp_file_name + '.jpg'
    # if os.path.exists(temp_file_path):
    #     print('i\'m removed (upload_img_example)')
    #     os.remove(temp_file_path)
    dataimage.save(request.files['file'], name=temp_file_name + '.jpg')
    new_name = compress_image(temp_file_name, os.path.join(
        real_file_url, 'dataimage', temp_file_name+'.jpg'))
    root_list = scientist_image_ai(
        real_file_url + 'dataimage/' + new_name, "general")
    j = {'name': new_name, 'root_list': root_list}
    return json.dumps(j)
=======
    # global temp_file_name
    # temp_file_name = str(currentUserId) + '_data_example_pic_' + str(global_file_index) + '.png'
    temp_file_name = str(currentUserId) + "_" + "example" + "_" + str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S')) + '.jpg'
    temp_file_path = real_file_url + 'dataimage/' + temp_file_name
    if os.path.exists(temp_file_path):
        print('i\'m removed (upload_img_example)')
        os.remove(temp_file_path)
    projectmainimage.save(request.files['file'], name=temp_file_name)
    root_list = scientist_image_ai(temp_file_path, "general")
    j = {'name': temp_file_name, 'root_list': root_list}
    return json.dumps(j)


# @admin.route('/admin/get_data/research_pic', methods=['POST', 'GET'])
# def get_pic():
#     img_local_path = 'static/files/pic.png'
#     img_stream = ''
#     with open(img_local_path, 'r') as img_f:
#         img_stream = img_f.read()
#         img_stream = base64.b64encode(img_stream).decode()
#     return img_stream
>>>>>>> a58bb7cb0cf6db351fa2af4022c663cfd459e8fb


@admin.route('/admin/upload/delete_research', methods=['POST', 'GET'])
def delete_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        return "success"


@admin.route('/admin/get_data/show_detail', methods=['POST', 'GET'])
def get_detail():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        tid = request.form.to_dict()
        p = Project.query.filter_by(project_id=tid['detailId']).first()
        print(tid)
        rela = p.participants
        assis = []
        dfs = []
        i = 0
        for r in rela:
            if r.user_identity == UserIdentity.ASSISTANT:
                assis.append({'id': r.user_id, 'name': r.user.user_realname})
        dfs = []
        print(p.data_format)
        if p.data_format is None:
            dfs.append({'dkey': -1, 'key': '', 'value': ''})
        else:
            dfj = json.loads(p.data_format)
            for key in dfj:
                dfs.append({'dkey': i, 'key': key, 'value': dfj[key]})
                i = i + 1
        print(p.branch)
        j = {"project_title": p.project_title,
             "data_start_time": p.data_start_time.strftime('%Y-%m-%d'),
             "data_end_time": p.data_end_time.strftime('%Y-%m-%d'),
             "end_time": p.end_time.strftime('%Y-%m-%d'),
             "category": p.category,
             "project_introduction": p.project_introduction,
             "way_of_participation": p.way_of_participation,
             "background_knowledge": p.background_knowledge,
             "project_main_image_url": p.project_main_image_url,
             "is_public": "公开" if p.is_public else "非公开",
             "note": p.precautions,
             "branch": json.loads(p.branch) if p.branch is not None else '',
             "project_start_time": p.start_time.strftime('%Y-%m-%d'),
             "df_desc": p.data_format_description,
             "data_formats": dfs,
             "assistants": assis}
        return json.dumps(j)


@admin.route('/admin/upload/form', methods=['POST', 'GET'])
def upload_form():
    global real_file_url
    from backend.models import db
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        print(request.form.to_dict())
        f = request.form.to_dict()
        for a in json.loads(f['assistants']):
            u = User.query.filter_by(user_id=a['value']).first()
            if u is None:
                return 'notExist'
            else:
                if u.user_realname is None:
                    return 'noAuthen'
        pid = ""
        df = [{'key': '', 'value': ''}]
        if f['data_format'] is not None:
            df = json.loads(f['data_format'])

        # if f['pid'] != "":
        #     pid = f['pid']
        #     p = Project.query.filter_by(project_id=f['pid']).first()
        #     p.project_title = f['name']
        #     p.start_time = datetime.datetime.now()
        #     p.data_start_time = datetime.datetime.strptime(
        #         f['date1'], "%Y-%m-%d")
        #     p.data_end_time = datetime.datetime.strptime(
        #         f['date2'], "%Y-%m-%d")
        #     p.end_time = datetime.datetime.strptime(f['endDate'], "%Y-%m-%d")
        #     p.project_introduction = f['desc']
        #     p.way_of_participation = f['participate_way']
        #     p.precautions = f['note']
        #     p.background_knowledge = f['background']
        #     p.is_public = True if f['public'] == 'true' else False
        #     p.project_main_image_url = f['pic']
        #     p.category = f['type']
        #     p.branch = f['branch']
        #     p.project_status = 0
        #     p.data_format = json.dumps({x['key']: x['value'] for x in df})
        #     print(p.data_format)
        #     p.data_format_description = f['df_desc']
        #     db.session.commit()
        # else:
        project = Project(project_title=f['name'],
                          start_time=datetime.datetime.now(),
                          data_start_time=datetime.datetime.strptime(
            f['date1'], "%Y-%m-%d"),
            data_end_time=datetime.datetime.strptime(
            f['date2'], "%Y-%m-%d"),
            end_time=datetime.datetime.strptime(
            f['endDate'], "%Y-%m-%d"),
            project_introduction=f['desc'],
            way_of_participation=f['participate_way'],
            precautions=f['note'],
            background_knowledge=f['background'],
            is_public=True if f['public'] == 'true' else False,
            project_main_image_url=f['pic'],
            category=f['type'],
            branch=f['branch'],
            project_status=ProjectStatus.TO_BE_VERIFIED if f['pid'] == "" else ProjectStatus.RE_SUBMIT,
            data_format=json.dumps(
            {x['key']: x['value'] for x in df}, ensure_ascii=False),
            data_format_description=f['df_desc'],
            previous_project_id=None if f['pid'] == "" else f['pid']
        )
        print(project.data_format_description)
        print(project.branch)
        db.session.add(project)
        db.session.commit()
        pid = project.project_id
        if f['pid'] != "":
            p = Project.query.filter_by(project_id=f['pid']).first()
            p.project_status = ProjectStatus.NOT_DIS
        # project.project_main_image_url = str(pid) + '.png'
        db.session.commit()
        up = UserProject(user_id=cu['id'],
                         project_id=pid,
                         user_identity=UserIdentity.SCIENTIST,
                         is_participated=True)
        db.session.add(up)
        db.session.commit()

        for a in json.loads(f['assistants']):
            print(a)
            tup = UserProject.query.filter_by(
                user_id=int(a['value']), project_id=pid).first()
            if tup is not None:
                if tup.user_identity == UserIdentity.SCIENTIST:
                    continue
                elif tup.user_identity == UserIdentity.VOLUNTEER:
                    tup.user_identity = UserIdentity.ASSISTANT
            else:
                tup = UserProject(user_id=int(a['value']),
                                  project_id=int(pid),
                                  user_identity=UserIdentity.ASSISTANT,
                                  is_participated=True)
                db.session.add(tup)
                db.session.commit()
            n = Notification(
                user_id=int(a['value']),
                notification_type=NotificationType.SET_AS_ASSISTANT,
                notification_content=cu['name'] + '将您设置成为项目助理，项目名称为：'
                + tup.project.project_title + '(ID:' + str(pid) + ')',
                notification_time=datetime.datetime.now(),
                project_id=pid,
                has_read=False
            )
            db.session.add(n)
            db.session.commit()
        return "success"


@admin.route('/admin/get_data/user_search', methods=['POST', 'GET'])
def get_user_search():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        td = request.form.to_dict()
        if td['keyword'] == "":
            return json.dumps([])
        us = User.query.filter(or_(User.user_id.like('%' + td['keyword'] + '%'),
                                   User.user_email.contains(
            '%' + td['keyword'] + '%'),
            User.user_nickname.contains('%' + td['keyword'] + '%'))).all()
        j = []
        for u in us:
            judge = False \
                if UserProject.query.filter_by(user_id=u.user_id, project_id=td['project_id']).first() is None \
                else True
            j.append({'user_id': u.user_id,
                      'in_project': judge,
                      'user_nickname': u.user_nickname,
                      'user_email': u.user_email})
        return json.dumps(j)


@admin.route('/admin/get_data/assistant_search', methods=['POST', 'GET'])
def assistant_search():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        td = request.form.to_dict()
        if td['keyword'] == "":
            return json.dumps([])
        us = User.query.filter(or_(User.user_id.like('%' + td['keyword'] + '%'),
                                   User.user_realname.contains('%' + td['keyword'] + '%'))).all()
        j = []
        for u in us:
            if u.user_realname is not None:
                j.append({'value': u.user_realname +
                          '(ID:' + str(u.user_id) + ')'})
        print(j)
        return json.dumps(j)


@admin.route('/admin/upload/complete_research', methods=['POST', 'GET'])
def complete_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        td = request.form.to_dict()
        print(td)
        p = Project.query.filter_by(project_id=int(td['pid'])).first()
        p.project_status = ProjectStatus.CLOSED
        print(p.project_status)
        db.session.commit()
        return 'success'


@admin.route('/admin/get_data/all_volunteer', methods=['POST', 'GET'])
def all_volunteer():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        users = User.query.filter_by(user_identity=1).all()
        j = []
        for u in users:
            j.append({"user_id": u.user_id,
                      "user_nickname": u.user_nickname,
                      "user_email": u.user_email,
                      "register_time": u.register_time.strftime('%Y-%m-%d')})
        j = sorted(j, key=lambda keys: keys['user_id'], reverse=True)
        return json.dumps(j)
    return "error"


@admin.route('/admin/get_data/all_scientist', methods=['POST', 'GET'])
def all_scientist():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        users = User.query.filter_by(user_identity=3).all()
        j = []
        for u in users:
            j.append({"user_id": u.user_id,
                      "user_realname": u.user_realname,
                      "user_email": u.user_email,
                      "association": u.association,
                      "research_team": u.research_team,
                      "apply_time": u.apply_time.strftime('%Y-%m-%d'),
                      "register_time": u.register_time.strftime('%Y-%m-%d')})
        j = sorted(j, key=lambda keys: keys['user_id'], reverse=True)
        return json.dumps(j)
    return "error"


@admin.route('/admin/get_data/detail_scientist_assistant', methods=['POST', 'GET'])
def detail_scientist():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        print(request.form.to_dict())
        tid = request.form.to_dict()['id']
        u = User.query.filter_by(user_id=tid).first()
        j = {"user_realname": u.user_realname,
             "user_nickname": u.user_nickname,
             "user_id": u.user_id,
             "association": u.association,
             "research_team": u.research_team,
             "user_email": u.user_email,
             "apply_time": u.apply_time.strftime('%Y-%m-%d'),
             "register_time": u.register_time.strftime('%Y-%m-%d'),
             "user_email": u.user_email,
             "photo_url": u.photo_url,
             "resume_url": u.resume_url,
             "job_title": u.job_title,
             "academic_degree": u.academic_degree,
             "research_area": u.research_area,
             "personal_info": u.personal_introduction,
             "profile_url": u.profile_url,
             "proof_photo": u.proof_file
             }
        return json.dumps(j)
    return "error"

@admin.route('/admin/get_data/my_detail', methods=['POST', 'GET'])
def my_detail():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        tid = cu['id']
        u = User.query.filter_by(user_id=tid).first()
        j = {"user_realname": u.user_realname,
             "user_nickname": u.user_nickname,
             "user_id": u.user_id,
             "association": u.association,
             "research_team": u.research_team,
             "user_email": u.user_email,
             "apply_time": u.apply_time.strftime('%Y-%m-%d'),
             "register_time": u.register_time.strftime('%Y-%m-%d'),
             "user_email": u.user_email,
             "photo_url": u.photo_url,
             "resume_url": u.resume_url,
             "job_title": u.job_title,
             "academic_degree": u.academic_degree,
             "research_area": u.research_area,
             "personal_info": u.personal_introduction,
             "profile_url": u.profile_url,
             "proof_photo": u.proof_file
             }
        return json.dumps(j)
    return "error"



@admin.route('/admin/get_data/all_assistant', methods=['POST', 'GET'])
def all_assistant():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        users = User.query.filter_by(user_identity=2).all()
        j = []
        for u in users:
            j.append({"user_id": u.user_id,
                      "user_nickname": u.user_nickname,
                      "user_realname": u.user_realname,
                      "user_email": u.user_email,
                      "register_time": u.register_time.strftime('%Y-%m-%d')})
        j = sorted(j, key=lambda keys: keys['user_id'], reverse=True)
        return json.dumps(j)
    return "error"


@admin.route('/admin/get_data/apply_assistant', methods=['POST', 'GET'])
def admin_apply_assistant():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        us = ApplyingAssistant.query.filter_by(
            scientist_id=cu['id']).all()
        j = []
        for u in us:
            assis = User.query.filter_by(user_id=u.assistant_id).first()
            j.append({"user_id": u.assistant_id,
                      "user_realname": assis.user_realname,
                      "association": assis.association,
                      "project_id": u.project_id,
                      "project_title": Project.query.filter_by(project_id=u.project_id).first().project_title,
                      "apply_time": u.apply_time.strftime('%Y-%m-%d')})
        return json.dumps(j)


@admin.route('/admin/get_data/authen_scientist', methods=['POST', 'GET'])
def authen_scientist():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        us = User.query.filter_by(verify_result=1).all()
        j = []
        for u in us:
            j.append({"user_id": u.user_id,
                      "user_nickname": u.user_nickname,
                      "user_realname": u.user_realname,
                      "user_email": u.user_email,
                      "association": u.association,
                      "research_team": u.research_team,
                      "apply_time": u.apply_time.strftime('%Y-%m-%d')})
        return json.dumps(j)


@admin.route('/admin/upload_data/invite_user', methods=['POST', 'GET'])
def invite_user():
    if request.method == "POST":
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        rd = request.form.to_dict()
        print(request.form.to_dict())
        title = Project.query.filter_by(
            project_id=rd['project_id']).first().project_title
        n = Notification(
            user_id=rd['user_id'],
            notification_type=NotificationType.PROJECT_INVITATION,
            notification_content=cu['name'] + '邀请您加入项目：' +
            title + '（ID:' + rd['project_id'] + ')',
            project_id=rd['project_id'],
            notification_time=datetime.datetime.now(),
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return 'success'


@admin.route('/admin/upload/delete_user', methods=['POST', 'GET'])
def delete_user():
    if request.method == "POST":
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        uid = request.form.to_dict()['user_id']
        u = User.query.filter_by(user_id=uid).first()
        u.user_identity = UserIdentity.INVALID
        ups = UserProject.query.filter_by(user_id=uid).all()
        for up in ups:
            db.session.delete(up)
        db.session.commit()
        return 'success'


@admin.route('/admin/user_feedback', methods=['POST', 'GET'])
def admin_feedback():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        fb = Feedback(user_id='匿名' if request.form.to_dict()['ano'] is True else cu['id'],
                      feedback_content=request.form.to_dict()['content'],
                      feedback_type=request.form.to_dict()['type'],
                      feedback_time=datetime.datetime.now())
        db.session.add(fb)
        db.session.commit()
        return 'success'


@admin.route('/admin/upload_data/accept_scientist', methods=['POST', 'GET'])
def accept_scientist():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        id = request.form.to_dict()['id']
        u = User.query.filter_by(user_id=id).first()
        u.verify_result = IdentifyVeirifyStatus.VERIFIED
        u.user_identity = UserIdentity.SCIENTIST
        db.session.commit()
        n = Notification(
            user_id=id,
            notification_type=NotificationType.APPLICATION_PASSED,
            notification_content=cu['name'] + '通过了您的科学家认证申请',
            notification_time=datetime.datetime.now(),
            project_id=17373132,
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return 'success'


@admin.route('/admin/upload_data/refuse_scientist', methods=['POST', 'GET'])
def refuse_scientist():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        rd = request.form.to_dict()
        id = rd['id']
        u = User.query.filter_by(user_id=id).first()
        u.verify_result = IdentifyVeirifyStatus.TO_BE_REVISED
        db.session.commit()
        n = Notification(
            user_id=id,
            notification_type=NotificationType.APPLICATION_FAILED,
            notification_content=cu['name'] +
            '拒绝了您的科学家认证申请，拒绝理由为：' + rd['content'],
            notification_time=datetime.datetime.now(),
            project_id=17373132,
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return 'success'


@admin.route('/admin/upload_data/refuse_assistant', methods=['POST', 'GET'])
def refuse_assistant():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        rd = request.form.to_dict()
        id = rd['id']
        pid = rd['pid']
        content = rd['content']
        aa = ApplyingAssistant.query.filter_by(
            assistant_id=id, project_id=pid).first()
        ptitle = Project.query.filter_by(project_id=pid).first().project_title
        db.session.delete(aa)
        db.session.commit()
        n = Notification(
            user_id=id,
            notification_type=NotificationType.APPLICATION_FAILED,
            notification_content=cu['name'] + '拒绝了您的助理认证申请，项目名称为：'
            + ptitle + '(ID:' + pid + ')，拒绝理由为：'
            + content,
            notification_time=datetime.datetime.now(),
            project_id=pid,
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return 'success'


@admin.route('/admin/upload_data/accept_assistant', methods=['POST', 'GET'])
def accept_assistant():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        id = request.form.to_dict()['id']
        pid = request.form.to_dict()['pid']
        u = User.query.filter_by(user_id=id).first()
        u.user_identity = UserIdentity.ASSISTANT
        db.session.commit()
        up = UserProject(user_id=id,
                         project_id=pid,
                         user_identity=UserIdentity.ASSISTANT,
                         is_participated=True)
        db.session.add(up)
        db.session.commit()
        n = Notification(
            user_id=id,
            notification_type=NotificationType.APPLICATION_PASSED,
            notification_content=cu['name'] + '通过了您的助理认证申请，项目名称为：'
            + up.project.project_title + '(ID:' + pid + ')',
            notification_time=datetime.datetime.now(),
            project_id=pid,
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        aa = ApplyingAssistant.query.filter_by(
            assistant_id=id, project_id=pid).first()
        db.session.delete(aa)
        db.session.commit()
        return 'success'


@admin.route('/admin/get_data/data', methods=['POST', 'GET'])
def data():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        print(request.form.to_dict())
        pid = request.form.to_dict()['project_id']
        # ptitle = request.form.to_dict()['project_title']
        ptitle = Project.query.filter_by(project_id=pid).first().project_title
        j = []
        ss = Submit.query.filter_by(project_id=pid).all()
        for s in ss:
            ai = 0
            cnt = 0
            ds = Data.query.filter_by(submit_id=s.submit_id).all()
            cs = []
            for d in ds:
                t = -1
                c = ""
                if d.data_type == DataType.FLOAT:
                    c = d.float_value
                elif d.data_type == DataType.INT:
                    c = d.int_value
                elif d.data_type == DataType.STRING:
                    c = d.string_value
                elif d.data_type == DataType.CATEGORY:
                    c = d.cata_value
                elif d.data_type == DataType.MAP:
                    c = d.map_value
                else:
                    c = d.file_url
                    t = d.float_value
                    if t != -1:
                        cnt = cnt + 1
                        ai = ai + t
                cs.append({'data_id': d.data_id,
                           'data_type': d.data_type,
                           'data_name': d.data_title,
                           'content': c,
                           'ai': t
                           })
                print(cs)
            u = User.query.filter_by(user_id=s.estimation_user_id).first()
            j.append({
                'submit_id': s.submit_id,
                'avg_ai': None if cnt == 0 else round(ai/cnt, 4),
                'project_id': pid,
                'project_title': ptitle,
                'user_id': s.uploader_id,
                'user_nickname': User.query.filter_by(user_id=s.uploader_id).first().user_nickname,
                'submit_time': s.submit_time.strftime('%Y-%m-%d'),
                'datas': cs,
                'e_user_id': s.estimation_user_id,
                'e_user_name': None if u is None else u.user_realname,
                'star_rating': -1 if s.star_rating is None else s.star_rating
            })
        j = sorted(j, key=lambda keys: keys['submit_id'], reverse=True)
        return json.dumps(j)


@admin.route('/admin/upload_data/rate', methods=['GET', 'POST'])
def rate():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        r = request.form.to_dict()
        sid = r['submit_id']
        rate = r['rate']
        content = "无" if r['rateContent'] == "" else r['rateContent']
        s = Submit.query.filter_by(submit_id=sid).first()
        uid = s.uploader_id
        pid = s.project_id
        s.star_rating = rate
        s.estimation_content = content
        s.estimation_time = datetime.datetime.now()
        s.estimation_user_id = cu['id']
        db.session.commit()
        n = Notification.query.filter_by(submit_id=sid).first()
        if n is not None:
            db.session.delete(n)
            db.session.commit()
        n = Notification(
            user_id=uid,
            notification_type=NotificationType.ESTIMATED_DATA,
            notification_content='数据ID:' + str(sid) + '被' + cu['name'] +
            '标注为' + rate + '分，评价内容为：' + content,
            project_id=pid,
            notification_time=datetime.datetime.now(),
            submit_id=sid,
            has_read=False
        )
        db.session.add(n)
        db.session.commit()
        return "success"


@admin.route('/admin/zip', methods=['POST', 'GET'])
def zip():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        sid = request.form.to_dict()['submit_id']
        print(sid)
        txt_name = real_file_url + 'dataimage/' + \
            str(sid) + '_'+str(cu['id']) + '.txt'
        zip_name = file_url + 'zip/' + str(sid) + '.zip'
        if os.path.exists(zip_name) == False:
            ftxt = open(txt_name, 'w')
            zf = zipfile.ZipFile(zip_name, 'w')
            ds = Data.query.filter_by(submit_id=sid).all()
            for d in ds:
                if d.data_type == 1:
                    ftxt.write(d.data_title+'：'+str(d.float_value) + '\n')
                elif d.data_type == 2:
                    ftxt.write(d.data_title+'：'+str(d.int_value) + '\n')
                elif d.data_type == 3:
                    ftxt.write(d.data_title+'：'+str(d.string_value) + '\n')
                elif d.data_type == 5:
                    zf.write(real_file_url + 'dataimage/' +
                             d.file_url, arcname=d.data_title+'.jpg')
            ftxt.close()
            zf.write(txt_name, arcname='非图片数据.txt')
            os.remove(txt_name)
            zf.close()
        return send_file(zip_name, mimetype='zip', as_attachment=True)


@admin.route('/admin/proof_zip', methods=['POST', 'GET'])
def pf_zip():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        uid = request.form.to_dict()['id']
        pf = User.query.filter_by(user_id=uid).first().proof_file
        pf = json.loads(pf)
        zip_name = file_url + 'zip/' + str(uid) + '_pf.zip'
        if os.path.exists(zip_name) == False:
            zf = zipfile.ZipFile(zip_name, 'w')
            print(pf)
            for k in pf:
                print(k)
                zf.write(real_file_url + 'proofphoto/' +
                         pf[k], arcname=k+'_'+pf[k])
            zf.close()
        return send_file(zip_name, mimetype='zip', as_attachment=True)


@admin.route('/admin/get_my_project', methods=['GET', 'POST'])
def get_my_project():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        ups1 = UserProject.query.filter_by(
            user_id=cu['id'], user_identity=UserIdentity.SCIENTIST).all()
        ups2 = UserProject.query.filter_by(
            user_id=cu['id'], user_identity=UserIdentity.ASSISTANT).all()
        ups = ups1 + ups2
        j = []
        for up in ups:
            if up.project.project_status == ProjectStatus.DATA_COLLECTING or \
                up.project.project_status == ProjectStatus.ANALYSISING or \
                    up.project.project_status == ProjectStatus.RE_SUBMIT:
            # j.append(str(up.project_id) + '(' + up.project.project_title+')')
                j.append({'project_id': up.project_id,
                      'project_title': up.project.project_title})
        return json.dumps(j)


@admin.route('/admin/get_data/up_data', methods=['POST', 'GET'])
def up_data():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        print(request.form.to_dict())
        pid = request.form.to_dict()['project_id']
        # ptitle = request.form.to_dict()['project_title']
        j = []
        us = UserProject.query.filter_by(project_id=pid).all()
        for u in us:
            ru = u.user
            ss = Submit.query.filter_by(uploader_id=ru.user_id,project_id=pid).all()
            score = 0
            count = 0
            for s in ss:
                if s.star_rating != -1:
                    count = count + 1
                    score = score + s.star_rating
            j.append({
                "user_id": ru.user_id,
                "user_nickname": ru.user_nickname,
                "user_realname": ru.user_realname,
                "identity": u.user_identity,
                "join_time": ru.register_time.strftime('%Y-%m-%d'),
                "submit_amount": count,
                "star_rating": round(score / count, 2) if count > 0 else -1
            })
        j = sorted(j, key=lambda keys: keys['identity'], reverse=True)
        return json.dumps(j)


@admin.route('/admin/upload_data/inform', methods=['GET', 'POST'])
def inform():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        r = request.form.to_dict()
        uid = r['user_id']
        pid = r['project_id']
        content = "无" if r['informContent'] == "" else r['informContent']
        if uid != 'all':
            n = Notification(
                user_id=uid,
                notification_type=NotificationType.CUSTOM,
                notification_content=cu['name'] + '（用户ID:' + str(cu['id']) +
                '）向你发送了一条通知：' + content,
                notification_time=datetime.datetime.now(),
                project_id=pid,
                has_read=False
            )
            db.session.add(n)
            db.session.commit()
        else:
            ups = UserProject.query.filter_by(project_id=pid).all()
            for up in ups:
                n = Notification(
                    user_id=up.user_id,
                    notification_type=NotificationType.CUSTOM,
                    notification_content=cu['name'] + '（用户ID:' + str(cu['id']) +
                    '）群发了一条通知：' + content,
                    notification_time=datetime.datetime.now(),
                    project_id=pid,
                    has_read=False
                )
                db.session.add(n)
            db.session.commit()
        return "success"


@admin.route('/admin/get_data/index_chart_1', methods=['GET', 'POST'])
def index_chart_1():
    if request.method == 'POST':
        print(request.headers.get('token'))
        cu = User.get_id_name(request.headers.get('token'))
        print(cu)
        if cu is None:
            return "networkError"
        ups1 = UserProject.query.filter_by(
            user_id=cu['id'], user_identity=UserIdentity.SCIENTIST).all()
        ups2 = UserProject.query.filter_by(
            user_id=cu['id'], user_identity=UserIdentity.ASSISTANT).all()
        ups = ups1 + ups2
        all_projects_count = len(ups)

        all_users_count = 0
        all_submits_count = 0
        to_rate_count = 0
        all_verify_assistant = len(ApplyingAssistant.query.filter_by(
            scientist_id=cu['id']).all())
        for up in ups:
            pid = up.project_id
            tups = UserProject.query.filter_by(project_id=pid).all()
            all_users_count = all_users_count + len(tups)
            tss = Submit.query.filter_by(project_id=pid).all()
            all_submits_count = all_submits_count + len(tss)
            for ts in tss:
                if ts.star_rating == None or ts.star_rating == -1:
                    to_rate_count = to_rate_count + 1
        return json.dumps({
            "all_projects_count": all_projects_count,
            "all_users_count": all_users_count,
            "all_submits_count": all_submits_count,
            "to_rate_count": to_rate_count,
            "all_verify_assistant": all_verify_assistant
        })


@admin.route('/admin/get_data/index_chart_2', methods=['GET', 'POST'])
def index_chart_2():
    if request.method == 'POST':
        print(request.headers.get('token'))
        cu = User.get_id_name(request.headers.get('token'))
        print(cu)
        if cu is None:
            return "networkError"
        ups1 = UserProject.query.filter_by(
            user_id=cu['id'], user_identity=UserIdentity.SCIENTIST).all()
        ups2 = UserProject.query.filter_by(
            user_id=cu['id'], user_identity=UserIdentity.ASSISTANT).all()
        ups = ups1 + ups2
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        count6 = 0
        for up in ups:
            p = up.project
            if p.project_status == ProjectStatus.TO_BE_VERIFIED:
                count1 = count1 + 1
            elif p.project_status == ProjectStatus.VERIFIED:
                count2 = count2 + 1
            elif p.project_status == ProjectStatus.DATA_COLLECTING:
                count3 = count3 + 1
            elif p.project_status == ProjectStatus.ANALYSISING:
                count4 = count4 + 1
            elif p.project_status == ProjectStatus.CLOSED:
                count5 = count5 + 1
            elif p.project_status == ProjectStatus.FAILED:
                count6 = count6 + 1
            elif p.project_status == ProjectStatus.RE_SUBMIT:
                count1 = count1 + 1
        return json.dumps({
            "a1": count1,
            "a2": count2,
            "a3": count3,
            "a4": count4,
            "a5": count5,
            "a6":count6
        })


@admin.route('/admin/feedback_admin', methods=['GET', 'POST'])
def feedback_admin():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        j = []
        fs = Feedback.query.all()
        feedbackMap = {'0': '功能建议', '1': '内容举报',
                       '2': '安全隐私', '3': '应用故障', '4': '其他问题'}
        for f in fs:
            j.append({
                'feedback_id': f.feedback_id,
                'user_id': '匿名' if f.user_id is None else f.user_id,
                'feedback_type': feedbackMap[str(f.feedback_type)],
                'feedback_time': f.feedback_time.strftime('%Y-%m-%d'),
                'feedback_content': f.feedback_content
            })
        return json.dumps(j)


@admin.route('/admin/output_datas', methods=['GET', 'POST'])
def output_datas():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"

        str_time = str(datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S'))
        mkpath = file_url + 'zip/' + str(cu['id']) + '_dir_' + str_time
        os.makedirs(mkpath)
        csv_name = str(cu['id']) + str_time + '.csv'
        zf = zipfile.ZipFile(file_url + 'zip/' +
                             'datas_' + str_time + '.zip', 'w')

        checked_score = json.loads(request.form.to_dict()['checked_score'])
        pid = request.form.to_dict()['project_id']
        print(pid)
        print(checked_score)
        ss = Submit.query.filter(
            and_(Submit.project_id == pid, Submit.star_rating.in_(checked_score))).all()
        print(ss)
        headers = ['提交ID', '用户ID', '得分']
        p = Project.query.filter_by(project_id=pid).first()
        hs = json.loads(p.data_format)
        rows = []
        for h, h2 in hs.items():
            if h2['type'] < 4 or h2['type'] > 7:
                headers.append(h)
            else:
                os.makedirs(os.path.join(mkpath, h))
        for s in ss:
            ds = s.datas
            row = {'提交ID': s.submit_id,
                   '用户ID': s.uploader_id, '得分': s.star_rating}
            for d in ds:
                if d.data_type == 1:
                    row[d.data_title] = d.float_value
                elif d.data_type == 2:
                    row[d.data_title] = d.int_value
                elif d.data_type == 3:
                    row[d.data_title] = d.string_value
                elif d.data_type > 4 and d.data_type < 8:
                    shutil.copyfile(os.path.join(real_file_url, 'dataimage', d.file_url), os.path.join(
                        mkpath, d.data_title, str(s.submit_id)+'.jpg'))
                elif d.data_type == 8:
                    row[d.data_title] = d.cata_value
                elif d.data_type == 9:
                    row[d.data_title] = d.map_value
                print(row)
            rows.append(row)

        with open(file_url + 'zip/' + csv_name, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, headers)
            w.writeheader()
            w.writerows(rows)
        zf.write(file_url + 'zip/' + csv_name, arcname='非图片数据.csv')
        for path, dirnames, filenames in os.walk(mkpath):
            fpath = path.replace(mkpath, '')
            for filename in filenames:
                zf.write(os.path.join(path, filename),
                         os.path.join(fpath, filename))
        zf.close()
        os.remove(file_url + 'zip/' + csv_name)
        shutil.rmtree(mkpath)
        return send_file(file_url + 'zip/' + 'datas_' + str_time + '.zip', mimetype='zip', as_attachment=True)
