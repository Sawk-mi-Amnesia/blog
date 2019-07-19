import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/blog?charset=utf8'
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True