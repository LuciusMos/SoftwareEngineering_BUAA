from flask import Flask, request, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES,configure_uploads,patch_request_class
from backend.upload import profile, photo, feedback, proofphoto, dataimage
import os

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db = SQLAlchemy(app)

    file_url = "/home/CitizenScience/file"
    file_dir = "image"

    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(file_url, file_dir)

    from backend.init import user1
    app.register_blueprint(user1)

    from backend.user import user
    app.register_blueprint(user)

    from backend.identity import ident
    app.register_blueprint(ident)

    from backend.project import proj
    app.register_blueprint(proj)

    from backend.homepage import hp
    app.register_blueprint(hp)

    from backend.visualization import vis
    app.register_blueprint(vis)

    from backend.app import admin,projectmainimage
    app.register_blueprint(admin)

    configure_uploads(app, profile)
    configure_uploads(app, photo)
    configure_uploads(app, feedback)
    configure_uploads(app, proofphoto)
    configure_uploads(app, projectmainimage)
    configure_uploads(app, dataimage)

    patch_request_class(app)

    return app


