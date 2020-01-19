import logging
import os
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

    return app

