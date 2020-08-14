from flask import Flask, request, jsonify
from flask_cors import *
from backend.models import *
from sqlalchemy import func
import backend.visualcity
import time
import os
import sys

# from models import *

# 跨域解决方案
CORS(app, supports_credentials=True)

vis = Blueprint("visual", __name__)


# @vis
@vis.route('/get_data_ops', methods=['GET', 'POST'])
def get_data_ops():
    if request.method == 'POST':
        datax = request.form.to_dict()
        project_id = datax.get('project_id')
        project = Project.query.filter_by(project_id=project_id).first()
        data_format = json.loads(project.data_format)
        keys = data_format.keys()
        xData_ops = []
        yData_ops = []
        cataData_ops = []
        mapData_ops = []
        for key in keys:
            value = data_format[key]
            if value['type'] == DataType.INT or value['type'] == DataType.FLOAT or value['type'] == DataType.CATEGORY:
                xData_ops.append({"value": key, "label": key})
            if value['type'] == DataType.INT or value['type'] == DataType.FLOAT:
                yData_ops.append({"value": key, "label": key})
            if value['type'] == DataType.CATEGORY:
                cataData_ops.append({"value": key, "label": key})
            if value['type'] == DataType.MAP:
                mapData_ops.append({"value":key,"label":key})
        data_ops = {'xData_ops': xData_ops, 'yData_ops': yData_ops, 'cataData_ops': cataData_ops,'mapData_ops':mapData_ops}
        # data_ops = {'xData_ops': xData_ops, 'yData_ops': yData_ops, 'cataData_ops': cataData_ops}
        xx = json.dumps(data_ops)
        return xx


@vis.route('/get_visual_data', methods=['GET', 'POST'])
def get_visual_data():
    if request.method == 'POST':
        datax = request.form.to_dict()
        project_id = datax.get('project_id')
        x_data_title = datax.get('x_data_title')
        y_data_title = datax.get('y_data_title')
        cata_data_title = datax.get('cata_data_title')
        map_data_title = datax.get('map_data_title')
        visual_type = int(datax.get('visual_type'))
        figure_type = datax.get('figure_type')
        submits = Submit.query.filter_by(project_id=project_id).all()
        x_data = []
        y_data = []
        x_types = []
        cata_data = []
        visual_data = {}
        if figure_type == 'map':
            listdata = []
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_type=DataType.MAP,data_title=map_data_title).all())
                for data in listdata:
                    local = data.map_value.split('/')[1]
                    if visual_data.get(local) is None:
                        visual_data[local] = {'value': 0, 'name': local}
                    visual_data[local]['value'] += 1
        elif visual_type == VisualType.SHOWVISUAL:
            listdata = []
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_title=cata_data_title).all())
                for data in listdata:
                    cate = data.cata_value
                    if visual_data.get(cate) is None:
                        visual_data[cate] = {'value': 0, 'name': cate}
                    visual_data[cate]['value'] += 1
        else:
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                submit_id = submit.submit_id
                x_line = Data.query.filter_by(submit_id=submit_id, data_title=x_data_title).first()
                if x_line is None or (
                        x_line.int_value is None and x_line.float_value is None and x_line.cata_value is None):
                    continue
                if x_line.int_value is not None:
                    x_data.append(x_line.int_value)
                elif x_line.float_value is not None:
                    print("I'm here:A")
                    x_data.append(x_line.float_value)
                elif x_line.cata_value is not None:
                    x_data.append(x_line.cata_value)
                y_line = Data.query.filter_by(submit_id=submit_id, data_title=y_data_title).first()
                if y_line is None or (
                        y_line.int_value is None and y_line.float_value is None and y_line.cata_value is None):
                    x_data.pop()
                    continue
                if y_line.int_value is not None:
                    y_data.append(y_line.int_value)
                elif y_line.float_value is not None:
                    print("I'm here:A")
                    y_data.append(y_line.float_value)
                elif y_line.cata_value is not None:
                    y_data.append(y_line.cata_value)
                if cata_data_title != "":
                    cata_line = Data.query.filter_by(submit_id=submit_id, data_title=cata_data_title).first()
                    if cata_line is None:
                        continue
                    if cata_line.cata_value is not None:
                        cata_data.append(cata_line.cata_value)
            if visual_type == VisualType.COMPAREVISUAL:
                if cata_data_title != "":
                    for i in range(len(x_data)):
                        if visual_data.get(cata_data[i]) is None:
                            visual_data[cata_data[i]] = []
                        visual_data[cata_data[i]].append({'value': y_data[i], 'name': x_data[i]})
                        if x_data[i] not in x_types:
                            x_types.append(x_data[i])
                else:
                    visual_data[y_data_title] = []
                    for i in range(len(x_data)):
                        visual_data[y_data_title].append({'value': y_data[i], 'name': x_data[i]})
            elif visual_type == VisualType.DATAVISUAL:
                if cata_data_title != "":
                    for i in range(len(x_data)):
                        if visual_data.get(cata_data[i]) is None:
                            visual_data[cata_data[i]] = []
                        visual_data[cata_data[i]].append([x_data[i], y_data[i]])
                    for k in visual_data.keys():
                        visual_data[k].sort(key=lambda x: x[0])
                else:
                    visual_data[y_data_title] = []
                    for i in range(len(x_data)):
                        visual_data[y_data_title].append([x_data[i], y_data[i]])
                    for k in visual_data.keys():
                        visual_data[k].sort(key=lambda x: x[0])
        print("I'm here:C")
        print(visual_data)
        myLengends = list(visual_data.keys())
        myVisualData = list(visual_data.values())
        if figure_type == 'map':
            myVisualData = backend.visualcity.convertData(myVisualData)
        my_data = {'myxAxis': x_types, 'mydata': myVisualData, 'mySize': len(myLengends), 'myLegends': myLengends}
        xx = json.dumps(my_data)
        print(my_data)
        return xx


@vis.route('/add_visualization', methods=['GET', 'POST'])
def add_visualization():
    import datetime
    if request.method == 'POST':
        datax = request.form.to_dict()
        project_id = datax.get('project_id')
        is_display_str = datax.get('is_display')
        is_display = False
        if is_display_str == "1":
            is_display = True
        figure_type = datax.get('figure_type')
        visual_type = datax.get('visual_type')
        figure_title = datax.get('figure_title')
        x_label = datax.get('x_label')
        y_label = datax.get('y_label')
        x_data_title = datax.get('x_data_title')
        y_data_title = datax.get('y_data_title')
        map_data_title = datax.get('map_data_title')
        cata_data_title = datax.get('cata_data_title')
        x_rangeL = datax.get('x_rangeL')
        x_rangeH = datax.get('x_rangeH')
        y_rangeL = datax.get('y_rangeL')
        y_rangeH = datax.get('y_rangeH')
        visual = Visualization(project_id=project_id, is_display=is_display, figure_title=figure_title,
                               figure_type=figure_type, visual_type=visual_type, cata_data_title=cata_data_title,
                               map_data_title=map_data_title,create_time=datetime.datetime.now(),
                               x_label=x_label, x_data_title=x_data_title, x_rangeH=x_rangeH, x_rangeL=x_rangeL,
                               y_label=y_label, y_data_title=y_data_title, y_rangeH=y_rangeH, y_rangeL=y_rangeL)
        db.session.add(visual)
        db.session.commit()
        if is_display and figure_type == 'map':
            visual_data = {}
            display_id = visual.display_id
            submits = Submit.query.filter_by(project_id=project_id).all()
            listdata = []
            for submit in submits:
                listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_type=DataType.MAP,data_title=map_data_title).all())
                for data in listdata:
                    local = data.map_value.split('/')[1]
                    if visual_data.get(local) is None:
                        visual_data[local] = {'value': 0, 'name': local}
                    visual_data[local]['value'] += 1
            map_data=[]
            for v in visual_data.values():
                map_data.append([v['name'],v['value']])
            # map_data = visual_data.values()
            figure_url = generate_geo_png(map_data, x_rangeH, x_rangeL, figure_title, display_id,map_data_title)  # 调用
            visual.figure_url = figure_url
            db.session.commit()
    return "success"


def generate_geo_png(geodata, geomax, geomin, geotitle, display_id,map_data_title):
    from pyecharts import options as opts
    from pyecharts.charts import Map, Geo
    from pyecharts.render import make_snapshot
    # from pyecharts_snapshot.main import make_a_snapshot
    from snapshot_selenium import snapshot
    geo = Geo()
    geo.add_coordinate_json('/home/CitizenScience/backend/backend/geoCoordJson.js')
    geo.add_schema(maptype="china")
    print(geodata)
    print(map_data_title)
    geo.add(" ", geodata, symbol_size=10)
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=geomax, min_=geomin))
    figure_url = "/home/CitizenScience/file/visualization/" + str(display_id) + '_geo.png'
    # figure_url = str(display_id) + '_geo.png'
    make_snapshot(snapshot, geo.render(), figure_url, 2)
    # geo.render(path='render.html')
    # cmd = "snapshot render.html png"
    # try:
    #    isRun = os.system(cmd)
    #    print("截图完成")
    # except:
    #    print("截图失败")
    # cmd = "mv output.png ../file/visualization/{}".format(figure_url)
    # try:
    #     isRun = os.system(cmd)
    #    print("移动完成")
    # except:
    #     print("移动失败")

    # make_a_snapshot('geo2.html', 'geo3.png')
    return figure_url

@vis.route('/update_map', methods=['GET', 'POST'])
def update_map():
    import os
    if request.method == 'POST':
        datax = request.form.to_dict()
        display_id = datax.get('display_id')
        project_id = datax.get('project_id')
        visual_data = {}
        submits = Submit.query.filter_by(project_id=project_id).all()
        visual = Visualization.query.filter_by(display_id=display_id).first()
        map_data_title=visual.map_data_title
        listdata = []
        for submit in submits:
            if submit.star_rating == 0:
                continue
            listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_type=DataType.MAP,data_title=map_data_title).all())
            for data in listdata:
                local = data.map_value.split('/')[1]
                if visual_data.get(local) is None:
                    visual_data[local] = {'value': 0, 'name': local}
                visual_data[local]['value'] += 1
        map_data=[]
        for v in visual_data.values():
            map_data.append([v['name'],v['value']])
        if os.path.exists("/home/CitizenScience/file/visualization/" + str(display_id) + '_geo.png'):
            os.remove("/home/CitizenScience/file/visualization/" + str(display_id) + '_geo.png')
        
        x_rangeH = visual.x_rangeH
        x_rangeL = visual.x_rangeL
        figure_title = visual.figure_title
        generate_geo_png(map_data, x_rangeH, x_rangeL, figure_title, display_id,map_data_title)  # 调用
        return "success"



@vis.route('/get_my_visual_research', methods=['GET', 'POST'])
def get_my_visual_research():
    if request.method == 'POST':
        cu = User.get_id_name(request.headers.get('token'))
        if cu is None:
            return "networkError"
        ups1 = UserProject.query.filter_by(user_id=cu['id'], user_identity=UserIdentity.SCIENTIST).all()
        ups2 = UserProject.query.filter_by(user_id=cu['id'], user_identity=UserIdentity.ASSISTANT).all()
        ups = ups1 + ups2
        ups = list(set(ups))
        mydata = []
        ftmap = {'map': '地图', 'bar': '柱状图', 'line': '折线图', 'pie': '扇形图', 'scatter': '散点图'}
        for up in ups:
            project = Project.query.filter_by(project_id=up.project_id).first()
            visuals = Visualization.query.filter_by(project_id=up.project_id).all()
            for v in visuals:
                mydata.append({'project_id': v.project_id,
                               'display_id': v.display_id,
                               'visual_type': v.visual_type,
                               'figure_title': v.figure_title,
                               'figure_type': ftmap[v.figure_type],
                               'x_label': v.x_label,
                               'y_label': v.y_label,
                               'x_data_title': v.x_data_title,
                               'y_data_title': v.y_data_title,
                               'cata_data_title': v.cata_data_title,
                               'map_data_title':v.map_data_title, #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!前端记得改这
                               'x_rangeL': v.x_rangeL,
                               'y_rangeL': v.y_rangeL,
                               'x_rangeH': v.x_rangeH,
                               'y_rangeH': v.y_rangeH,
                               'project_title': project.project_title,
                               'create_time':v.create_time.strftime('%Y-%m-%d')
                               })
        mydata = sorted(mydata,key=lambda keys:keys['display_id'],reverse=True)
        return json.dumps(mydata)


# 管理端预览
@vis.route('/get_visualization_each', methods=['GET', 'POST'])
def get_visualization_each():
    if request.method == 'POST':
        datax = request.form.to_dict()
        display_id = datax.get('display_id')
        visual = Visualization.query.filter_by(display_id=display_id).first()
        project_id = visual.project_id
        x_data_title = visual.x_data_title
        y_data_title = visual.y_data_title
        cata_data_title = visual.cata_data_title
        map_data_title = visual.map_data_title
        visual_type = int(visual.visual_type)
        figure_name = visual.figure_title
        figure_type = visual.figure_type
        xName = visual.x_label
        yName = visual.y_label
        xRangeL = visual.x_rangeL
        yRangeL = visual.y_rangeL
        xRangeH = visual.x_rangeH
        yRangeH = visual.y_rangeH
        submits = Submit.query.filter_by(project_id=project_id).all()
        x_data = []
        y_data = []
        x_types = []
        cata_data = []
        visual_data = {}
        if figure_type == 'map':
            listdata = []
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_type=DataType.MAP,data_title=map_data_title).all())
                for data in listdata:
                    local = data.map_value.split('/')[1]
                    if visual_data.get(local) is None:
                        visual_data[local] = {'value': 0, 'name': local}
                    visual_data[local]['value'] += 1
        elif visual_type == VisualType.SHOWVISUAL:
            listdata = []
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_title=cata_data_title).all())
                for data in listdata:
                    cate = data.cata_value
                    if visual_data.get(cate) is None:
                        visual_data[cate] = {'value': 0, 'name': cate}
                    visual_data[cate]['value'] += 1
        else:
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                submit_id = submit.submit_id
                x_line = Data.query.filter_by(submit_id=submit_id, data_title=x_data_title).first()
                if x_line is None or (
                        x_line.int_value is None and x_line.float_value is None and x_line.cata_value is None):
                    continue
                if x_line.int_value is not None:
                    x_data.append(x_line.int_value)
                elif x_line.float_value is not None:
                    x_data.append(x_line.float_value)
                elif x_line.cata_value is not None:
                    x_data.append(x_line.cata_value)
                y_line = Data.query.filter_by(submit_id=submit_id, data_title=y_data_title).first()
                if y_line is None or (
                        y_line.int_value is None and y_line.float_value is None and y_line.cata_value is None):
                    x_data.pop()
                    continue
                if y_line.int_value is not None:
                    y_data.append(y_line.int_value)
                elif y_line.float_value is not None:
                    y_data.append(y_line.float_value)
                elif y_line.cata_value is not None:
                    y_data.append(y_line.cata_value)
                if cata_data_title is not None:
                    cata_line = Data.query.filter_by(submit_id=submit_id, data_title=cata_data_title).first()
                    if cata_line is None:
                        continue
                    if cata_line.cata_value is not None:
                        cata_data.append(cata_line.cata_value)
            if visual_type == VisualType.COMPAREVISUAL:
                if cata_data_title is not None:
                    for i in range(len(x_data)):
                        if visual_data.get(cata_data[i]) is None:
                            visual_data[cata_data[i]] = []
                        visual_data[cata_data[i]].append({'value': y_data[i], 'name': x_data[i]})
                        if x_data[i] not in x_types:
                            x_types.append(x_data[i])
                else:
                    visual_data[y_data_title] = []
                    for i in range(len(x_data)):
                        visual_data[y_data_title].append({'value': y_data[i], 'name': x_data[i]})
            elif visual_type == VisualType.DATAVISUAL:
                if cata_data_title != "":
                    for i in range(len(x_data)):
                        if visual_data.get(cata_data[i]) is None:
                            visual_data[cata_data[i]] = []
                        visual_data[cata_data[i]].append([x_data[i], y_data[i]])
                    for k in visual_data.keys():
                        visual_data[k].sort(key=lambda x: x[0])
                else:
                    visual_data[y_data_title] = []
                    for i in range(len(x_data)):
                        visual_data[y_data_title].append([x_data[i], y_data[i]])
                    for k in visual_data.keys():
                        visual_data[k].sort(key=lambda x: x[0])
        myLengends = list(visual_data.keys())
        myVisualData = list(visual_data.values())
        if figure_type == 'map':
            myVisualData = backend.visualcity.convertData(myVisualData)
        my_data = {'myxAxis': x_types, 'mydata': myVisualData, 'mySize': len(myLengends), 'myLegends': myLengends,
                   'figure_name': figure_name, 'figure_type': figure_type, 'xName': xName, 'yName': yName,
                   'xRangeL': xRangeL,
                   'yRangeL': yRangeL, 'xRangeH': xRangeH, 'yRangeH': yRangeH}
        xx = json.dumps(my_data)
        print(my_data)
        return xx


@vis.route('/delete_visualization', methods=['GET', 'POST'])
def delete_visualization():
    if request.method == 'POST':
        datax = request.form.to_dict()
        display_id = datax.get('display_id')
        visual = Visualization.query.filter_by(display_id=display_id).first()
        if os.path.exists("/home/CitizenScience/file/visualization/" + str(display_id) + '_geo.png'):
            os.remove("/home/CitizenScience/file/visualization/" + str(display_id) + '_geo.png')
        db.session.delete(visual)
        db.session.commit()
        return "OK"


# APP
@vis.route('/get_all_visual', methods=['GET', 'POST'])
def get_all_visual():
    project_id = request.args.get('project_id')
    visuals = Visualization.query.filter_by(project_id=project_id).all()
    my_data = {}
    my_data['display_id'] = []
    my_data['myxAxis'] = []
    my_data['myVisualData'] = []
    my_data['mySize'] = []
    my_data['myLegends'] = []
    my_data['figure_name'] = []
    my_data['figure_type'] = []
    my_data['xName'] = []
    my_data['yName'] = []
    my_data['xRangeL'] = []
    my_data['xRangeH'] = []
    my_data['yRangeL'] = []
    my_data['yRangeH'] = []
    my_data['figure_url'] = []
    for visual in visuals:
        if visual.is_display == 0:
            continue
        figure_type = visual.figure_type
        # if figure_type == 'map':
        #    figure_urls.append(visual.figure_url)
        #    continue
        display_id = visual.display_id
        x_data_title = visual.x_data_title
        y_data_title = visual.y_data_title
        cata_data_title = visual.cata_data_title
        visual_type = int(visual.visual_type)
        figure_name = visual.figure_title
        xName = visual.x_label
        yName = visual.y_label
        xRangeL = visual.x_rangeL
        yRangeL = visual.y_rangeL
        xRangeH = visual.x_rangeH
        yRangeH = visual.y_rangeH
        figure_url = visual.figure_url
        if figure_url is None:
            figure_url = '-'
        submits = Submit.query.filter_by(project_id=project_id).all()
        x_data = []
        y_data = []
        x_types = []
        cata_data = []
        visual_data = {}
        if visual_type == VisualType.SHOWVISUAL:
            listdata = []
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                listdata.extend(Data.query.filter_by(submit_id=submit.submit_id, data_title=cata_data_title).all())
                for data in listdata:
                    cate = data.cata_value
                    if visual_data.get(cate) is None:
                        visual_data[cate] = {'value': 0, 'name': cate}
                    visual_data[cate]['value'] += 1
        else:
            for submit in submits:
                if submit.star_rating == 0:
                    continue
                submit_id = submit.submit_id
                x_line = Data.query.filter_by(submit_id=submit_id, data_title=x_data_title).first()
                if x_line is None or (
                        x_line.int_value is None and x_line.float_value is None and x_line.cata_value is None):
                    continue
                if x_line.int_value is not None:
                    x_data.append(x_line.int_value)
                elif x_line.float_value is not None:
                    x_data.append(x_line.float_value)
                elif x_line.cata_value is not None:
                    x_data.append(x_line.cata_value)
                y_line = Data.query.filter_by(submit_id=submit_id, data_title=y_data_title).first()
                if y_line is None or (
                        y_line.int_value is None and y_line.float_value is None and y_line.cata_value is None):
                    x_data.pop()
                    continue
                if y_line.int_value is not None:
                    y_data.append(y_line.int_value)
                elif y_line.float_value is not None:
                    y_data.append(y_line.float_value)
                elif y_line.cata_value is not None:
                    y_data.append(y_line.cata_value)
                if cata_data_title is not None:
                    cata_line = Data.query.filter_by(submit_id=submit_id, data_title=cata_data_title).first()
                    if cata_line is None:
                        continue
                    if cata_line.cata_value is not None:
                        cata_data.append(cata_line.cata_value)
            if visual_type == VisualType.COMPAREVISUAL:
                if cata_data_title is not None:
                    for i in range(len(x_data)):
                        if visual_data.get(cata_data[i]) is None:
                            visual_data[cata_data[i]] = []
                        visual_data[cata_data[i]].append({'value': y_data[i], 'name': x_data[i]})
                        if x_data[i] not in x_types:
                            x_types.append(x_data[i])
                else:
                    visual_data[y_data_title] = []
                    for i in range(len(x_data)):
                        visual_data[y_data_title].append({'value': y_data[i], 'name': x_data[i]})
            elif visual_type == VisualType.DATAVISUAL:
                if cata_data_title is not None:
                    for i in range(len(x_data)):
                        if visual_data.get(cata_data[i]) is None:
                            visual_data[cata_data[i]] = []
                        visual_data[cata_data[i]].append([x_data[i], y_data[i]])
                    for k in visual_data.keys():
                        visual_data[k].sort(key=lambda x: x[0])
                else:
                    visual_data[y_data_title] = []
                    for i in range(len(x_data)):
                        visual_data[y_data_title].append([x_data[i], y_data[i]])
                    for k in visual_data.keys():
                        visual_data[k].sort(key=lambda x: x[0])
        # for key,value in visual_data.items():
        #    visual_data[key] = str(value)
        myLengends = list(visual_data.keys())
        myVisualData = list(visual_data.values())
        # if figure_type == 'map':
        #     myVisualData = visualcity.convertData(myVisualData)
        my_data['display_id'].append(display_id)
        my_data['myxAxis'].append(x_types)
        my_data['myVisualData'].append(myVisualData)
        my_data['mySize'].append(len(myLengends))
        my_data['myLegends'].append(myLengends)
        my_data['figure_name'].append(figure_name)
        my_data['figure_type'].append(figure_type)
        my_data['xName'].append(xName)
        my_data['yName'].append(yName)
        my_data['xRangeL'].append(xRangeL)
        my_data['xRangeH'].append(xRangeH)
        my_data['yRangeL'].append(yRangeL)
        my_data['yRangeH'].append(yRangeH)
        my_data['figure_url'].append(figure_url)
    print(my_data)
    return my_data


if __name__ == '__main__':
    app.run(debug=True)
