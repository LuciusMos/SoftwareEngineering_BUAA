import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'ball-ball-you-do-not-attack-me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'CitizenScience.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:zjanb@localhost:3306/CitizenScience'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'CitizenScience_db_repo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['17373157@buaa.edu.cn']

    OPERATIONS_PER_PAGE = 6
    '''