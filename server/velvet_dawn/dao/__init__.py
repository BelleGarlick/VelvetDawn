from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
db.init_app(app)


# noinspection PyUnresolvedReferences
from velvet_dawn.dao import models

with app.app_context():
    print(db)
    db.create_all()
