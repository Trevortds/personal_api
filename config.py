import os

basedir = os.environ.get("DATA_DIR") or os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'ares-is-a-good-kitty'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

