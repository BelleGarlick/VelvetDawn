import unittest
from abc import ABC

import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.dao import app, db
from velvet_dawn.dao.models import UnitInstance


class BaseTest(unittest.TestCase, ABC):

    def get_test_config(self):
        config = Config()
        config.datapacks = ['__testing__', 'civil-war']
        return config

    def setup_game(self):
        with app.app_context():
            config = self.get_test_config()
            config.seed = 0
            velvet_dawn.datapacks.init(config)
            velvet_dawn.map.creation.new(config)
            velvet_dawn.players.join("player1", "")
            velvet_dawn.players.join("player2", "")
            velvet_dawn.game.setup.update_setup("testing:commander", 1)
            velvet_dawn.game.setup.update_setup("civil-war:commander", 1)
            velvet_dawn.game.setup.update_setup("civil-war:cavalry", 1)
            velvet_dawn.game.phase.start_setup_phase(config)
            velvet_dawn.game.setup.place_entity("player1", "testing:commander", 15, 0, config)
            velvet_dawn.game.setup.place_entity("player1", "civil-war:cavalry", 14, 0, config)
            velvet_dawn.game.setup.place_entity("player2", "testing:commander", 15, config.map_height - 1, config)
            velvet_dawn.game.phase.start_game_phase(config)

            db.session.query(UnitInstance)\
                .where(UnitInstance.x == 15, UnitInstance.y == config.map_height - 1)\
                .update({
                    UnitInstance.y: 2
                })
            db.session.commit()

    def get_config(self):
        config = Config()
        config.datapacks = ['__testing__', 'civil-war']
        config.map_height = 11
        config.map_width = 7
        config.spawning.width_multiplier = 1
        config.spawning.neighbours_multiplier = 1
        config.spawning.width_addition = 1
        return config

    def prepare_game(self):
        with app.app_context():
            config = self.get_config()
            config.seed = 0
            velvet_dawn.datapacks.init(config)
            velvet_dawn.map.creation.new(config)
            velvet_dawn.players.join("player1", "")
            velvet_dawn.players.join("player2", "")
            velvet_dawn.game.setup.update_setup("testing:commander", 1)
            velvet_dawn.game.setup.update_setup("testing:upgradable", 1)
            velvet_dawn.game.phase.start_setup_phase(config)
            velvet_dawn.game.setup.place_entity("player1", "testing:commander", 5, 0, config)
            velvet_dawn.game.setup.place_entity("player1", "testing:upgradable", 4, 0, config)
            velvet_dawn.game.setup.place_entity("player2", "testing:commander", 5, config.map_height - 1,
                                                config)
            velvet_dawn.game.phase.start_game_phase(config)

            db.session.query(UnitInstance) \
                .where(UnitInstance.x == 4, UnitInstance.y == config.map_height - 1) \
                .update({
                    UnitInstance.y: 2
                })
            db.session.commit()

    def setUp(self) -> None:
        with app.app_context():
            db.drop_all()
            db.create_all()
