
from backend.models import *
from flask import Blueprint

user1 = Blueprint("user1",__name__) #生成蓝图对象

@user1.route('/init_reset_pwd', methods=['GET', 'POST'])
def init_reset_pwd():
    for user_id in range(0,22):
        user = User.query.filter_by(user_id=user_id).first()
        print(user)
        user.set_password(user.user_password)
        db.session.commit()
    return "初始化密码成功"

@user1.route('/init_register_time', methods=['GET', 'POST'])
def init_register_time():
    for _ in range(1,102):
        user = User.query.filter_by(user_id=_).first()
        user.register_time=datetime.datetime.now()
        db.session.commit()
    return "注册时间添加成功"


import random

def Unicode():
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)

def GBK2312():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xfe)
    val = f'{head:x} {body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str

# print(GBK2312())

def get_rand_nickname():
    num = random.randint(2,5)
    str = ''
    for _ in range(num):
        str += GBK2312()
    return str

first_name = ["冰", "樟", "舫", "舟", "梦", "蝶", "宁", "江", "莎安娜", "沙琪", "圆", "成", "天", "音", "上官", "柊", "歌","鸽","米","蓝","鱼","竹","苏","莉","时","涛","桃","韬","平","花","慕容","云","楚","绮"]
second_name = ["伟", "欣欣","拉拉", "佳佳","海儿","菲菲", "翔", "华", "建国", "洋", "刚", "万里", "爱民", "牧", "佳", "路", "昕", "鑫", "兵", "硕", "志宏", "峰", "泪", "雷", "文","明浩", "光", "超", "军", "达","姐","哥"]

# print(get_rand_nickname())
@user1.route('/init_signup', methods=['GET', 'POST'])
def init_signup():
    for _ in range(100):
        user = User(user_email=str(_)+"@163.com",
                    user_identity=1,
                    user_nickname=random.choice(first_name) + random.choice(second_name),
                    register_time=date(random.randint(2015,2019),random.randint(1,12),random.randint(1,28)),
                    profile_url='travel.jpeg',
                    user_themecode='CommonwealGreen',
                    ) # 初始化为user_email，之后去个人设置里改
        user.set_password(str(_)+"pwdpwd")
        db.session.add(user)
        db.session.commit()
        print("注册成功"+str(_))
    return "注册成功"


@user1.route('/reset_nickname', methods=['GET', 'POST'])
def reset_nickname():
    for _ in range(21, 101):
        user_id = _
        user = User.query.filter_by(user_id=user_id).first()
        user.user_nickname = random.choice(first_name) + random.choice(second_name)
        db.session.commit()
    return "昵称修改成功"



@user1.route('/init_apply_scientist', methods=['GET', 'POST'])
def init_apply_scientist():
    for _ in range(4,16):
        user_id = _
        user = User.query.filter_by(user_id=user_id).first()
        user.verify_result = 3
        user.user_identity = 3
        user.user_realname = str(_)+"号科学家"
        user.association = '中国科学院动物研究所研究员'
        user.research_team = '国家自然基金委重点项目、创新群体项目和国家重点研发计划重点专项'
        user.photo_url = 'wfwys.png'
        user.resume_url = ''
        user.job_title = '院士'
        user.apply_time = datetime.datetime.now()
        user.research_area = '濒危动物保护生物学'
        # user.personal_introduction = request.args.get('personal_introduction')
        # proof_file_json = json.dumps(request.args.get('proof_file')) # TODO: 传过来的是list
        # user.proof_file = proof_file_json
        db.session.commit()
        print('科学家认证提交成功')
    return "科学家认证提交成功"


@user1.route('/init_apply_assistant', methods=['GET', 'POST'])
def init_apply_assistant():
    for _ in range(16,30):
        user_id = _
        user = User.query.filter_by(user_id=user_id).first()
        user.verify_result = 3
        user.user_identity = 2
        user.user_realname = str(_)+"号助理"
        user.association = '清华大学生物系'
        user.research_team = '国家自然基金委重点项目、创新群体项目和国家重点研发计划重点专项'
        user.photo_url = 'zhuli.jpg'
        user.resume_url = ''
        user.job_title = '博士'
        user.apply_time = datetime.datetime.now()
        user.research_area = '濒危动物保护生物学'
        # user.personal_introduction = request.args.get('personal_introduction')
        # proof_file_json = json.dumps(request.args.get('proof_file')) # TODO: 传过来的是list
        # user.proof_file = proof_file_json
        db.session.commit()
        print('助理认证提交成功')
    return "助理认证提交成功"



@user1.route('/add_project', methods=['GET', 'POST'])
def add_project():
    category = ['双子叶植物 / 十字花科', '天文学 / 星象学', '无脊椎动物 / 昆虫类',
                '体育 / 文体活动','文学 / 纪实文学' ,'脊椎动物 / 哺乳动物',
                '光学','热力学','裸子植物 / 银杏纲',
                '信息技术 / 视觉计算','裸子植物 / 松山纲']
    branch = ['植物','天文','动物',
                '体育','文学','动物',
                '物理','物理','植物',
                '计算机','植物']

    for _ in range(30):
        project_title = "第"+str(_)+"个瞎编的项目"
        start_time = date(2019,int(_%12+1),_+1)
        # start_time = datetime.datetime.strptime('2019-02-12','%Y-%m-%d')
        # print(start_time)
        time_delta_verify = datetime.timedelta(14)
        time_delta_data_collecting = datetime.timedelta(300)
        time_delta_close = datetime.timedelta(600)
        intro='项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍项目介绍'

        project = Project(project_title=project_title,
                            start_time=start_time,
                            data_start_time=start_time+time_delta_verify,
                            data_end_time=start_time+time_delta_verify+time_delta_data_collecting,
                            end_time=start_time+time_delta_close,
                            project_introduction='第'+str(_)+"个项目的介绍"+intro,
                            way_of_participation='参与方式介绍参与方式介绍参与方式介绍参与方式介绍参与方式介绍',
                            precautions='注意事项注意事项注意事项注意事项注意事项',
                            background_knowledge='背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识背景知识',
                            data_format_description='数据格式说明数据格式说明数据格式说明数据格式说明数据格式说明数据格式说明数据格式说明数据格式说明数据格式说明',
                            is_public=True,
                            project_main_image_url='SrbXjbo-XbQ.jpg',
                            category=category[_%3],
                            branch=branch[_%3])
        db.session.add(project)
        db.session.commit()
        print("项目"+str(_)+"添加成功")

    return "项目创建成功"

@user1.route('/add_project_demo', methods=['GET','POST'])
def add_project_demo():
    project = Project(
                project_title="短尾猴，我们的朋友",
                start_time=date(2019,3,5),
                data_start_time=date(2019,3,15),
                data_end_time=date(2020,3,15),
                end_time=date(2022,4,30),
                project_introduction='在中国，狩猎和栖息地的丧失，减少了短尾猴的种群，在一些地方甚至局部灭绝。短尾猴是中国猕猴属中除猕猴外分布最广、数量最多的一个种，其种群数量估计有7万只，其中70-80%分布在云南和广西两省区；广东和福建已非常稀少，在广东，仅分布在惠水一带；福建和贵州南部的可能已接近绝迹。 在武夷山自然保护区活跃着一群短尾猴，经常和进入武夷山保护区旅游的游人嬉闹，与人和谐相处。武夷山自然保护区加大对野生动物保护的力度，所以武夷山自然保护区的猴群越来越多，短尾猴的数量也逐年增加，据武夷山保护区管理人员介绍，武夷山自然保护区的短尾猴已达到数千只。',
                way_of_participation='如果您在野外有看到短尾猴的踪迹或生活痕迹，可上传照片并发送定位。',
                precautions='请勿影响短尾猴或其他动物的正常生活，尊重自然，珍爱生命。',
                background_knowledge='短尾猴（学名：Macaca arctoides），也称红面猴，是体型较大的一种猕猴，体重5千克，体长50-56厘米，尾极短；颜面部常为暗红色或带紫红色斑块；体色深暗，背部多为暗褐黑色或暗橄榄棕褐色，腹面稍浅于背部，亦为暗棕黄色。中国西南一带的短尾猴头顶棕色较重，而产于东部者其头顶褐色显著。尾巴短得出奇，还没有后脚长，仅为体长的十分之一，而且被毛稀少，因此又有“断尾猴”之称。\n主要栖于1500-3000米的原始阔叶林、针阔混交林或竹林地带。食性较杂，既取食野果、树叶、竹笋，也捕食蟹、蛙等小动物。分布于中国的华南及西南地区、孟加拉、柬埔寨、印度等国。属于CITES附录Ⅱ。\n短尾猴是体型较大的一种猕猴，短尾猴的颜面宽阔，头骨相对较宽，有明显的眉脊。体形浑圆、憨实，四肢粗壮，雄兽的体长为52-65厘米，体重9.9-10.2千克；雌兽的体长为48-59厘米，7.5-9.1千克。前额部分裸露无毛，几乎全部秃顶，呈灰黑色，颊部的毛也较为稀少。胸部、腹部，以及四肢内侧的毛稀疏而且颜色较浅，肩部、颈部和背部的毛较为粗糙。胼胝的周围也是裸露无毛。尾巴短得出奇，还没有后脚长，仅为体长的十分之一，而且被毛稀少，因此又有“断尾猴”之称。\n短尾猴的成体头顶毛较长，由中央向两侧披开。两颊和颏下的须毛像兜腮胡子，且其唇下的颏须暗褐色而周边棕白色呈层次分明的半月形。成年雄猴颜面鲜红色，老年紫红色，幼体肉红色。成体眉毛多呈棕黄色，老年猴面部出现白毛，常伸向鼻侧。耳较小，尾短光秃无毛。体背毛色棕褐，披毛较长，腹面略浅；体毛长而密，成年猴毛长8-12cm，其毛色在幼年为淡褐色，以后逐渐变深，至成年为深褐色，但胸腹部及四肢内测较淡，呈淡棕褐色。成体在中国西南一带的短尾猴头顶棕色较重，而产于东部者其头顶褐色显著。\n短尾猴系南亚和东南亚地区的特有灵长类。主要栖于热带雨林、季雨林、季风常绿阔叶林、落叶阔叶林以及中山针阔混交林。栖息高度可从沿海低地至海拔2650米的中山林区。栖息在高山密林的较高海拔林带，主要利用常绿阔叶林带和常绿与落叶混交林带这两个林带，除此之外，在其栖息地中还需有山溪水源和悬崖陡壁，供猴群喝水和夜间睡眠。栖息林带的植被以山毛榉科植物为主，其果实和叶是短尾猴的主要食物，特别是果实，在秋季和大部分冬季被广泛食用。',
                data_format_description='每次提交一张或多张照片，系统自动采集您的地理位置，请开启GPS功能。',
                data_format='{"地理位置": {"type": 3, "max": 20, "min": 1}, "短尾猴照片": {"type": 5, "max": 200, "min": 0}}',
                is_public=True,
                project_main_image_url='duanweihou.jpg',
                category='野生动物 / 哺乳动物 / 灵长类',
                branch='动物',
                )
    db.session.add(project)
    db.session.commit()
    project = Project.query.filter_by(project_title='短尾猴，我们的朋友').first()
    userproject = UserProject(user_id=7, user_identity=3, is_participated=True, project_id=project.project_id)
    db.session.add(userproject)
    db.session.commit()
    userproject = UserProject(user_id=19, user_identity=2, is_participated=True, project_id=project.project_id)
    db.session.add(userproject)
    db.session.commit()
    for _ in range(32,90):
        userproject = UserProject(user_id=_, project_id=project.project_id, user_identity=1, is_participated=True, is_liked=random.randint(0,1), is_starred=random.randint(0,1), is_shared=random.randint(0,1))
        db.session.add(userproject)
        db.session.commit()
    return "短尾猴项目添加成功"

@user1.route('/add_userproject', methods=['GET', 'POST'])
def add_userproject():
    for _ in range(1, 11):
        userproject = UserProject(user_id=random.randint(21, 100),
                                project_id=_,
                                user_identity=1,
                                is_participated=True,
                                is_liked=random.randint(0,1),
                                is_starred=random.randint(0,1),
                                is_shared=random.randint(0,1))
        db.session.add(userproject)
        try:
            db.session.commit()
        except:
            continue

        print("添加志愿者")

    return "添加完毕"


@user1.route('/init_project_milestone', methods=['GET', 'POST'])
def init_project_milestone():
    for id in range(1,31):
        milestone = {}
        project = Project.query.filter_by(project_id=id).first()
        if project is not None:
            for e in range(random.randint(3,10)):
                datetime = date(random.randint(2016,2020),random.randint(1,12),random.randint(1,28))
                event = ""
                iter = random.randint(1,10)
                for _ in range(iter):
                    event += "事件详情"
                milestone[str(datetime)] = event
            # print(milestone)
            project.milestone = json.dumps(milestone,ensure_ascii=False)
            db.session.commit()
            print("项目"+str(project.project_id)+"进度初始化完成")

    return "项目进度初始化完毕"

@user1.route('/init_project_milestone_begin_data_colleting', methods=['GET', 'POST'])
def init_project_milestone_begin_data_colleting():
    for id in range(1,11):
        project = Project.query.filter_by(project_id=id).first()
        if project.milestone is None:
            milestone={}
            milestone[str(project.start_time)]="复审"
            milestone[str(project.data_start_time)]="数据收集开始"
            project.milestone = json.dumps(milestone, ensure_ascii=False)
            db.session.commit()
        else:
            milestone = json.loads(project.milestone)
            milestone[str(project.data_start_time)]="数据收集开始"
            project.milestone = json.dumps(milestone, ensure_ascii=False)
            db.session.commit()
    return "项目milestone数据开始收集更新"

@user1.route('/init_project_milestone_31', methods=['GET', 'POST'])
def init_project_milestone_4():
    # for id in range(1,31):
    milestone = {}
    project = Project.query.filter_by(project_id=31).first()
    if project is not None:
        datetime = date(2016,3,25)
        milestone[str(datetime)]="审核通过"
        datetime = date(2016,4,5)
        milestone[str(datetime)]="数据需求更新，需采集志愿者地理位置"
        datetime = date(2016,4,6)
        milestone[str(datetime)]="数据收集开始"
        datetime = date(2016,7,20)
        milestone[str(datetime)]="数据量达到2.7万，尝试对部分数据进行清洗和初步分析"
        datetime = date(2017,7,20)
        milestone[str(datetime)]="数据收集结束"
        datetime = date(2017,7,21)
        milestone[str(datetime)]="数据量充足，导出所有数据并进行清洗"
        datetime = date(2017,7,20)
        milestone[str(datetime)]="分析研究"
        datetime = date(2019,2,2)
        milestone[str(datetime)]="项目成果公开"
        datetime = date(2019,2,3)
        milestone[str(datetime)]="项目结项"

        # for e in range(random.randint(3,10)):
        #     datetime = date(random.randint(2016,2020),random.randint(1,12),random.randint(1,28))
        #     event = ""
        #     iter = random.randint(1,10)
        #     for _ in range(iter):
        #         event += "事件详情"
        #     milestone[str(datetime)] = event
        # print(milestone)
        project.milestone = json.dumps(milestone,ensure_ascii=False)
        db.session.commit()
        print("项目"+str(project.project_id)+"进度初始化完成")


    return "项目"+str(project.project_id)+"进度初始化完毕"


def getNotificationContent(type):
    if type==0:
        return "您提交的数据已收到来自科学家/助理的评价反馈"
    elif type==1:
        return '您有新的数据待评价'
    elif type==2:
        return '您收到一条项目邀请'
    elif type==3:
        return "您收到一条助理申请"
    elif type==4:
        return '您被科学家设置为项目助理'
    elif type==5:
        return "您的申请已通过"

@user1.route('/init_Notification', methods=['GET', 'POST'])
def init_Notification():
    for userid in range(30):
        for _ in range(10):
            type = random.randint(0,5)
            notification = Notification(
                        user_id=userid,
                        notification_type=type,
                        notification_content=getNotificationContent(type),
                        project_id=random.randint(1,30),
                        notification_time=date(random.randint(2016,2020),random.randint(1,12),random.randint(1,28)))
            db.session.add(notification)
            db.session.commit()
        print("用户"+str(userid)+"已完成消息盒子初始化")

    return "消息盒子完成初始化"


@user1.route('/init_submit', methods=['GET', 'POST'])
def init_submit():
    for userid in range(30):
        for _ in range(10):
            date1 = date(random.randint(2016,2020),random.randint(1,12),random.randint(1,28))
            submit = Submit(project_id=random.randint(1,30),
                            uploader_id=userid,
                            submit_time=date1,
                            star_rating=random.randint(1,5),
                            estimation_content="评价内容",
                            estimation_time=date1+datetime.timedelta(14))
            db.session.add(submit)
            db.session.commit()
        print("用户"+str(userid)+"已完成提交数据初始化")
        notifications = Notification.query.filter_by(
                            user_id=userid,
                            notification_type=0).all()
        submits = Submit.query.filter_by(
                            uploader_id=userid,
                            ).all()
        for _ in range(len(notifications)):
            notifications[_].notification_content=str(submits[_].submit_id)
            notifications[_].notification_time=submits[_].estimation_time
    return "已完成提交初始化"


@user1.route('/init_visual',methods=['GET','POST'])
def init_visual():
    project_id = 1011
    uploader_id = 4041
    data_dict = {'组员': {'type': DataType.CATEGORY, '类别': ['丁一', '李四']},
                 '心情指数': {'type': DataType.INT, 'min': '1', 'max': '100'},
                 '星期': {'type': DataType.CATEGORY, '类别': ['周一', '周二', '周三', '周四']},
                 '室温': {'type': DataType.INT, 'min': '1', 'max': '40'}}
    project = Project(project_id=project_id, data_format=json.dumps(data_dict), project_title='小组观察计划')
    db.session.add(project)
    submit_id = 20011
    data_id = 10011
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='丁一')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周一')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='50')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='14')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='丁一')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周二')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='70')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='27')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='丁一')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周三')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='22')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='29')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='丁一')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周四')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='88')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='23')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='李四')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周一')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='23')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='30')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='李四')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周二')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='7')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='25')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='李四')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周三')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='88')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='10')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)

    submit_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='组员', cata_value='李四')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.CATEGORY, data_title='星期', cata_value='周四')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='心情指数', int_value='34')
    db.session.add(data)
    data_id += 1
    data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.INT, data_title='室温', int_value='23')
    db.session.add(data)
    data_id += 1
    submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
    db.session.add(submit)
    visual = Visualization(display_id=111, project_id=project_id, is_display=1, figure_type='scatter', visual_type=2,
                           figure_title='aaa', x_label='心情指数', y_label='室温',
                           y_data_title='室温', x_data_title='心情指数', y_rangeH='dataMax',
                           y_rangeL='dataMin', x_rangeH='dataMax', x_rangeL='dataMin')
    db.session.add(visual)
    db.session.commit()
    print('init')
    return "可视化初始化成功"


