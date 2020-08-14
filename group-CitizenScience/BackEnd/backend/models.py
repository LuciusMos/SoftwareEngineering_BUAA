from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import datetime
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_uploads import configure_uploads, UploadSet
from enum import IntEnum

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from flask import Flask, request, jsonify
import sqlite3
from flask import g
from flask_cors import CORS

import smtplib
from email.mime.text import MIMEText

import base64

from datetime import date  # 不知道用啥 全部导入就可以
import random

from PIL import Image
import pdb


file_url = "/home/CitizenScience/"
file_dir = "images"
real_file_url = file_url + file_dir + '/'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['UPLOADS_DEFAULT_DEST'] = file_url


class UserIdentity(IntEnum):
    VOLUNTEER = 1
    ASSISTANT = 2
    SCIENTIST = 3
    ADMINISTRATOR = 4
    INVALID = 5


class IdentifyVeirifyStatus(IntEnum):
    NO_NEED_TO_VERIFY = 0
    TO_BE_VERIFIED = 1
    TO_BE_REVISED = 2
    VERIFIED = 3


# UserProject = db.Table('UserProject', db.metadata,
#                        db.Column('user_id', db.Integer, db.ForeignKey('User.user_id'), primary_key=True),
#                        db.Column('project_id', db.Integer, db.ForeignKey('Project.project_id'), primary_key=True),
#                        db.Column('user_identity', db.Integer),  # UserIdentity
#                        db.Column('is_starred', db.Boolean, default=False),
#                        db.Column('is_participated', db.Integer, default=False),
#                        db.Column('is_liked', db.Boolean, default=False),
#                        db.Column('activities', db.Text))  # json


class UserProject(db.Model):
    __tablename__ = 'UserProject'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.user_id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'Project.project_id'), primary_key=True)
    user_identity = db.Column(db.Integer, nullable=False)  # UserIdentity
    is_starred = db.Column(db.Boolean, default=False)
    is_participated = db.Column(db.Boolean, default=False)
    is_liked = db.Column(db.Boolean, default=False)
    is_shared = db.Column(db.Boolean, default=False)
    activities = db.Column(db.Text)  # json
    user = db.relationship('User', back_populates='projects')
    project = db.relationship('Project', back_populates='participants')

    def __repr__(self):
        return '<用户#{} 参与项目#({})>'.format(self.user_id, self.project_id)


class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, unique=True, nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    user_identity = db.Column(db.Integer, nullable=False)  # UserIdentityEnum
    user_nickname = db.Column(db.String(50), nullable=False)
    # allow_global_notification = db.Column(db.Boolean, default=True, nullable=False)
    # allow_new_task_notification = db.Column(db.Boolean, default=True, nullable=False)
    # allow_new_feedback_notification = db.Column(db.Boolean, default=True, nullable=False)
    # allow_new_activity_notification = db.Column(db.Boolean, default=True, nullable=False)
    user_themecode = db.Column(db.String(50), nullable=False)
    profile_url = db.Column(db.String(200), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False)
    # projects = db.relationship('Project', secondary='UserProject', backref=db.backref('user'))
    projects = db.relationship('UserProject', back_populates='user')

    user_realname = db.Column(db.String(50), nullable=True)
    association = db.Column(db.String(50), nullable=True)
    photo_url = db.Column(db.String(200), nullable=True)
    academic_degree = db.Column(db.String(50), nullable=True)
    research_area = db.Column(db.String(50), nullable=True)

    job_title = db.Column(db.String(50), nullable=True)
    research_team = db.Column(db.String(50), nullable=True)
    resume_url = db.Column(db.String(200), nullable=True)
    personal_introduction = db.Column(db.Text, nullable=True)
    proof_file = db.Column(db.Text, nullable=True)  # json格式
    # ApplyCertificationResult
    verify_result = db.Column(db.Integer, nullable=True)
    revise_advice = db.Column(db.Text, nullable=True)
    apply_time = db.Column(db.DateTime, nullable=True)
<<<<<<< HEAD
    verification_code = db.Column(db.String(200), nullable=True)
=======
    verification_code = db.Column(db.String, nullable=True)
>>>>>>> a58bb7cb0cf6db351fa2af4022c663cfd459e8fb

    def __repr__(self):
        return '<用户#{}({}): {}>'.format(self.user_id, self.user_email, self.user_nickname)

    def password_hash(self, user_password_raw):
        return generate_password_hash(user_password_raw + self.user_email)

    def set_password(self, user_password_raw):
        self.user_password = self.password_hash(user_password_raw)

    def check_password(self, user_password_raw):
        return check_password_hash(self.user_password, user_password_raw + self.user_email)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id':self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None  # invalid token
        except:
            return None
        user = User.query.filter_by(user_id=data['user_id']).first()
        return user

    @staticmethod
    def get_id_name(token):
        cu = User.verify_auth_token(token)
        if cu is None:
            return None
        else:
            return {'id':cu.user_id,'name':cu.user_realname}



class ApplyingAssistant(db.Model):
    __tablename__ = 'ApplyingAssistant'
    assistant_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    scientist_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), primary_key=True)

class ProjectStatus(IntEnum):
    TO_BE_VERIFIED = 0
    VERIFIED = 1
    DATA_COLLECTING = 2
    ANALYSISING = 3
    CLOSED = 4
    FAILED = 5
    RE_SUBMIT = 6
    NOT_DIS = 7


class Project(db.Model):
    __tablename__ = 'Project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    project_title = db.Column(db.String(50), nullable=False)
    # sponsor_id = db.Column(db.String(50), db.ForeignKey('User.user_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    data_start_time = db.Column(db.DateTime, nullable=False)
    data_end_time = db.Column(db.DateTime, nullable=False)
    project_introduction = db.Column(db.Text, default='暂无简介')
    way_of_participation = db.Column(db.String(200), default='暂无参与方式')
    precautions = db.Column(db.Text, default='暂无注意事项')
    background_knowledge = db.Column(db.Text, default='暂无背景知识')
    data_format = db.Column(db.Text, nullable=False)  # json
    data_format_description = db.Column(db.Text, default='暂无数据描述')
    milestone = db.Column(db.Text)  # json
    category = db.Column(db.Text, default='无分类')
    branch = db.Column(db.Text, nullable=False) # 检索的学科

    is_public = db.Column(db.Boolean, default=True)
    project_status = db.Column(db.Integer, default=ProjectStatus.TO_BE_VERIFIED)
    project_main_image_url = db.Column(db.String(200), nullable=False)
    # participants = db.relationship('User', secondary='UserProject', backref=db.backref('project'))
    participants = db.relationship('UserProject', back_populates='project')
    submits = db.relationship('Submit', backref=db.backref('project'))
    content = db.Column(db.Text, nullable=True)
    previous_project_id = db.Column(db.Integer)

    def __repr__(self):
        return '<项目#{}({})>'.format(self.project_id, self.project_title)


class FeedbackType(IntEnum):
    FUNCTION = 0
    CONTENT = 1
    SECURITY = 2
    BREAKDOWN = 3
    OTHER = 4


class Feedback(db.Model):
    __tablename__ = 'Feedback'
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=True)
    feedback_type = db.Column(db.Integer, nullable=False)
    feedback_content = db.Column(db.Text, nullable=True)
    feedback_time = db.Column(db.DateTime, nullable=False)
    feedback_photo_urls = db.Column(db.Text, nullable=True)  # json格式


class Submit(db.Model):
    __tablename__ = 'Submit'
    submit_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    submit_time = db.Column(db.DateTime, nullable=False)
    ai_confidence = db.Column(db.Float, nullable=True) # json
    star_rating = db.Column(db.Integer, nullable=False, default=-1)
    estimation_content = db.Column(db.Text, nullable=True)
    estimation_time = db.Column(db.DateTime, nullable=True)
    estimation_user_id =  db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=True)
    datas = db.relationship('Data', backref=db.backref('submit'))


class DataType(IntEnum):
    FLOAT = 1
    INT = 2
    STRING = 3
    FRACTION = 4
    PICTURE = 5
    VIDEO = 6
    AUDIO = 7
    CATEGORY = 8
    MAP = 9

class Data(db.Model):
    __tablename__ = 'Data'
    data_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    submit_id = db.Column(db.Integer, db.ForeignKey('Submit.submit_id'), nullable=False)
    data_title = db.Column(db.String(200), nullable=False)
    data_type = db.Column(db.Integer, nullable=False)  # DataType
    float_value = db.Column(db.Float, nullable=True)
    int_value = db.Column(db.Integer, nullable=True)
    string_value = db.Column(db.Text, nullable=True)
    file_url = db.Column(db.String(200), nullable=True)
    cata_value = db.Column(db.String(200), nullable=True)
    map_value = db.Column(db.String(200), nullable=True)
    info = db.Column(db.Text, nullable=True)

class VisualType(IntEnum):
    COMPAREVISUAL = 1
    DATAVISUAL = 2
    SHOWVISUAL = 3

class Visualization(db.Model):
    __tablename__ = 'Visualization'
    display_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    is_display = db.Column(db.Boolean, nullable=False)
    figure_type = db.Column(db.String(200), nullable=False)  # map,bar,line,pie,scatter
    visual_type = db.Column(db.Integer, nullable=False)
    x_label = db.Column(db.String(200), nullable=True)
    y_label = db.Column(db.String(200), nullable=True)
    figure_title = db.Column(db.String(200), nullable=True)
    y_data_title = db.Column(db.String(200), nullable=True)
    x_data_title = db.Column(db.String(200), nullable=True)
    cata_data_title = db.Column(db.String(200), nullable=True)
    map_data_title = db.Column(db.String,nullable=True)
    y_rangeH = db.Column(db.String(200), nullable=True)  # 数字或dataMin或dataMax
    y_rangeL = db.Column(db.String(200), nullable=True)  # 数字或dataMin或dataMax
    x_rangeH = db.Column(db.String(200), nullable=True)  # 数字或dataMin或dataMax
    x_rangeL = db.Column(db.String(200), nullable=True)  # 数字或dataMin或dataMax
    create_time = db.Column(db.DateTime, nullable=False)
    figure_url = db.Column(db.String(200), nullable=True)


class NotificationType(IntEnum):
    ESTIMATED_DATA = 0
    TO_ESTIMATE_DATA = 1
    PROJECT_INVITATION = 2
    ASSISTANT_APPLICATION = 3
    SCIENTIST_APPLICATION = 4
    APPLICATION_PASSED = 5
    APPLICATION_FAILED = 6
    SET_AS_ASSISTANT = 7
    CUSTOM = 8

class Notification(db.Model):
    __tablename__ = 'Notification'
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    notification_type = db.Column(db.Integer, default=NotificationType.CUSTOM, nullable=False)
    notification_content = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=False)
    # project_id = db.Column(db.Integer, db.ForeignKey('Project.project_id'), nullable=True)
    has_read = db.Column(db.Boolean, default=False, nullable=False)
    notification_time = db.Column(db.DateTime, nullable=False)
    submit_id = db.Column(db.Integer, db.ForeignKey('Submit.submit_id'), nullable=True)


    def __repr__(self):
        return '<消息#{}({})>'.format(self.notification_id, self.notification_time)


def user_project():
    user1 = User(user_email='aa@', user_password='pwd', user_identity=UserIdentity.VOLUNTEER, user_nickname='nick')
    db.session.add(user1)
    usera = User.query.filter(User.user_id == 1).first()
    project1 = Project(project_title='p1', sponsor_id=usera.user_id)
    project2 = Project(project_title='p2', sponsor_id=usera.user_id)
    db.session.add(project1)
    db.session.add(project2)
    # usera.projects.append(project1)
    # usera.projects.append(project2)
    projecta = Project.query.filter(Project.project_id == 1).first()
    projectb = Project.query.filter(Project.project_id == 2).first()
    user_project1 = UserProject(user_id=usera.user_id, project_id=projecta.project_id,
                                user_identity=UserIdentity.VOLUNTEER, is_starred=True, activities='')
    user_project2 = UserProject(user_id=usera.user_id, project_id=projectb.project_id,
                                user_identity=UserIdentity.ASSISTANT, is_starred=True, activities='')
    db.session.add(user_project1)
    db.session.add(user_project2)
    # db.session.add(usera)
    db.session.commit()
    usera = User.query.filter(User.user_id == 1).first()
    print(usera)
    print(usera.projects)
    # print(usera.projects[0])
    for project in usera.projects:
        print(project.project)


def submit():
    project1 = Project(project_title='p1', sponsor_id=1)
    db.session.add(project1)
    submit1 = Submit(project=project1, uploader_id=1)
    # db.session.add(submit1)
    data1 = Data(submit=submit1, data_type=DataType.INT, int_value=100000)
    data2 = Data(submit=submit1, data_type=DataType.PICTURE, file_url='asfsd')
    project1 = Project.query.filter(Project.project_id == 1).first()
    print(project1)
    submit = Submit.query.filter(Submit.submit_id == 1).first()
    print(submit)
    for data in submit.datas:
        print(data)
    db.session.commit()


db.create_all()
print('db created!')
# user_project()

from backend.recommend_system import *
from backend.image_classification import *
from backend.upload import *
from backend.homepage import *
from backend.user import *
from backend.project import *
from backend.identity import *
from backend.init import *
from backend.upload import *
from backend.admin_project import *
from backend.admin_user import *
from backend.visualization import *
# from backend.app import db


