import unittest
from velvet_dawn.dao import app, db


class BaseTest(unittest.TestCase):

    def setUp(self) -> None:
        with app.app_context():
            db.drop_all()
            db.create_all()
