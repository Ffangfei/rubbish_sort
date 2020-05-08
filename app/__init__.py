import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from config import basedir
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')
lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

#实例化 UploadSet 对象
photos = UploadSet('photos', IMAGES)
#将 app 的 config 配置注册到 UploadSet 实例 photos
configure_uploads(app, photos)


from app import views,models
