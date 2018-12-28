import logging
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

loglevel = os.environ.get("FLASK_LOGLEVEL")
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

logging.basicConfig(level=numeric_level)
app.logger.setLevel(numeric_level)

app.url_map.strict_slashes = False

login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "State": models.State, "CommuteTimeEntry": models.CommuteTimeEntry, "User": models.User}

# TODO add an authentication configuration website
