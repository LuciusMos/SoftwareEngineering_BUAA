from migrate.versioning import api
from config import Config
from app import database
import os.path
database.create_all()
# if not os.path.exists(Config.SQLALCHEMY_MIGRATE_REPO):
# api.create(Config.SQLALCHEMY_MIGRATE_REPO, 'database_repository')
# api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
# else:
# print('Database already exists!')
