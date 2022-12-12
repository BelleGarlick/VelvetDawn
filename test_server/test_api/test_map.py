import unittest

import velvet_dawn.entities
from server.app import app, config


class TestEntitiesApi(unittest.TestCase):
    def test_get_entities(self):
        velvet_dawn.map.tiles.initialise(config)

        with app.test_client() as client:
            results = client.get("/map/tiles/").json

            # Check results have loaded
            self.assertGreater(len(results), 0)

            # TODO Test tile attributes when there are some
