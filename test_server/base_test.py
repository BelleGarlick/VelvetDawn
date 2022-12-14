import unittest

import velvet_dawn.game.setup
from config import Config
from dao.initialisation import app, db


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        test_config = Config(
            datapacks=['civil-war', 'gods']
        )
        velvet_dawn.resources.initialise(test_config)
        velvet_dawn.entities.initialise(test_config)
        velvet_dawn.map.tiles.initialise(test_config)

    def setUp(self) -> None:
        with app.app_context():
            db.drop_all()
            db.create_all()
