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

    s3 = boto3.client(
        "s3",
        aws_access_key_id=Config.ACCESS_KEY,
        aws_secret_access_key=Config.SECRET_ACCESS_KEY
    )

    bucket_resource = s3

    return app
