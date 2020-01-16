import os
import json
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app.main.forms import FacebookChatUpload
from app.main import bp
from app.classes import Person, Reaction, ReactCounter
from app. helper import react_classifier, react_compare
from werkzeug.utils import secure_filename
from flask_googlecharts import GoogleCharts


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    form = FacebookChatUpload()
    if form.validate_on_submit():
        filenames = []
        names = request.files.getlist(form.json_facebook_file.name)
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
    list_of_people = []
    list_results = []
    messages = []
    react_types = ['thumbs_up', 'angry', 'wow', 'laugh', 'cry', 'heart']
    for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)) as json_file:
            stringdata = json.load(json_file)
            data = json.loads(stringdata)
            participants = data["participants"]
            messages = messages + data['messages']
            # getting list of participants across all files.
            for member in participants:
                list_of_people.append(member.get('name'))
            list_of_people = list(set(list_of_people))
    for person in list_of_people:
        profile = Person(person)
        list_results.append(profile)
    # looping over messages in n^2 :<
    for message in messages:
        for each in list_results:
            if message.get('sender_name') in each.id:
                if message.get('content'):
                    # updating how many messages were sent
                    each.up_comments()
                    reacts = message.get('reactions')
                    temp_counter = ReactCounter()
                    if reacts:
                        for react in reacts:
                            cur_react = react_classifier(react.get('reaction'))
                            temp_counter.add_count(cur_react)
                            # update number of reacts received
                            y = getattr(each, cur_react)
                            y.up_received()
                            # updating how many reacts someone has sent
                            for listee in list_results:
                                if react.get('actor') in listee.id:
                                    actor_react = getattr(listee, cur_react)
                                    actor_react.up_given()
                    for each_type in react_types:
                        # setting new top comment for each react type
                        if react_compare(each, temp_counter, each_type):
                            x = getattr(getattr(each, each_type))
                            setattr(x, 'top_comment', message.get('content'))
                else:
                    # update how many messages were deleted
                    each.up_deleted()
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    # Feeding Data into Google Charts

    return render_template('readme.html', title='Your Chat')
