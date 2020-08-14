from models import *

project_id = 1
uploader_id = 404
data_dict = {'组员': {'type': DataType.CATEGORY, '类别': ['丁一', '李四']},
             '心情指数': {'type': DataType.INT, 'min': '1', 'max': '100'},
             '星期': {'type': DataType.CATEGORY, '类别': ['周一', '周二', '周三', '周四']},
             '室温': {'type': DataType.INT, 'min': '1', 'max': '40'}}
project = Project(project_id=project_id, data_format=json.dumps(data_dict), project_title='小组观察计划')
db.session.add(project)
submit_id = 2001
data_id = 1001
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
visual = Visualization(display_id=111, project_id=1, is_display=1, figure_type='line', visual_type=2,
                       figure_title='aaa', x_label='心情指数', y_label='室温',
                       y_data_title='室温', x_data_title='心情指数', cata_data_title='星期', y_rangeH='dataMax',
                       y_rangeL='dataMin', x_rangeH='dataMax', x_rangeL='dataMin')
db.session.add(visual)
db.session.commit()
print('init')
