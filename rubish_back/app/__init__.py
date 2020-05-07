from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from app.config import config
from flask_login import LoginManager
from app.database.mysql import db
from flask_caching import Cache
from app.controller import jwt_init

basedir = os.path.abspath(os.getcwd())

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__, static_folder=basedir + '/static')
app.config.from_object(config['default'])
config['default'].init_app(app)
cache.init_app(app)
jwt = jwt_init()
jwt.init_app(app)
db.init_app(app)

from app.handler import auth_blueprint

app.register_blueprint(auth_blueprint)

from app.handler import user_blueprint

app.register_blueprint(user_blueprint)

# app.logger.addHandler(consoleHandler)

# if __name__ != '__main__':
# gunicorn_logger = logging.getLogger('gunicorn.error')
# app.logger.handlers.extend(gunicorn_logger.handlers)
# app.logger.addHandler(fileHandler)
# app.logger.setLevel(gunicorn_logger.level)
