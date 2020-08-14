1) 创建虚拟环境  python3 -m venv venv
2) 激活虚拟环境 . venv/bin/activate
3) 将后端代码的路径加入全局变量 export FLASK_APP=manage.py
4) 运行后端:  flask run
5) 用python运行后端  python3 manage.py
6) 查询  netstat -lntp
7) 关闭  Uwsgi --stop <查到的 pid> 或 sudo kill <查到的 pid>
8) 用uwsgi跑  uwsgi --ini myproject.ini
9) 看日志  cat log/mylog.log
