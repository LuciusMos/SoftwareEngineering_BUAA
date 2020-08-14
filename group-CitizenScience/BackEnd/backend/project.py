# from flask import Flask, request, jsonify
# import sqlite3
# from flask import g
# from flask_cors import CORS
from backend.models import *
from flask import Blueprint
# from datetime import date #不知道用啥 全部导入就可以


proj = Blueprint("project", __name__)

'''
No.2-7
表名：UserProject
功能名称：用户是否有权访问该项目，项目是否存在
input: 项目id，用户id
error: 1.项目id错误 2.项目不公开且该用户无权限
'''
@proj.route('/check_access_permission', methods=['GET', 'POST'])
def check_access_permission():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')

    # 如果项目id错误，则返回error
    project = Project.query.filter_by(project_id=project_id).first()
    if project is None:
        return "不存在该id的项目"

    # 如果用户没有权限访问项目，则返回error
    userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()
    if (not project.is_public) and (userproject is None):
        return "用户无权限访问该项目"


'''
No.2-1
表名： Project
功能名称：项目详情页
input：项目id
output：项目名称、发起时间、数据采集开始时间、数据采集结束时间、
        项目预计周期、项目简介、参与方式、注意事项、背景知识、数据格式说明、
        是否公开、项目主图url、项目类型
'''

@proj.route('/project_detail', methods=['GET', 'POST'])
def project_detail():
    project_id = request.args.get('project_id')

    project = Project.query.filter_by(project_id=project_id).first()
    project_detail = {"project_title": project.project_title,
                        "start_time": str(project.start_time),
                        "data_start_time": str(project.data_start_time),
                        "data_end_time": str(project.data_end_time),
                        "end_time": str(project.end_time),
                        "project_introduction":project.project_introduction, #
                        "way_of_participation":project.way_of_participation, #
                        "precautions":project.precautions,
                        "background_knowledge":project.background_knowledge,
                        "data_format_description":project.data_format_description,
                        "is_public":project.is_public,
                        "project_main_image_url":project.project_main_image_url,
                        "category":project.category} #

    return project_detail



'''
No.2-3
表名：ProjectMilestone
功能名称：获取项目进展
input：项目id
output：时间列表、进展详情列表
'''
@proj.route('/get_project_milestone', methods=['GET', 'POST'])
def get_project_milestone():
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(project_id=project_id).first()
    dt = []
    event = []
    if project.milestone is None:
        dt.append(str(datetime.datetime.now()))
        event.append("复审")
    else:
        milestone_json = project.milestone # json
        milestone = json.loads(milestone_json) # 转python dict
        milestone = sorted(milestone.items(),key=lambda item:item[0], reverse=False)
        print("milestone="+str(milestone))
        for item in milestone:
            dt.append(item[0])
            event.append(item[1])

    return {"datetime": dt, "event": event}


'''
No.2-4
表名： UserProject
功能名称：项目详情页参与者的姓名和头像列表
input：项目id
output：参与者的姓名和头像列表，参与人数，点赞人数
'''
@proj.route('/get_participant_list', methods=['GET', 'POST'])
def get_participant_list():
    project_id = request.args.get('project_id')
    all_participated = UserProject.query.filter_by(project_id=project_id,
                                            user_identity=UserIdentity.VOLUNTEER,
                                            is_participated=True
                                            ).all() # 所有参与者
    participated_count = len(all_participated) # 参与人数
    liked_count = UserProject.query.filter_by(project_id=project_id,
                                            user_identity=UserIdentity.VOLUNTEER,
                                            is_liked=True
                                            ).count() # 点赞人数

    res = {}
    res['participated_count'] = participated_count
    res['liked_count'] = liked_count
    res['participant_nickname'] = []
    res['participant_profile'] = []

    if participated_count == 0:
        return res

    for participant in all_participated:
        user = User.query.filter_by(user_id=participant.user_id).first()
        res['participant_nickname'].append(user.user_nickname)
        res['participant_profile'].append(user.profile_url)

    return res

'''
No.2-5
表名： Project
功能名称：项目详情页发起人id、姓名照片列表
input：项目id
output：发起人的id、姓名和照片列表
'''
@proj.route('/get_sponsor_list', methods=['GET', 'POST'])
def get_sponsor_list():
    project_id = request.args.get('project_id')
    all_scientist = UserProject.query.filter_by(project_id=project_id,
                                                user_identity=UserIdentity.SCIENTIST
                                                ).all() # 所有科学家

    sponsors = {}
    sponsors['user_id'] = []
    sponsors['realname'] = []
    sponsors['photo_url'] = []
    sponsors['job_title'] = []

    for scientist in all_scientist:
        user = User.query.filter_by(user_id=scientist.user_id).first()
        sponsors['user_id'].append(user.user_id) # id
        sponsors['realname'].append(user.user_realname) # 真名
        sponsors['photo_url'].append(user.photo_url) # 照片
        sponsors['job_title'].append(user.job_title) # 职称
    # print(sponsors)
    return sponsors


'''
No.2-6
表名： Project
功能名称：项目详情页助理id姓名头像列表
input：项目id
output：助理的id姓名和头像列表
'''
@proj.route('/get_assistant_list', methods=['GET', 'POST'])
def get_assistant_list():
    project_id = request.args.get('project_id')
    all_assistant = UserProject.query.filter_by(project_id=project_id,
                                                user_identity=UserIdentity.ASSISTANT
                                                ).all() # 所有助理
    assistents = {}
    assistents['user_id'] = []
    assistents['realname'] = []
    assistents['photo_url'] = []
    assistents['job_title'] = []

    for assistent in all_assistant:
        user = User.query.filter_by(user_id=assistent.user_id).first()
        assistents['user_id'].append(user.user_id) # id
        assistents['realname'].append(user.user_realname) # 真名
        assistents['photo_url'].append(user.photo_url) # 照片
        assistents['job_title'].append(user.job_title) # 照片

    return assistents


'''
No.2-8
表名：Project
功能名称：获取数据表单
input: 项目id
output: 数据格式（要求）字典
'''
@proj.route('/get_data_form', methods=['GET', 'POST'])
def get_data_form():
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(project_id=project_id).first()
    data_format_json = project.data_format # json
    print(type(data_format_json))
    data_format = json.loads(data_format_json) # 转换成python dict

    res = {}
    res['show_hint'] = []
    res['type'] = []
    res['min'] = []
    res['max'] = []
    res['cate'] = []
    res['nullable'] = []
    res['examples'] = []

    for key in data_format.keys():
        res['show_hint'].append(key)
        print(data_format[key])
        value = data_format[key]
        res['type'].append(value['type'])
        try:
            res['min'].append(value['min'])
        except:
            res['min'].append('')
        try:
            res['max'].append(value['max'])
        except:
            res['max'].append('')
        try:
            res['cate'].append(value['cate'])
        except:
            res['cate'].append('')
        try:
            res['nullable'].append(value['nullable'])
        except:
            res['nullable'].append('false')
        try:
            res['examples'].append(value['examples'])
        except:
            res['examples'].append('')

    return res



'''
No.2-9
表名：Project
功能名称：获取项目搜索结果
input: 项目id或名称关键字
output: 项目id，题目，发起人姓名、职称，发起人工作单位，
        研究团队，主图url，项目起止时间，分类，状态，项目简要
error: 无搜索结果
'''
@proj.route('/search_project_by_keyword', methods=['GET', 'POST'])
def search_project_by_keyword():
    keyword = request.args.get('keyword')
    user_id = request.args.get('user_id')
    ack = int(request.args.get('ack'))
    print("ack="+str(ack))
    print("keyword="+str(keyword))

    if keyword=='新发布':
        return get_more_latest_projects()
    elif keyword=='为我推荐':
        return get_recommended_projects_2(user_id, ack)
    elif keyword=='最热门':
        print("进入最热门函数get_hotest_project_2()")
        return get_hotest_project_2(ack)

    projects1 = Project.query.filter(
            Project.project_title.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.VERIFIED
            ).all()
    projects2 = Project.query.filter(
            Project.project_title.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.DATA_COLLECTING
            ).all()
    projects3 = Project.query.filter(
            Project.project_title.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.CLOSED
            ).all()
    projects4 = Project.query.filter(
            Project.project_title.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.NOT_DIS
            ).all()
    projects5 = Project.query.filter(
            Project.project_title.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.ANALYSISING
            ).all()

    projects_by_category1 = Project.query.filter(
            Project.category.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.VERIFIED
            ).all()
    projects_by_category2 = Project.query.filter(
            Project.category.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.DATA_COLLECTING
            ).all()
    projects_by_category3 = Project.query.filter(
            Project.category.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.CLOSED
            ).all()
    projects_by_category4 = Project.query.filter(
            Project.category.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.NOT_DIS
            ).all()
    projects_by_category5 = Project.query.filter(
            Project.category.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.ANALYSISING
            ).all()

    projects_by_branch1 = Project.query.filter(
            Project.branch.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.VERIFIED
            ).all()
    projects_by_branch2 = Project.query.filter(
            Project.branch.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.DATA_COLLECTING
            ).all()
    projects_by_branch3 = Project.query.filter(
            Project.branch.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.CLOSED
            ).all()
    projects_by_branch4 = Project.query.filter(
            Project.branch.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.NOT_DIS
            ).all()
    projects_by_branch5 = Project.query.filter(
            Project.branch.like('%'+keyword+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.ANALYSISING
            ).all()

    projects = projects1 + projects2 + projects3 + projects4 + projects5 + \
            projects_by_category1 + projects_by_category2 + projects_by_category3 + \
            projects_by_category4 + projects_by_category5 + projects_by_branch1 + \
            projects_by_branch2 + projects_by_branch3 + projects_by_branch4 + projects_by_branch5

    if projects is None:
        return "无搜索结果"

    res = {}
    res['project_id'] = []
    res['project_title'] = []
    res['sponsor_real_name'] = []
    res['sponsor_job_title'] = []
    res['sponsor_association'] = []
    res['sponsor_research_team'] = []
    res['project_main_image_url'] = []
    res['start_time'] = []
    res['end_time'] = []
    res['category'] = []
    res['project_status'] = []
    res['project_introduction'] = []

    count = 0
    print(ack)
    for project in projects:
        count += 1
        if project.project_id in res['project_id']:
            continue
        if count <= ack:
            continue
        if count > ack+10:
            break
        print("搜索到的project_id="+str(project.project_id))
        res['project_id'].append(project.project_id)
        res['project_title'].append(project.project_title)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['start_time'].append(str(project.start_time))
        # print("时间="+str(project.start_time))
        res['end_time'].append(str(project.end_time))
        res['category'].append(project.category)
        res['project_status'].append(project.project_status)
        res['project_introduction'].append(project.project_introduction)
        # 选一位发起人
        sponsor_userproject = UserProject.query.filter_by(
                                project_id=project.project_id,
                                user_identity=UserIdentity.SCIENTIST
                                ).first()
        sponsor = User.query.filter_by(user_id=sponsor_userproject.user_id).first()
        res['sponsor_real_name'].append(sponsor.user_realname)
        res['sponsor_job_title'].append(sponsor.job_title)
        res['sponsor_association'].append(sponsor.association)
        res['sponsor_research_team'].append(sponsor.research_team)

    return res


'''
No.2-10
表名：UserProject & Project
功能名称：根据科学家id找到他的所有项目
input: 科学家id
output：他的所有项目的 id，题目，发起人姓名、职称，发起人工作单位，
        研究团队，主图url，项目起止时间，分类，状态，项目简要
error：无项目
'''
@proj.route('/get_all_project_by_sponsor_id', methods=['GET', 'POST'])
def get_all_project_by_sponsor_id():
    sponsor_id = request.args.get('sponsor_id')
    sponsor = User.query.filter_by(user_id=sponsor_id).first()

    userprojects = UserProject.query.filter_by(
                    user_id=sponsor_id,
                    user_identity=UserIdentity.SCIENTIST,
                    ).all()

    if userprojects is None:
        return "该科学家无公开发布的项目"

    res = {}
    res['project_id'] = []
    res['project_title'] = []
    res['sponsor_real_name'] = []
    res['sponsor_job_title'] = []
    res['sponsor_association'] = []
    res['sponsor_research_team'] = []
    res['project_main_image_url'] = []
    res['start_time'] = []
    res['end_time'] = []
    res['category'] = []
    res['project_status'] = []
    res['project_introduction'] = []

    for userproject in userprojects:
        project = Project.query.filter_by(
                        project_id=userproject.project_id,
                        is_public=True,
                        ).first()
        if (project.project_status>=1 and project.project_status<=4) or project.project_status==7:
            res['project_id'].append(project.project_id)
            res['project_title'].append(project.project_title)
            res['project_main_image_url'].append(project.project_main_image_url)
            res['start_time'].append(str(project.start_time))
            res['end_time'].append(str(project.end_time))
            res['category'].append(project.category)
            res['project_status'].append(project.project_status)
            res['project_introduction'].append(project.project_introduction)

            res['sponsor_real_name'].append(sponsor.user_realname)
            res['sponsor_job_title'].append(sponsor.job_title)
            res['sponsor_association'].append(sponsor.association)
            res['sponsor_research_team'].append(sponsor.research_team)

    return res

'''
No.2-11
表名：UserProject & Project
功能名称：根据科学家id or 助理id找到他的所有与他身份相关的项目
input: 科学家id or 助理id，身份
output：他的所有项目的 id，题目，项目起止时间，分类，状态，待评价数据条数，是否关注
error：无项目
'''
@proj.route('/get_project_listview', methods=['GET', 'POST'])
def get_project_listview():
    user_id = request.args.get('user_id')
    identity = request.args.get('identity')
    user = User.query.filter_by(user_id=user_id).first()

    if identity == "科学家":
        print('科学家公开发布的项目')
        userprojects = UserProject.query.filter_by(
                    user_id=user_id,
                    user_identity=UserIdentity.SCIENTIST,
                    ).all()

        if userprojects==[]:
            print('该科学家无公开发布的项目')
            return "该科学家无公开发布的项目"

    elif identity == "助理":
        print('助理管理中的项目')
        userprojects = UserProject.query.filter_by(
                    user_id=user_id,
                    user_identity=UserIdentity.ASSISTANT,
                    ).all()

        if userprojects==[]:
            print('该助理无管理中的项目')
            return "该助理无管理中的项目"
    else:
        print('用户参与中的项目')
        userprojects = UserProject.query.filter_by(
                    user_id=user_id,
                    user_identity=UserIdentity.VOLUNTEER,
                    ).all()
        print(userprojects)
        if userprojects==[]:
            print('该用户无参与中的项目')
            return "该用户无参与中的项目"
    print(userprojects)
    res = {}
    res['project_id'] = []
    res['project_title'] = []
    res['start_time'] = []
    res['end_time'] = []
    res['category'] = []
    res['project_status'] = []
    res['data_tobe_estimated_count'] = []
    res['is_starred'] = []
    res['main_image_url'] = []

    for userproject in userprojects:
        # print(userproject.project_id)
        project = Project.query.filter_by(
                        project_id=userproject.project_id,
                        is_public=True,
                        # project_status=ProjectStatus.VERIFIED,
                        ).first()
        # print(project)
        if project is None:
            continue
        if (project.project_status>=1 and project.project_status<=4) or project.project_status==7:
            # print(project)
            res['project_id'].append(project.project_id)
            res['project_title'].append(project.project_title)
            res['start_time'].append(str(project.start_time))
            res['end_time'].append(str(project.end_time))
            res['category'].append(project.category)
            res['project_status'].append(project.project_status)
            res['is_starred'].append(userproject.is_starred)
            res['main_image_url'].append(project.project_main_image_url)

            data_tobe_estimated_count = Submit.query.filter_by(
                            project_id=project.project_id,
                            star_rating=0).count()
            res['data_tobe_estimated_count'].append(data_tobe_estimated_count)
    print(res)
    return res


'''
No.2-2
表名： UserProject
功能名称：用户关注参与项目情况与用户活动
input：项目id，用户id
output：是否关注、参与、点赞、用户活动
'''
# def user_project_status():
#     project_id = request.args.get('project_id')
#     userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()

#     return {"is_starred":userproject.is_starred,
#             "is_participated": userproject.is_participated,
#             "is_liked": userproject.is_liked,
#             "activities": userproject.activities}

'''
No.2-12
表名： UserProject
功能名称：关注 参与 点赞、数据总数
input：项目id
output：关注 参与 点赞情况总数
'''
@proj.route('/user_activity', methods=['GET', 'POST'])
def user_activity():
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')

    overall_starred = UserProject.query.filter_by(project_id=project_id, is_starred=True).count()
    overall_participated = UserProject.query.filter_by(project_id=project_id, is_participated=True).count()
    overall_liked = UserProject.query.filter_by(project_id=project_id, is_liked=True).count()
    overall_shared = UserProject.query.filter_by(project_id=project_id, is_shared=True).count()
    submits_count = Submit.query.filter_by(project_id=project_id).count()

    userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()

    if userproject is None:
        print("userproject is None")
        return {"overall_starred":overall_starred,
                "overall_participated": overall_participated,
                "overall_liked": overall_liked,
                "overall_shared":overall_shared,
                "submit_count":submits_count,
                "is_starred" : False,
                "is_participated": False,
                "is_liked": False,
                "is_shared": False,
                "activities": False}
    else:
        # print(userproject.is_starred)
        # print(userproject.is_participated)
        # print(userproject.is_liked)
        # print(userproject.is_shared)
        return {"overall_starred":overall_starred,
                "overall_participated": overall_participated,
                "overall_liked": overall_liked,
                "overall_shared":overall_shared,
                "submit_count":submits_count,
                "is_starred":userproject.is_starred,
                "is_participated": userproject.is_participated,
                "is_liked": userproject.is_liked,
                "is_shared": userproject.is_shared,
                "activities": userproject.activities}

'''
No.2-13
表名： UserProject
功能名称：用户修改关注
input：项目id, user id
output：none
'''
@proj.route('/set_userproject_is_starred', methods=['GET', 'POST'])
def set_userproject_is_starred():
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    new_value = request.args.get('new_value')

    userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()
    if userproject is None:
        userproject = UserProject(user_id=user_id, project_id=project_id, is_starred=True, user_identity=UserIdentity.VOLUNTEER,)
        db.session.add(userproject)
        db.session.commit()
        return "加关注成功"

    if new_value=='true':
        userproject.is_starred = True
    else:
        userproject.is_starred = False

    db.session.commit()
    print("修改关注成功")
    return "修改关注成功"


'''
No.2-13
表名： UserProject
功能名称：用户修改参与
input：项目id, user id
output：none
'''
@proj.route('/set_userproject_is_participated', methods=['GET', 'POST'])
def set_userproject_is_participated():
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    new_value = request.args.get('new_value')

    userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()

    if userproject is None:
        userproject = UserProject(user_id=user_id, project_id=project_id, is_participated=True, user_identity=UserIdentity.VOLUNTEER,)
        db.session.add(userproject)
        db.session.commit()
        print('加参与成功')
        return "加参与成功"

    if new_value=='true':
        userproject.is_participated = True
    else:
        userproject.is_participated = False

    db.session.commit()
    print("修改参与成功")
    return "修改参与成功"


'''
No.2-13
表名： UserProject
功能名称：用户修改点赞
input：项目id, user id
output：none
'''
@proj.route('/set_userproject_is_liked', methods=['GET', 'POST'])
def set_userproject_is_liked():
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    new_value = request.args.get('new_value')

    userproject = UserProject.query.filter_by(user_id=user_id, project_id=project_id).first()

    if userproject is None:
        userproject = UserProject(user_id=user_id, project_id=project_id, is_liked=True,user_identity=UserIdentity.VOLUNTEER,)
        db.session.add(userproject)
        db.session.commit()
        return "加点赞成功"

    if new_value=='true':
        userproject.is_liked = True
    else:
        userproject.is_liked = False

    db.session.commit()
    print("修改点赞成功")
    return "修改点赞成功"



'''
No.4-1
表名： Submit、Data
功能名称：提交上传
input：上传者id，项目编号，提交时间，数据类型list，数据的值list
output：1. ai置信度不达标
数据库操作：两个表各增加一项/多项
'''
@proj.route('/submit_submit', methods=['GET', 'POST'])
def submit_submit():
    project_id = request.args.get('project_id')
    uploader_id = request.args.get('uploader_id')
    submit_time = datetime.datetime.now()


    submit = Submit(project_id=project_id,
                    uploader_id=uploader_id,
                    submit_time=submit_time)

    db.session.add(submit)
    db.session.commit()

    submit = Submit.query.filter_by(project_id=project_id,
                    uploader_id=uploader_id,
                    submit_time=submit_time).first()

    return {'submit_id' : submit.submit_id}

'''
No.4-4
表名： Submit、Data
功能名称：数据上传
input：
output：1. ai置信度不达标
数据库操作：两个表各增加一项/多项
'''
@proj.route('/submit_data', methods=['GET', 'POST'])
def submit_data():
    submit_id =  request.args.get('submit_id')
    project_id =  request.args.get('project_id')
    user_id = request.args.get('user_id')

    type = request.args.get('type')
    value = request.args.get('value')
    data_title = request.args.get('show_hint')

    if type=='1':
        print("type="+str(type))
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    float_value=value)
    elif type=='2':
        print("type="+str(type))
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    int_value=value)
    elif type=='3':
        print("type="+str(type))

        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    string_value=value)
    elif type=='5':
        print("type="+str(type))

        image = request.data

        import exifread
        import re
        # print("import re")
        # imagetext = exifread.process_file(image)
        # print("exifread")
        # for key in imagetext:                           #打印键值对
        #     print(key,":",imagetext[key])

        basename = upload_data_image(user_id, project_id, submit_id, value, image)
        score, info = volunteer_image_ai(project_id, data_title, basename)
        # info = info.encode('utf-8').decode('unicode_escape')
        print("project里传回的百科："+str(info))
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    file_url=basename,
                    info=json.dumps(info),
                    float_value=score)
        # print("data.info="+data.info)

        # submit = Submit.query.filter_by(submit_id=submit_id).first()

        # ai_confidence_json = submit.ai_confidence
        # if ai_confidence_json is None:
        #     ai_confidence = {}
        # else:
        #     ai_confidence = json.loads(ai_confidence_json)
        # ai_confidence[value]=float(score)
        # submit.ai_confidence=json.dumps(ai_confidence)
        # print(str(submit_id)+"的ai得分："+str(score))

    elif type=='6':
        print("type="+str(type))

        video = request.data['file']
        basename = upload_data_video(user_id, project_id, submit_id, value, video)
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    file_url=basename)
    elif type=='8':
        print("type="+str(type))
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    cata_value=value)
    elif type=='9':
        print("type="+str(type))
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    map_value=value)

    else:
        print("type="+str(type))
        data = Data(submit_id=submit_id,
                    data_title=data_title,
                    data_type=type,
                    string_value=value)

    db.session.add(data)
    db.session.commit()
    print("数据提交成功，值为"+str(value))
    return "数据提交成功"




'''
No.4-2
表名： Submit
功能名称：评价细节
input：submit_id
output：star rating, estimate content, (提交的数据)
'''
@proj.route('/get_estimate_details', methods=['GET', 'POST'])
def get_estimate_details():
    submit_id = request.args.get('submit_id')
    submit = Submit.query.filter_by(submit_id=submit_id).first()
    res = {}
    res['star_rating'] = submit.star_rating
    print("submit.star_rating"+str(submit.star_rating))
    if submit.estimation_content is None:
        res['estimation_content'] = "暂无回复"
    else:
        res['estimation_content'] = submit.estimation_content
    res['estimation_time'] = str(submit.estimation_time)
    return res



'''
No.4-3
表名： Submit
功能名称：获取用户对该项目的所有提交
input：user id, project id
output: all submits
'''
@proj.route('/get_submit_brief', methods=['GET', 'POST'])
def get_submit_brief():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')
    submits = Submit.query.filter_by(uploader_id=user_id, project_id=project_id).all()
    print("user_id="+user_id)
    print("project_id="+project_id)

    # if submits is None:
    #     print("无提交")
    #     return "无提交"
    # else:
    #     print(submits)

    res = {}
    res['submit_id'] = []
    res['submit_time'] = []
    res['ai_confidence'] = []
    res['star_rating'] = []
    _zero = False
    _pass = False
    submits.sort(key=lambda x:x.submit_time, reverse=True)
    for submit in submits:
        ai_confidence_json = submit.ai_confidence
        if ai_confidence_json is not None:
            ai_confidence = json.loads(ai_confidence_json)
            for key in ai_confidence.keys():
                if ai_confidence[key]==0:
                    _zero = True
                elif ai_confidence[key]!=0:
                    _pass = True
            if _zero and _pass:
                res['ai_confidence'].append(0.5)
            elif _zero and not _pass:
                res['ai_confidence'].append(0)
            elif not _zero and _pass:
                res['ai_confidence'].append(1)
        else:
            res['ai_confidence'].append(0)

        res['submit_id'].append(submit.submit_id)
        res['submit_time'].append(str(submit.submit_time))
        res['star_rating'].append(submit.star_rating)

    print("提交总数为"+str(len(submits)))
    return res



'''
No.4-4
表名：Data, Submit
功能名称：获取本次提交的所有数据
input: submit_id
output: show_hint, value
'''
@proj.route('/get_data4submit', methods=['GET', 'POST'])
def get_data4submit():
    submit_id = request.args.get('submit_id')
    submit = Submit.query.filter_by(submit_id=submit_id).first()
    datas = Data.query.filter_by(submit_id=submit_id).all()

    # project = Project.query.filter_by(project_id=submit.project_id).first()
    # data_format_json = project.data_format # json
    # data_format = json.loads(data_format_json) # 转换成python dict

    res = {}
    res['show_hint'] = []
    res['value'] = []
    res['type'] = []
    res['info'] = []
    res['score'] = []

    res['show_hint'].append("提交日期")
    res['type'].append(3)
    res['value'].append(submit.submit_time.strftime('%Y-%m-%d'))
    res['info'].append(' ')
    res['score'].append(' ')

    for data in datas:
        res['show_hint'].append(data.data_title)
        res['type'].append(data.data_type)
        if data.data_type==1:
            res['value'].append(data.float_value)
            res['info'].append(data.info)
            res['score'].append(data.float_value)
        elif data.data_type==2:
            res['value'].append(data.int_value)
            res['info'].append(data.info)
            res['score'].append(data.float_value)
        elif data.data_type==3:
            res['value'].append(data.string_value)
            res['info'].append(data.info)
            res['score'].append(data.float_value)
        elif data.data_type==5: # pic
            res['value'].append(data.file_url)
            res['info'].append(json.loads(data.info))
            res['score'].append(data.float_value)
        elif data.data_type==8: # cate
            res['value'].append(data.cata_value)
            res['info'].append(data.info)
            res['score'].append(data.float_value)
        elif data.data_type==9:
            res['value'].append(data.map_value)
            res['info'].append(data.info)
            res['score'].append(data.float_value)
        else:
            res['info'].append(' ')
            res['score'].append(' ')

    print(res)
    return res








