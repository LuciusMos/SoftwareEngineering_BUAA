
from backend.models import *
from backend.upload import *
from flask import Blueprint
import pdb
ident = Blueprint("identity",__name__) #生成蓝图对象

'''
No.1-5
表名： Use UserProject
功能名称：科学家个人简介页面
input：user_id
output：发布项目数、累计参与人数、职称、研究方向、个人简介、姓名、工作单位学校、所属团队
error：无
'''
@ident.route('/get_scientist_info', methods=['GET', 'POST'])
def get_scientist_info():
    scientist_id = request.args.get('sponsor_id')
    scientist = User.query.filter_by(user_id=scientist_id).first()
    if scientist is None:
        print("不存在此科学家 scientist_id="+str(scientist_id))
        return "不存在此科学家"
    scientist_info = {}
    scientist_info['user_realname'] = scientist.user_realname
    scientist_info['photo_url'] = scientist.photo_url
    scientist_info['association'] = scientist.association
    scientist_info['research_team'] = scientist.research_team
    scientist_info['job_title'] = scientist.job_title
    scientist_info['research_area'] = scientist.research_area
    scientist_info['personal_introduction'] = scientist.personal_introduction
    all_projects = UserProject.query.filter_by(
                                        user_id=scientist_id,
                                        user_identity=UserIdentity.SCIENTIST).all()
    scientist_info['overall_project_count'] = len(all_projects)
    scientist_info['overall_participant_count'] = 0
    for project in all_projects:
        participant_count = UserProject.query.filter_by(
                                project_id=project.project_id,
                                user_identity=UserIdentity.VOLUNTEER).count()
        scientist_info['overall_participant_count'] = scientist_info['overall_participant_count'] + participant_count
    # print("1）"+str(scientist_info))
    return scientist_info


'''
No.1-9
表名： User
功能名称：科学家申请认证
input：申请者id、姓名、工作单位/学校、所属团队、相关证件照片、简历、职称、学历、研究方向、证明文件
output：无
数据库操作：更改用户表状态
'''
@ident.route('/apply_scientist', methods=['GET', 'POST'])
def apply_scientist():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    user.verify_result = 1 # 审核中
    user.user_realname = request.args.get('user_realname')
    user.association = request.args.get('association')
    user.research_team = request.args.get('research_team')
    user.academic_degree = request.args.get('academic_degree')
    photo_raw = request.data
    basename = upload_photo(user_id, photo_raw)
    user.photo_url = basename
    user.apply_time = datetime.datetime.now()
    user.job_title = request.args.get('job_title')
    user.research_area = request.args.get('research_area')
    db.session.commit()
    return str(user.apply_time.strftime('%Y%m%d%H%M%S'))

'''
No.1-10
表名： User, ApplyingAssistant
功能名称：助理申请认证
input：申请者id、项目id、科学家id、工作单位/学校、所属团队、相关证件照片、简历、职称、学历、研究方向、个人简介、证明文件
output：无
数据库操作：增加一项
'''
@ident.route('/apply_assistant', methods=['GET', 'POST'])
def apply_assistant():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')
    scientist_id = request.args.get('scientist_id')
    user = User.query.filter_by(user_id=user_id).first()
    user.verify_result = 0 # 不知道助理审核状态
    user.user_realname = request.args.get('user_realname')
    user.association = request.args.get('association')
    user.research_team = request.args.get('research_team')
    user.academic_degree = request.args.get('academic_degree')

    photo_raw = request.data
    basename = upload_photo(user_id, photo_raw)
    user.photo_url = basename

    # user.resume_url = request.args.get('resume_url')
    user.job_title = request.args.get('job_title')
    user.research_area = request.args.get('research_area')
    user.personal_introduction = request.args.get('personal_introduction')
    user.apply_time = datetime.datetime.now()

    db.session.commit()
    return str(user.apply_time.strftime('%Y%m%d%H%M%S'))


'''
No.1-11
表名： User
功能名称：助理身份认证是否已完善
input：申请者id
output：工作单位/学校、所属团队、相关证件照片、简历、职称、学历、研究方向、个人简介、证明文件
数据库操作：
'''
@ident.route('/if_applied', methods=['GET', 'POST'])
def if_applied():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    print(user.user_realname)
    print(user.association)
    print(user.photo_url)
    print(user.job_title)
    print(user.academic_degree)
    print(user.research_area)
    if user.user_realname is None or user.association is None or  user.photo_url is None or user.academic_degree is None or user.research_area is None:
        print("请完善个人身份信息")
        return "请完善个人身份信息"
    else:
        return "个人身份已验证"



'''
No.1-12
表名： User
功能名称：根据关键字（email or realname）找到科学家
input：关键字
output：科学家id, email、realname、头像url、association、research_area, 职称
error：no such scientist
'''
@ident.route('/search_scientist_by_keyword', methods=['GET', 'POST'])
def search_scientist_by_keyword():
    keyword = request.args.get('keyword')
    candidates_by_realname = User.query.filter(
                    User.user_realname.like('%'+keyword+'%'),
                    ).all()
    candidates_by_email = User.query.filter(
                    User.user_email.like('%'+keyword+'%'),
                    ).all()
    all_candidates = candidates_by_email + candidates_by_realname

    candidates = {}
    candidates['user_id'] = []
    candidates['user_email'] = []
    candidates['user_realname'] = []
    candidates['photo_url'] = []
    candidates['association'] = []
    candidates['research_area'] = []
    candidates['job_title'] = []

    for candidate in all_candidates:
        candidates['user_id'].append(candidate.user_id)
        candidates['user_email'].append(candidate.user_email)
        candidates['user_realname'].append(candidate.user_realname)
        candidates['photo_url'].append(candidate.photo_url)
        candidates['association'].append(candidate.association)
        candidates['research_area'].append(candidate.research_area)
        candidates['job_title'].append(candidate.job_title)

    return candidates


'''
No.1-13
表名： User
功能名称：提交证明文件的图片
input：user id , file, index apply time
output：
'''
@ident.route('/submit_proof_image', methods=['GET', 'POST'])
def submit_proof_image():
    user_id = request.args.get('user_id')
    index = request.args.get('index')
    apply_time = request.args.get('apply_time')
    photo_raw = request.data

    basename = upload_proof_photo(user_id, index, apply_time, photo_raw)
    user = User.query.filter_by(user_id=user_id).first()
    proof_file_json = user.proof_file
    if index == '0' or proof_file_json is None:
        proof_file = {}
    else:
        proof_file = json.loads(proof_file_json)
    proof_file[index] = basename
    user.proof_file=json.dumps(proof_file)
    print("证明文件"+str(index)+"提交成功"+basename)
    return "证明文件"+str(index)+"提交成功"+basename


'''
No.1-14
表名： User
功能名称：身份认证信息
input：申请者id
output：工作单位/学校、所属团队、相关证件照片、简历、职称、学历、研究方向、个人简介、证明文件
'''
@ident.route('/get_apply_info', methods=['GET', 'POST'])
def get_apply_info():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()

    apply_info = {}
    apply_info['realname'] = user.user_realname
    apply_info['association'] = user.association
    apply_info['job_title'] = user.job_title
    apply_info['academic_degree'] = user.academic_degree
    apply_info['research_area'] = user.research_area
    apply_info['research_team'] = user.research_team
    apply_info['personal_introduction'] = user.personal_introduction
    apply_info['photo_url'] = user.photo_url

    return apply_info


















