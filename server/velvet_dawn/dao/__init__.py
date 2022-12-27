from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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
        if not _type: return value.value
        elif _type == str: return value.value
        elif _type == float: return float(value.value)
        elif _type == int: return int(value.value)
    else:
        return default


def set_value(key: models.Keys, value):
    db.session.query(models.KeyValues).where(models.KeyValues.key == key).delete()
    db.session.add(models.KeyValues(key=key, value=value))
    db.session.commit()
