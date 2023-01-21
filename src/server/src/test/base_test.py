import unittest
from abc import ABC

import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.dao import app, db


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
            instance = velvet_dawn.game.setup.place_entity("player2", "testing:commander", 15, config.map_height - 1, config)
            velvet_dawn.game.phase.start_game_phase(config)

            velvet_dawn.db.units.move(instance, 15, 2)

    def get_config(self):
        config = Config()
        config.datapacks = ['__testing__']
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
            velvet_dawn.game.setup.update_setup("testing:abilitied", 1)
            velvet_dawn.game.phase.start_setup_phase(config)
            velvet_dawn.game.setup.place_entity("player1", "testing:commander", 5, 0, config)
            velvet_dawn.game.setup.place_entity("player1", "testing:upgradable", 4, 0, config)
            velvet_dawn.game.setup.place_entity("player1", "testing:abilitied", 6, 0, config)
            instance = velvet_dawn.game.setup.place_entity("player2", "testing:commander", 5, config.map_height - 1,
                                                config)
            velvet_dawn.game.phase.start_game_phase(config)

            velvet_dawn.db.units.move(instance, 5, 2)

    def setUp(self) -> None:
        velvet_dawn.db.instance.clear()
        with app.app_context():
            db.drop_all()
            db.create_all()
