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
