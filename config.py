import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey'
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'tmp')
    FLASKs3_BUCKET_NAME = 'facebook-chat-data-tool-bucket'
