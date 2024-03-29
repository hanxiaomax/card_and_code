#coding:utf-8
import os

basedir=os.path.abspath(os.path.dirname(__file__))#get basedir of the project

WTF_CSRF_ENABLED = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#for database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#for upload pic
UPLOAD_FOLDER = basedir+'/app/static/uploads/' #should use basedir
MAX_CONTENT_LENGTH=2*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])#TODO:make user aware

#for qrcodes
QRCODES_FOLDER = basedir+'/app/static/qrcodes/' #should use basedir
