import os
basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI ='mysql://root:root@127.0.0.1:3306/flasky_test'
UPLOADED_PHOTOS_DEST = basedir + '/static/img'