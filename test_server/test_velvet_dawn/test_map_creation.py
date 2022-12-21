import velvet_dawn
from config import Config
from velvet_dawn.dao import app
from test_server.base_test import BaseTest


class TestMapCreation(BaseTest):
    def test_map_creation(self):
        with app.app_context():
            velvet_dawn.map.new(Config().set_map_size(5, 5))
            pass
