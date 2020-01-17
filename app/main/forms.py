from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, MultipleFileField
from flask_wtf.file import FileAllowed
from wtforms.validators import InputRequired
from flask_uploads import UploadSet
from werkzeug.utils import secure_filename

json = UploadSet('json', ['json'])


class FacebookChatUpload(FlaskForm):
    json_facebook_file = MultipleFileField('Message Files',
                                           validators=[InputRequired(), FileAllowed(json, 'JSON Chat files only')])
    submit = SubmitField('Upload Files')
