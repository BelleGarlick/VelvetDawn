import unittest

import velvet_dawn
from server.app import app, config


class TestEntitiesApi(unittest.TestCase):
    def test_get_entities(self):
        velvet_dawn.datapacks.init(config)

        with app.test_client() as client:
            results = client.get("/entities/").json

            # Check results have loaded
            self.assertGreater(len(results), 0)

            # Get the musketeers
            musketeers = None
            for result in results:
                if result['name'] == 'Musketeers':
                    musketeers = result

            # Test that it's loading correctly
            self.assertEqual(25, musketeers['combat']['damage'])
