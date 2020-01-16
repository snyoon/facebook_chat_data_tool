import os
import json
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app.main.forms import FacebookChatUpload
from app.main import bp
from werkzeug.utils import secure_filename


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    form = FacebookChatUpload()
    if form.validate_on_submit():
        filenames = []
        names = request.files.getlist(form.json_facebook_file.name)
        # for file in form.json_facebook_file.data:
        #     # filepath = os.path.join()
        #     bleh = file.stream.read()
        #
        #     print(bleh)
        #     file_names = secure_filename(file.filename)
        #     bleh.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_names))
        for file in form.json_facebook_file.data:
            file_names = secure_filename(file.filename)
            bleh = file.stream.read()
            stringbleh = bleh.decode("utf-8")
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], file_names), 'w+') as json_file:
                json.dump(stringbleh, json_file)
        return redirect(url_for('main.results'))
    return render_template('home.html', title='Home', form=form)


@bp.route('/readme', methods=['GET', 'POST'])
def readme():
    return render_template('readme.html', title='How to Use')


@bp.route('/results', methods=['GET', 'POST'])
def results():
    for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)) as json_file:
            stringdata = json.load(json_file)
            data = json.loads(stringdata)
            participants = data["participants"]
            for member


        #delete files after use
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return render_template('readme.html', title='Your Chat')