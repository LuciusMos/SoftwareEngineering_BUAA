from backend.models import *
from backend.upload import *
from flask import Blueprint
import pdb

hp = Blueprint("homepage",__name__) #生成蓝图对象

'''
No.5-1
表名：Project
功能名称：主页-最新发布5个
input：none
output：项目id，主图，名字，发起人，单位，职称，团队，category,start_time
'''
@hp.route('/get_latest_project', methods=['GET', 'POST'])
def get_latest_project():
    # projects = Project.query.filter_by(project_status=ProjectStatus.VERIFIED).all()
    # projects = Project.query.filter(Project.start_time!=None, Project.project_status==ProjectStatus.VERIFIED).all()
    project_list1 = Project.query.filter_by(project_status=ProjectStatus.VERIFIED).all()
    project_list2 = Project.query.filter_by(project_status=ProjectStatus.DATA_COLLECTING).all()
    project_list3 = Project.query.filter_by(project_status=ProjectStatus.CLOSED).all()
    project_list4 = Project.query.filter_by(project_status=ProjectStatus.NOT_DIS).all()
    project_list5 = Project.query.filter_by(project_status=ProjectStatus.ANALYSISING).all()
    projects = project_list1+project_list2+project_list3+project_list4+project_list5

    projects.sort(key=lambda x: x.start_time, reverse=True)
    # print(projects)
    res = {}
    res['project_id'] = []
    res['project_title'] = []
    res['sponsor_real_name'] = []
    res['sponsor_job_title'] = []
    res['sponsor_association'] = []
    res['sponsor_research_team'] = []
    res['project_main_image_url'] = []
    res['start_time'] = []
    res['category'] = []
    res['project_status'] = []

    count = 0
    for project in projects:
        if count==5:
            break
        count += 1
        res['project_id'].append(project.project_id)
        res['project_title'].append(project.project_title)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['category'].append(project.category)
        res['start_time'].append(str(project.start_time))
        res['project_status'].append(project.project_status)

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
No.5-2
表名：Project
功能名称：搜索最新发布15个
input：none
output：项目id，主图，名字，发起人，单位，职称，团队，category, start_time
'''
def get_more_latest_projects():
    # projects = Project.query.filter(Project.start_time!=None,Project.project_status==ProjectStatus.VERIFIED).all()
    project_list1 = Project.query.filter_by(project_status=ProjectStatus.VERIFIED).all()
    project_list2 = Project.query.filter_by(project_status=ProjectStatus.DATA_COLLECTING).all()
    project_list3 = Project.query.filter_by(project_status=ProjectStatus.CLOSED).all()
    project_list4 = Project.query.filter_by(project_status=ProjectStatus.NOT_DIS).all()
    project_list5 = Project.query.filter_by(project_status=ProjectStatus.ANALYSISING).all()
    projects = project_list1+project_list2+project_list3+project_list4+project_list5
    projects.sort(key=lambda x: x.start_time, reverse=True)
    # print(projects)
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
    res['project_status'] = []
    res['category'] = []
    res['project_introduction'] = []

    count = 0
    for project in projects:
        if count==15:
        	break
        count += 1
        res['project_id'].append(project.project_id)
        res['project_title'].append(project.project_title)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['project_status'].append(project.project_status)
        res['category'].append(project.category)
        res['start_time'].append(str(project.start_time))
        res['end_time'].append(str(project.end_time))
        res['project_introduction'].append(project.project_introduction)
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
No.5-3
表名：User
功能名称：主页-新入驻大咖
input：none
output：id, 姓名，照片，职称，单位
'''
@hp.route('/get_latest_scientists', methods=['GET', 'POST'])
def get_latest_scientists():
    scientists = User.query.filter_by(user_identity=UserIdentity.SCIENTIST).all()
    scientists.sort(key=lambda x: x.apply_time, reverse=True)

    res = {}
    res['user_id'] = []
    res['user_realname'] = []
    res['photo_url'] = []
    res['job_title'] = []
    res['association'] = []

    count = 0
    for scientist in scientists:
        if count==10:
            break
        count += 1
        res['user_id'].append(scientist.user_id)
        res['user_realname'].append(scientist.user_realname)
        res['photo_url'].append(scientist.photo_url)
        res['job_title'].append(scientist.job_title)
        res['association'].append(scientist.association)

    return res



'''
No.5-4
表名：Project
功能名称：主页-最热门5个
input：none
output：项目id，主图，名字，发起人，单位，职称，团队，category, start_time
'''
@hp.route('/get_hotest_project', methods=['GET', 'POST'])
def get_hotest_project():
    ack = int(request.args.get('ack'))
    return get_hotest_project_2(ack)

def get_hotest_project_2(ack):
    # projects = Project.query.filter_by(project_status=ProjectStatus.VERIFIED).all()
    project_list1 = Project.query.filter_by(project_status=ProjectStatus.VERIFIED).all()
    project_list2 = Project.query.filter_by(project_status=ProjectStatus.DATA_COLLECTING).all()
    project_list3 = Project.query.filter_by(project_status=ProjectStatus.CLOSED).all()
    project_list4 = Project.query.filter_by(project_status=ProjectStatus.NOT_DIS).all()
    project_list5 = Project.query.filter_by(project_status=ProjectStatus.ANALYSISING).all()
    projects = project_list1+project_list2+project_list3+project_list4+project_list5

    # projects = Project.query.all()
    pairs = []

    for project in projects:
        userprojects_count = UserProject.query.filter_by(
                                project_id=project.project_id
                                ).count()
        pairs = pairs + [(project.project_id, userprojects_count)]

    pairs.sort(key=lambda x: x[1], reverse=True)
    print(pairs)

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
    for pair in pairs:
        count += 1
        if count <= ack:
            continue
        if count > ack+10:
            break
        project = Project.query.filter_by(project_id=pair[0]).first()
        res['project_id'].append(project.project_id)
        res['project_title'].append(project.project_title)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['start_time'].append(str(project.start_time))
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
No.5-5
表名：Project
功能名称：主页-各门类最高赞
input：none
output：项目id，主图，名字，赞数
'''
@hp.route('/get_top_liked_project_by_category', methods=['GET', 'POST'])
def get_top_liked_project():
    branch_names = ["经济", "社会", "教育", "心理", "文学", "物理", "化学", "动物", "植物", "微生物", "地理", "大气", "生态", "天文", "水文", "建筑", "农业", "医学", "艺术", "管理学", "新闻传媒", "信息技术"];

    res = {}
    res['branch_name'] = []
    res['project_main_image_url_1'] = []
    res['project_title_1'] = []
    res['project_id_1'] = []
    res['liked_count_1'] = []
    res['status_1'] = []
    res['project_main_image_url_2'] = []
    res['project_title_2'] = []
    res['project_id_2'] = []
    res['liked_count_2'] = []
    res['status_2'] = []

    for branch_name in branch_names:
        project_list1 = Project.query.filter(
            Project.branch.like('%'+branch_name+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.VERIFIED
            ).all()
        project_list2 = Project.query.filter(
            Project.branch.like('%'+branch_name+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.DATA_COLLECTING
            ).all()
        project_list3 = Project.query.filter(
            Project.branch.like('%'+branch_name+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.CLOSED
            ).all()
        project_list4 = Project.query.filter(
            Project.branch.like('%'+branch_name+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.NOT_DIS
            ).all()
        project_list5 = Project.query.filter(
            Project.branch.like('%'+branch_name+'%'),
            Project.is_public==True,
            Project.project_status==ProjectStatus.ANALYSISING
            ).all()

        projects = project_list1+project_list2+project_list3+project_list4+project_list5

        pairs = []
        for project in projects:
            userprojects_count = UserProject.query.filter_by(
                                    project_id=project.project_id,
                                    is_liked=True,
                                    ).count()
            pairs = pairs + [(project.project_id, userprojects_count)]

        pairs.sort(key=lambda x: x[1], reverse=True)
        if pairs==[]:
            continue
        if len(pairs)>=2:
            res['branch_name'].append(branch_name)

            res['project_id_1'].append(pairs[0][0])
            res['liked_count_1'].append(pairs[0][1])
            project = Project.query.filter_by(project_id=pairs[0][0]).first()
            res['project_main_image_url_1'].append(project.project_main_image_url)
            res['project_title_1'].append(project.project_title)
            res['status_1'].append(project.project_status)


            res['project_id_2'].append(pairs[1][0])
            res['liked_count_2'].append(pairs[1][1])
            project = Project.query.filter_by(project_id=pairs[1][0]).first()
            res['project_main_image_url_2'].append(project.project_main_image_url)
            res['project_title_2'].append(project.project_title)
            res['status_2'].append(project.project_status)

    print("get_top_liked_project"+str(res))
    return res

'''
No.5-6
表名：Project
功能名称：主页-为我推荐
input：none
output：项目id，题目，发起人姓名、职称，发起人工作单位，
        研究团队，主图url，项目起止时间，分类，状态，项目简要
'''
@hp.route('/get_recommended_projects', methods=['GET', 'POST'])
def get_recommended_projects():
    user_id = request.args.get('user_id')
    ack = int(request.args.get('ack'))
    return get_recommended_projects_2(user_id, ack)


def get_recommended_projects_2(user_id, ack):

    rec_proj_ids = get_recommended(user_id)

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
    for project_id in rec_proj_ids:
        count += 1
        if count <= ack:
            continue
        if count > ack+10:
            break
        print("想推荐的project_id="+str(project_id))
        project = Project.query.filter_by(project_id=project_id).first()
        # print("想推荐的project_id="+str(project.project_id))
        res['project_id'].append(project.project_id)
        res['project_title'].append(project.project_title)
        res['project_main_image_url'].append(project.project_main_image_url)
        res['start_time'].append(str(project.start_time))
        res['end_time'].append(str(project.end_time))
        res['category'].append(project.category)
        res['project_status'].append(project.project_status)
        res['project_introduction'].append(project.project_introduction)
        # 选一位发起人
        sponsor_userproject = UserProject.query.filter_by(
                                project_id=project.project_id,
                                user_identity=UserIdentity.SCIENTIST
                                ).first()
        print("项目id="+str(project.project_id))
        print("发起人id="+str(sponsor_userproject.user_id))
        sponsor = User.query.filter_by(user_id=sponsor_userproject.user_id).first()
        res['sponsor_real_name'].append(sponsor.user_realname)
        res['sponsor_job_title'].append(sponsor.job_title)
        res['sponsor_association'].append(sponsor.association)
        res['sponsor_research_team'].append(sponsor.research_team)

    return res

