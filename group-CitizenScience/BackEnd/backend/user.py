from backend.models import *

from flask import Blueprint, Flask, request, jsonify
import sqlite3
from flask import g
from flask_cors import CORS
import base64
# from models import User
import smtplib
from email.mime.text import MIMEText
from backend.project import *


'''
No.1-1
表名： User
功能名称：注册
input：用户登录名，密码
output：id, 昵称，身份，头像url
error：
1. 用户名已被注册
数据库改动：
1.添加一项
'''

user = Blueprint("user", __name__)

@user.route('/signup',methods=['GET','POST'])
def signup():
    user_email = request.args.get('user_email')
    user_password = request.args.get('user_password')
    register_time = datetime.datetime.now()

    # 检查邮箱是否已被注册
    user = User.query.filter_by(user_email=user_email).first()
    if user is not None:
        # 已被注册
        return "该邮箱已被注册"
    else:
        # 未被注册，数据库中添加一项
        user = User(user_email=user_email,
                    user_identity=UserIdentity.VOLUNTEER,
                    user_nickname=user_email,  # 初始化为user_email，之后去个人设置里改
                    register_time=register_time,
                    user_themecode='CommonwealGreen',
                    profile_url='travel.jpeg')
        user.set_password(user_password)
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(user_email=user_email).first()
        res = {}
        res['user_id']=user.user_id
        res['user_nickname']=user.user_nickname
        res['user_identity']=user.user_identity
        res['profile_url']=user.profile_url
        return res


'''
No.1-2
表名： User
功能名称：登录
input：用户登录名，密码
output：id, 昵称，身份，头像url
error：
1. 密码错误
2. 该邮箱尚未注册
数据库部分：
1.需要一个check_password函数
'''


@user.route('/login', methods=['GET', 'POST'])
def login():
    user_email = request.args.get('user_email')
    user_password = request.args.get('user_password')
    user = User.query.filter_by(user_email=user_email).first()
    if user is None:
        return "该邮箱尚未注册"
    elif not user.check_password(user_password):
       return "密码错误"
    else:
        res = {}
        res['user_id'] = user.user_id
        res['user_nickname'] = user.user_nickname
        res['user_identity'] = user.user_identity
        res['profile_url'] = user.profile_url
        res['user_themecode'] = user.user_themecode
        return res

@user.route('/last_login', methods=['GET', 'POST'])
def last_login():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        return "用户不存在"
    else:
        res = {}
        res['user_id'] = user.user_id
        res['user_nickname'] = user.user_nickname
        res['user_identity'] = user.user_identity
        res['profile_url'] = user.profile_url
        res['user_themecode'] = user.user_themecode
        return res

# @user.route('/login', methods=['GET', 'POST'])
# def user_project():
#     usera = User.query.filter(User.user_id == 1).first()
#     project1 = Project(project_title='p1', sponsor_id=usera.user_id)
#     user1 = User(user_email='aa@', user_password='pwd', user_identity=UserIdentity.VOLUNTEER, user_nickname='nick')
#     db.session.add(user1)
#     print(usera.user_id)
#     project2 = Project(project_title='p2', sponsor_id=usera.user_id)
#     usera.projects.append(project1)
#     usera.projects.append(project2)
#     db.session.add(project1)
#     db.session.add(project2)
#     db.session.add(usera)
#     db.session.commit()
#     usera = User.query.filter(User.user_id == 1).first()
#     print(usera)
#     for project in usera.projects:
#         print(project)


'''
No.1-3
表名： User
功能名称：消息推送查看
input：用户id
output：允许blablabla四个布尔值组成一个列表（为了少调用接口次数）
'''
# @user.route('/get_notification_setting', methods=['GET', 'POST'])
# def get_notification_setting():
# 	user_id = request.args.get('user_id')
# 	user = User.query.filter_by(user_id=user_id).first()
# 	notification_setting = [user.allow_global_notification,
# 							user.allow_new_task_notification,
# 							user.allow_new_feedback_notification,
# 							user.allow_new_activity_notification]
# 	# Note: 这里返回的是列表类型，flutter写的时候注意
# 	return notification_setting


'''
No.1-6
表名： User
功能名称：消息推送设置
input：用户id，用户本次设置的功能（功能名称即列名）
output：无
'''
# @user.route('/get_notification_setting', methods=['GET', 'POST'])
# def set_notification_setting():
# 	user_id = request.args.get('user_id')
# 	notification_setting_name = request.args.get('notification_setting_name')
# 	user = User.query.filter_by(user_id=user_id).first()
# 	# TODO: 把该用户的该功能置反是这样吗
# 	if notification_setting_name == 'allow_global_notification':
# 		user.allow_global_notification = !user.allow_global_notification
# 	elif notification_setting_name == 'allow_new_task_notification':
# 		user.allow_new_task_notification = !user.allow_new_task_notification
# 	elif notification_setting_name == 'allow_new_feedback_notification':
# 		user.allow_new_feedback_notification = !user.allow_new_feedback_notification
# 	elif notification_setting_name == 'allow_new_activity_notification':
# 		user.allow_new_activity_notification = !user.allow_new_activity_notification
# 	else:
# 		return "功能名称在flutter接口那边写错了！"
# 	database.session.commit()
# 	return notification_setting_name+"已成功设置"


'''
No.1-4
app.route:"/get_user_info"
表名： User
功能名称：获取头像url和身份
input：用户id
output：头像图片url, 身份
error：
'''
@user.route('/get_user_info', methods=['GET', 'POST'])
def get_user_info():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    userInfo = {}
    userInfo['profile_url'] = user.profile_url
    userInfo['user_identity'] = user.identity
    return userInfo



'''
No.1-7
表名： User
功能名称：忘记密码
input：用户email
output：无
error:1.用户尚未注册
数据库修改：密码重置
'''
@user.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    print("forget password")
    user_email = request.args.get('user_email')
    user = User.query.filter_by(user_email=user_email).first()
    if user is None:
        return "该邮箱尚未注册"
    else:
        # 该用户已注册过
        # 该用户已注册过
        rand_verification_code = str(random.randint(100000,999999))
        user.verification_code = rand_verification_code
        user.verification_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        db.session.commit()

        password = "ykzfihjpctmpbfgd"
        email_host = "smtp.qq.com"
        sender = "994732432@qq.com"
        receiver = [user_email]
        content = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>密码重置</title>
        </head>
        <body>

        <p>亲爱的「公众科学」用户""" + user.user_nickname + """，</p>
        <p>您好，</p>
        <p>这是一封重置密码的邮件，如果是您本人操作，请将以下验证码填写到APP验证码输入框中。 </p>
        <h2>""" + rand_verification_code + """</h2>

        <p>如果您并没有执行密码重置操作，您可以选择忽略此邮件。</p>
        <br><br>
        <p>致以最好的祝愿，</p>
        <p>「公众科学」开发组</p>
        </body>
        </html>
        """
        user = "CitizenScience" + "<" + sender + ">"
        message = MIMEText(content, _subtype='html',_charset='utf-8')
        message['Subject'] = "【公众科学】密码重置"
        message['From'] = user
        message['To'] = ";".join(receiver)
        server = smtplib.SMTP()
        server.connect(email_host, port=587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(user, receiver, message.as_string())
        server.close()
        print("邮件已发送")
        return rand_verification_code


'''
No.1-8
表名： User
功能名称：密码重置
input：用户id（从邮箱打开密码重置的链接带有用户id？
output：无
数据库操作：密码重置
'''
@user.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    user_email = request.args.get('user_email')
    user_password = request.args.get('user_password')
    user = User.query.filter_by(user_email=user_email).first()
    user.set_password(user_password)
    db.session.commit()
    return "密码修改成功"


'''
No.1-9
表名： User
功能名称：昵称重置
input：用户id
output：无
'''
@user.route('/edit_nickname', methods=['GET', 'POST'])
def edit_nickname():
    user_id = request.args.get('user_id')
    new_nickname = request.args.get('new_nickname')
    print(new_nickname)
    user = User.query.filter_by(user_id=user_id).first()
    user.user_nickname = new_nickname
    db.session.commit()
    print("昵称修改成功")
    return "昵称修改成功"

'''
No.1-10
表名： User
功能名称：用户头像重置
input：用户id
output：无
'''
@user.route('/set_profile', methods=['GET', 'POST'])
def set_profile():
    user_id = request.args.get('user_id')
    new_profile = request.data

    basename = upload_profile(user_id, new_profile)

    user = User.query.filter_by(user_id=user_id).first()
    user.profile_url = basename

    db.session.commit()
    print("头像更换成功")
    return basename

'''
No.1-11
表名： User
功能名称：用户主题色设置
input：用户id，主题色代码
output：无
'''
@user.route('/set_themecode', methods=['GET', 'POST'])
def set_themecode():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    user.user_themecode = request.args.get('themecode')

    db.session.commit()
    print("主题色更换成功")
    return "主题色更换成功"


'''
No.3-1
表名： Feedback
功能名称：意见反馈提交
input：用户id，类型，内容
output：无
数据库操作：增加一项
'''
@user.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    user_id = request.args.get('user_id')
    feedback_type = request.args.get('feedback_type')
    print("feedback_type=",feedback_type)
    feedback_content = request.args.get('feedback_content')
    feedback_time = datetime.datetime.now()

    photo_raw = request.data
    # photo_raws_basenames = {}
    # for _ in range(len(photo_raws)):
    #     photo_raw=photo_raws[_]
    basename = upload_feedback_photo("feedback_" + user_id, photo_raw)
    photo_raws_basenames = basename

    feedback = Feedback(user_id=user_id,
                        feedback_type=feedback_type,
                        feedback_content=feedback_content,
                        feedback_time=feedback_time,
                        feedback_photo_urls=json.dumps(photo_raws_basenames))

    db.session.add(feedback)
    db.session.commit()
    return "意见反馈提交成功"


'''
No.3-2
表名：Notification
功能名称：获取通知
input：用户id
output：通知id、通知类型列表、通知内容列表、项目id列表
数据库操作：
'''
@user.route('/get_notification', methods=['GET', 'POST'])
def get_notification():
    user_id = request.args.get('user_id')
    notifications = Notification.query.filter_by(user_id=user_id).all()
    note_info = {}
    note_info['notification_id'] = []
    note_info['notification_type'] = []
    note_info['notification_content'] = []
    note_info['project_id'] = []
    for note in notifications:
        note_info['notification_id'].append(node.notification_id)
        note_info['notification_type'].append(node.notification_type)
        note_info['notification_content'].append(node.notification_content)
        note_info['project_id'].append(node.project_id)
    return note_info


'''
No.3-3
表名：Notification
功能名称：删除通知
input：通知id
output：
数据库操作：删除一项
'''
@user.route('/delete_notification', methods=['GET', 'POST'])
def delete_notification():
    notification_id = request.args.get('notification_id')
    notification = Notification.query.filter_by(notification=notification).first()
    db.session.delete(notification)
    db.session.commit()
    return "消息删除成功"


'''
No.3-4
表名：Notification
功能名称：助理被设置为助理消息条数
input：用户id
output：条数
'''
@user.route('/set_as_assistant', methods=['GET', 'POST'])
def set_as_assistant():
    user_id = request.args.get('user_id')
    notification_count = Notification.query.filter_by(
                            user_id=user_id,
                            notification_type=4).count()
    return {"notification_count": notification_count}

'''
No.3-5
表名：Notification
功能名称：用户新收到评价条数、新邀请条数
input：用户id
output：条数
'''
@user.route('/user_notification_count', methods=['GET', 'POST'])
def user_notification_count():
    user_id = request.args.get('user_id')
    new_estimation_count = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=0,
                                has_read=False).count()
    new_invitation_count = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=2,
                                has_read=False).count()
    new_invitation_count2 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=7,
                                has_read=False).count()
    return {"new_estimation_count":new_estimation_count,
            "new_invitation_count":new_invitation_count+new_invitation_count2}


'''
No.3-6
表名：Notification
功能名称：科学家待审核助理申请数
input：用户id
output：条数
'''
@user.route('/application_from_assistant', methods=['GET', 'POST'])
def application_from_assistant():
    user_id = request.args.get('user_id')
    new_assistant_applicant = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=3,
                                has_read=False).count()
    return {"new_assistant_applicant":new_assistant_applicant}



'''
No.3-7
表名： Submit、Notification
功能名称：所有数据评价
input：user id
output：数据submit_id + 评价内容
error：尚无评价
'''
@user.route('/get_rating_and_content', methods=['GET', 'POST'])
def get_rating_and_content():
    user_id = request.args.get('user_id')
    notifications = Notification.query.filter_by(
                user_id=user_id,
                notification_type=0).all()
    if notifications is None:
        return "None"

    # print("排序前")
    # print(notifications)
    notifications.sort(key=lambda x:x.notification_time, reverse=True)
    notifications.sort(key=lambda x:x.has_read)
    # print("排序后")
    # print(notifications)

    res = {}
    res['submit_id'] = []
    res['project_title'] = []
    res['star_rating'] = []
    res['estimation_content'] = []
    res['estimation_time'] = []
    res['has_read'] = []
    res['project_main_image_url'] = []
    res['notification_id'] = []

    for notification in notifications:
        res['submit_id'].append(notification.submit_id)
        submit = Submit.query.filter_by(
                    submit_id=notification.submit_id,
                    ).first()
        if submit is None:
            continue
        # print("submit_id="+str(notification.submit_id))
        project = Project.query.filter_by(project_id=submit.project_id).first()
        if project is None:
            continue
        res['project_title'].append(project.project_title)
        res['star_rating'].append(submit.star_rating)
        res['estimation_content'].append(notification.notification_content)
        res['estimation_time'].append(str(submit.estimation_time))
        res['has_read'].append(notification.has_read)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['notification_id'].append(notification.notification_id)

    return res


'''
No.3-8
表名： Submit、Notification
功能名称：所有项目邀请
input：user id
output：数据submit_id + 评价内容
error：尚无评价
'''
@user.route('/get_project_invitation', methods=['GET', 'POST'])
def get_project_invitation():
    user_id = request.args.get('user_id')
    notifications = Notification.query.filter_by(
                user_id=user_id,
                notification_type=2).all()
    notifications2 = Notification.query.filter_by(
                user_id=user_id,
                notification_type=7).all()
    notifications = notifications+notifications2
    if notifications is None:
        print("无项目邀请")
        return "None"

    notifications.sort(key=lambda x:x.notification_time, reverse=True)

    res = {}
    res['project_id'] = []
    res['project_title'] = []
    res['content'] = []
    res['notification_time'] = []
    res['has_read'] = []
    res['project_main_image_url'] = []
    res['notification_id'] = []
    res['notification_type'] = []
    res['project_status'] = []


    for notification in notifications:
        res['project_id'].append(notification.project_id)
        print("project_id="+str(notification.project_id))
        project = Project.query.filter_by(project_id=notification.project_id).first()
        res['project_title'].append(project.project_title)
        res['content'].append(notification.notification_content)
        res['has_read'].append(notification.has_read)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['notification_time'].append(str(notification.notification_time))
        res['notification_id'].append(notification.notification_id)
        res['project_status'].append(project.project_status)
        res['notification_type'].append(notification.notification_type)


    return res



'''
No.3-8
表名： Notification
功能名称：设置已读
input：notification id
output：none
'''
@user.route('/set_has_read', methods=['GET', 'POST'])
def set_has_read():
    notification_id = request.args.get('notification_id')
    notification = Notification.query.filter_by(notification_id=notification_id).first()
    notification.has_read=True
    db.session.commit()
    return "已读设置成功"


'''
No.3-9
表名： Notificaton
功能名称：用户邀请用户
input：project_id, inviter_id, 被邀请者email
数据库：Notification加一项
error：不存在该email的用户
'''
@user.route('/user_invite_user', methods=['GET', 'POST'])
def user_invite_user():
    inviter_id = request.args.get('inviter_id')
    invited_email = request.args.get('invited_email')
    project_id = request.args.get('project_id')

    invited_user = User.query.filter_by(user_email=invited_email).first()
    inviter_user = User.query.filter_by(user_id=inviter_id).first()
    project = Project.query.filter_by(project_id=project_id).first()

    if invited_user is None:
        return "不存在该用户"

    notification_content = "用户"+inviter_user.user_nickname+" ("+inviter_user.user_email+") 邀请您加入项目「"+project.project_title+"」，快来看看吧~"

    notificaton = Notification(
                    user_id=invited_user.user_id,
                    notification_type=NotificationType.PROJECT_INVITATION,
                    project_id=project_id,
                    notification_time=datetime.datetime.now(),
                    notification_content=notification_content)

    db.session.add(notificaton)
    db.session.commit()

    userproject = UserProject.query.filter_by(user_id=inviter_id, project_id=project_id).first()
    if userproject is None:
        userproject = UserProject(user_id=inviter_id, project_id=project_id,is_shared=True)
        db.session.add(userproject)
    else:
        userproject.is_shared=True
    db.session.commit()

    return "成功邀请"

'''
No.3-10
表名：Notification
功能名称：消息56类的条数
input：用户id
output：条数
'''
@user.route('/application_result_notifaction_count', methods=['GET', 'POST'])
def application_result_notifaction_count():
    user_id = request.args.get('user_id')
    notification1 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=5,
                                has_read=False).count()
    notification2 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=6,
                                has_read=False).count()
    notification3 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=8,
                                has_read=False).count()
    return {"notification_number":notification1+notification2+notification3}

'''
No.3-10
表名：Notification
功能名称：消息56类
input：用户id
output：内容
'''
@user.route('/application_result_notifaction', methods=['GET', 'POST'])
def application_result_notifaction():
    user_id = request.args.get('user_id')
    notification1 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=5).all()
    notification2 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=6).all()
    notification3 = Notification.query.filter_by(
                                user_id=user_id,
                                notification_type=8).all()

    notifications = notification1+notification2+notification3

    if notifications is None:
        return "无重要消息"

    notifications.sort(key=lambda x:x.notification_time, reverse=True)

    res = {}
    res['notification_id'] = []
    res['notification_type'] = []
    res['notification_content'] = []
    res['notification_time'] = []
    res['has_read'] = []

    for notification in notifications:
        res['notification_id'].append(notification.notification_id)
        res['notification_type'].append(notification.notification_type)
        res['notification_content'].append(notification.notification_content)
        res['notification_time'].append(str(notification.notification_time.strftime('%Y-%m-%d')))
        res['has_read'].append(notification.has_read)

    return res








