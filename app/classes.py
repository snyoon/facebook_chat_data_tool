from flask import current_app


class Reaction:
    id = ''
    num_received = 0
    num_given = 0
    max_received = 0
    top_comment = ''

    def __repr__(self):
        return '<Reaction for {}>'.format(self.id)

    def __init__(self, id):
        self.id = id

    def up_received(self):
        self.num_received = self.num_received + 1

    def up_given(self):
        self.num_given += 1

    def max_update(self, number):
        self.max_received = number

    def update_top(self, string):
        self.top_comment = string


class Person:
    id = ''
    heart = Reaction('heart')
    laugh = Reaction('laugh')
    cry = Reaction('cry')
    wow = Reaction('wow')
    angry = Reaction('angry')
    thumbs_up = Reaction('thumbs_up')
    thumbs_down = Reaction('thumbs_down')
    num_comments = 0
    num_deleted = 0

    def __repr__(self):
        return '<Person  {}>'.format(self.id)

    def __init__(self, id):
        self.id = id

    def up_comments(self):
        self.num_comments = self.num_comments + 1

    def up_deleted(self):
        self.num_deleted = self.num_deleted + 1


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
