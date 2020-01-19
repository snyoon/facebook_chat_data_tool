import os
import json
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app.main.forms import FacebookChatUpload
from app.main import bp
from app.classes import Person, Reaction, ReactCounter
from app.helper import react_classifier, react_compare, react_chart_row_filler
from werkzeug.utils import secure_filename
import boto3


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    # s3 = boto3.client(
    #     "s3",
    #     aws_access_key_id=current_app.config['ACCESS_KEY'],
    #     aws_secret_access_key=current_app.config['SECRET_ACCESS_KEY']
    # )
    # bucket_resource = s3
    form = FacebookChatUpload()
    if form.validate_on_submit():
        filenames = []
        names = request.files.getlist(form.json_facebook_file.name)
        for file in form.json_facebook_file.data:
            # kicks out if files is not json (very weak)
            if 'json'not in str(file.filename):
                return redirect(url_for('main.readme'))
            file_names = secure_filename(file.filename)
            bleh = file.stream.read()
            stringbleh = bleh.decode("utf-8")
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], file_names), 'w+') as json_file:
                json.dump(stringbleh, json_file)
            # bucket_resource.upload_file(
            #     Bucket=current_app.config['FLASKS3_BUCKET_NAME'],
            #     Filename=os.path.join(current_app.config['UPLOAD_FOLDER'], file_names),
            #     Key=str(current_app.config['RANDOM_DIRECTORY'])+'/'+file_names
            # )

        return redirect(url_for('main.results'))
    return render_template('home.html', title='Home', form=form)


@bp.route('/readme', methods=['GET', 'POST'])
def readme():
    return render_template('readme.html', title='How to Use')


@bp.route('/results', methods=['GET', 'POST'])
def results():
    list_of_people = []
    list_results = []
    messages = None
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
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    for person in list_of_people:
        profile = Person(person)
        list_results.append(profile)
    # looping over messages in n^2 :<
    for message in messages:
        for each in list_results:
            if message.get('sender_name') in each.id:
                if message.get('content') or message.get('photos') or message.get('videos') or message.get(
                        'gifs') or message.get('sticker') or message.get('audio_files') or message.get('files'):
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

    # os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    member_values = []
    heart_values = []
    laugh_values = []
    wow_values = []
    cry_values = []
    angry_values = []
    thumbs_up_values = []
    thumbs_down_values = []
    pie_delete_values = []
    pie_messages_values = []
    for each in list_results:
        member_values.append(each.id)
        heart_values.append(each.heart.num_received)
        laugh_values.append(each.laugh.num_received)
        wow_values.append(each.wow.num_received)
        cry_values.append(each.cry.num_received)
        angry_values.append(each.angry.num_received)
        thumbs_up_values.append(each.thumbs_up.num_received)
        thumbs_down_values.append(each.thumbs_down.num_received)
        pie_delete_values.append(each.num_deleted)
        pie_messages_values.append(each.num_comments)

    return render_template('result.html', title='Your Chat', member_values=member_values, heart_values=heart_values,
                           laugh_values=laugh_values, wow_values=wow_values, cry_values=cry_values,
                           angry_values=angry_values, thumbs_up_values=thumbs_up_values,
                           thumbs_down_values=thumbs_down_values, pie_messages_values=pie_messages_values,
                           pie_delete_values=pie_delete_values, len=len(member_values))
