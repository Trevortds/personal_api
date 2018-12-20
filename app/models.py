from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class State(db.Model):
    '''
    This table should only have one entry: my current state.
    id will always be 0
    '''
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(64))
    start_time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return "<State entry value: {}, start: {} >".format(self.value,self.start_time)


class CommuteTimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    departure_time = db.Column(db.DateTime(timezone=True))
    arrival_time = db.Column(db.DateTime(timezone=True))
    travel_time = db.Column(db.Integer)

    # maybe information from port authority twitter will go here one day
    twitter_delay = db.Column(db.Integer)

    # maybe google maps / osm info will go here some day
    maps_prediction = db.Column(db.Integer)

    model_prediction = db.Column(db.Float)

    def __repr__(self):
        return "<Commute time entry for {}, arrival: {}, travel time: {} >".format(self.departure_time,
                                                                                   self.arrival_time, self.travel_time)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        # don't worry, this workzeug function automatically adds a salt.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

    # class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     team = db.Column(db.String(64), index=True)
#     issue_id = db.Column(db.Integer, index=True)
#     user_name = db.Column(db.String(64), index=True)
#     value = db.Column(db.String(64))
#
#     def __repr__(self):
#         return "<{}'s Answer for {} issue {}>".format(self.user_name, self.team, self.issue_id)
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "team": self.team,
#             "issue_id": self.issue_id,
#             "user_name": self.user_name,
#             "value": self.value,
#         }
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     channel = db.Column(db.String(32), index= True, unique=True)
#     user_name = db.Column(db.String(64), index=True)
#     awaiting_response = db.Column(db.Boolean())
#     conversation = db.Column(db.String(1024))  # comma-separated list of issue ids
#
#     def __repr__(self):
#         return "<User {}>".format(self.user_name)
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "channel": self.channel,
#             "user_name": self.user_name,
#             "awaiting_response": self.awaiting_response,
#             "conversation": self.conversation.split(",") if self.conversation else [],
#         }
#
#
# class Issue(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     team = db.Column(db.String(64), index=True)
#     key = db.Column(db.String(64), index=True)
#     summary = db.Column(db.String(256))
#     url = db.Column(db.String(128))
#
#     def __repr__(self):
#         return "<{} Issue {}>".format(self.team, self.key)
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "team": self.team,
#             "key": self.key,
#             "summary": self.summary,
#             "url": self.url,
#         }

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# http://ondras.zarovi.cz/sql/demo/
