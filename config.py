import os
basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wshwoaini@localhost:3306/rubbish'
SQLALCHEMY_ECHO = True
UPLOADED_PHOTOS_DEST = basedir + '/static/img'