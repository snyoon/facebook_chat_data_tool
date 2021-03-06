import os
import random
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey'
    UPLOAD_FOLDER = os.path.join(basedir, 'tmp')
    FLASKS3_BUCKET_NAME = 'facebook-chat-data-tool-bucket'
    ACCESS_KEY = 'kek'
    SECRET_ACCESS_KEY = 'H/keke'
    RANDOM_DIRECTORY = random.randint(1,10000000)
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')