import os
import random
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey'
    UPLOAD_FOLDER = os.path.join(basedir, 'tmp')
    FLASKS3_BUCKET_NAME = 'facebook-chat-data-tool-bucket'
    ACCESS_KEY = 'AKIAIGHM2SS7UAA4A4YQ'
    SECRET_ACCESS_KEY = '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'
    RANDOM_DIRECTORY = random.randint(1,100000000)