import os
basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:justformyself521@localhost:3306/rubbish'
UPLOADED_PHOTOS_DEST = basedir + '/static/img'