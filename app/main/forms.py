from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, MultipleFileField
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename


class FacebookChatUpload(FlaskForm):
    json_facebook_file = MultipleFileField('Message Files')
    submit = SubmitField('Upload Files')
