import velvet_dawn
from velvet_dawn.dao import app
from test_server.base_test import BaseTest


class TestMapCreation(BaseTest):
    def test_map_creation(self):
        with app.app_context():
            velvet_dawn.map.creation.new(20, 13)
            pass
