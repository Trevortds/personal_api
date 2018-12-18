import datetime
import json
import pytz

from app import app
from app import db
from app.models import State, CommuteTimeEntry


def get_state():
    return State.query.filter_by(id=0).first()


def update_state(new_value):
    old_state=State.query.get(0)
    if old_state:
        on_state_change(State.query.get(0).value, new_value)
    else:
        old_state = State(id=0)
    old_state.value = new_value
    old_state.start_time = datetime.datetime.now(pytz.utc)
    db.session.commit()
    return True


def on_state_change(old_value, new_value):
    """
    TODO write to toggl
    TODO send to commute model
    TODO trigger hue via ifttt
    TODO update slack status
    :param old_value:
    :param new_value:
    :return:
    """
    pass
