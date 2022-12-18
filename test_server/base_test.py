import unittest

import velvet_dawn.game.setup
from config import Config
from velvet_dawn.dao import app, db


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        test_config = Config(
            datapacks=['civil-war', 'gods']
        )
        velvet_dawn.datapacks.init(test_config)

    def setUp(self) -> None:
        with app.app_context():
            db.drop_all()
            db.create_all()
