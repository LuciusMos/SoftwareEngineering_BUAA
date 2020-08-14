# import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

application = Flask(__name__)
application.config.from_object(Config)
database = SQLAlchemy(application)
migrate = Migrate(application, database)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
bootstrap = Bootstrap(application)
login_manager.login_message = '请先登录'
login_manager.login_message_category = "error"

'''
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   fromaddr=app.config['MAIL_USERNAME'],
                                   toaddrs=app.config['ADMINS'],
                                   subject='BankATM Failure', credentials=auth)
        # print(mail_handler.fromaddr, mail_handler.toaddrs)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        
        # 这里是SMTPHandler测试
        # 1. 需配置MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD可在：1)config.py赋值 2)环境变量配置
        # 2. 需在config.py中指定管理员邮箱ADMINS
        # try:
            # a = 1 / 0
        # except:
            # app.logger.error("SMTPHandler test", exc_info=True)
        

    logs_dir = os.path.join(Config.basedir, 'logs')
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    file_handler = RotatingFileHandler(os.path.join(logs_dir, 'BankATM.log'), maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    # 这里是RotatingFileHandler测试
    # app.logger.info('BankATM logging.handlers.RotatingFileHandler starts')
'''
