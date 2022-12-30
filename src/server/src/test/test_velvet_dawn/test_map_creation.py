import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.dao import app
from test.base_test import BaseTest


class TestMapCreation(BaseTest):
    def test_map_creation(self):
        with app.app_context():
            config = Config().set_map_size(20, 20)
            config.seed = 79221
            config.datapacks = ['civil-war']

            velvet_dawn.datapacks.init(config)
            velvet_dawn.map.new(config)
