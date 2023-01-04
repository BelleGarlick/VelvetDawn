import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from os import remove

import velvet_dawn

db_path=Path(__file__).parent.parent.parent / "instance" / "game.db"
if db_path.exists():
    i = 0
    while i == 0:
        resume = input("A game alredy exists. Would you like to resume or start fresh?\nResume game = 0 (Default)\nStart Fresh = 1\nEnter your choice here: ")
        if resume == "1":
            print("Creating a new game...")
            remove(db_path)
            i = 1
        elif resume in ("0", ""):
            print("Resuming existing game...")
            i = 1
        else:
            print("\nImproper answer! Please choose from the available options or hit 'return' to accept the default option.\n\n")
    del i
else:
    print("Existing game not found, creating a new game...")

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
