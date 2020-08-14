from models import *

project_id = 222
uploader_id = 404
data_dict = {'城市': {'type': DataType.MAP}}
project = Project(project_id=project_id, data_format=json.dumps(data_dict), project_title='城市空气质量统计')
db.session.add(project)
submit_id = 201
data_id = 101
data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.MAP, data_title='城市', map_value='浙江省/舟山市')
db.session.add(data)
submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
data_id += 1
db.session.add(submit)

submit_id += 1
data = Data(data_id=data_id, submit_id=submit_id, data_type=DataType.MAP, data_title='城市', map_value='四川省/成都市')
db.session.add(data)
submit = Submit(submit_id=submit_id, project_id=project_id, uploader_id=uploader_id)
data_id += 1
db.session.add(submit)

db.session.commit()
print('init2')
