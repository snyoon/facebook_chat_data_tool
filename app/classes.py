from flask import current_app


class Reaction:
    id = ''
    num_received = 0
    num_given = 0
    max_received = 0
    top_comment = ''

    def __repr__(self):
        return '<Reaction for {}>'.format(self.id)

    def __init__(self, name):
        self.id = name

    def up_received(self):
        self.num_received += 1

    def up_given(self):
        self.num_given += 1

    def max_update(self, number):
        self.max_received = number

    def update_top(self, string):
        self.top_comment = string


class Person:
    def __repr__(self):
        return '<Person  {}>'.format(self.id)

    def __init__(self, id):
        self.id = id
        self.heart = Reaction('heart')
        self.laugh = Reaction('laugh')
        self.cry = Reaction('cry')
        self.wow = Reaction('wow')
        self.angry = Reaction('angry')
        self.thumbs_up = Reaction('thumbs_up')
        self.thumbs_down = Reaction('thumbs_down')
        self.num_comments = 0
        self.num_deleted = 0

    def up_comments(self):
        self.num_comments += 1

    def up_deleted(self):
        self.num_deleted += 1


class ReactCounter:
    heart = 0
    laugh = 0
    cry = 0
    wow = 0
    angry = 0
    thumbs_up = 0
    thumbs_down = 0

    def __repr__(self):
        return '<ReactCounter>'

    def add_count(self, string):
        atr = getattr(self, string)
        atr += 1
