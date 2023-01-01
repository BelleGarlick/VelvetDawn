import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import velvet_dawn

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
db.init_app(app)


# noinspection PyUnresolvedReferences
from velvet_dawn.dao import models

with app.app_context():
    db.create_all()


def get_value(key: models.Keys, _type=None, default=None):
    value = db.session.query(models.KeyValues).get(key)
    if value:
        return velvet_dawn.utils.parse_type(value.value, _type, default)
    return default


def set_value(key: models.Keys, value):
    db.session.query(models.KeyValues).where(models.KeyValues.key == key).delete()
    db.session.add(models.KeyValues(key=key, value=value))
    db.session.commit()
