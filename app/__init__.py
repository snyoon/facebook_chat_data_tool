import logging
import os
import boto3
from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_googlecharts import GoogleCharts
from config import Config
from flask_s3 import FlaskS3

bootstrap = Bootstrap()
moment = Moment()
charts = GoogleCharts()
flasks3 = FlaskS3()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    moment.init_app(app)
    charts.init_app(app)
    flasks3.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/facebookchatdatatool.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('facebook-chat-data-tool start up')
    return app
