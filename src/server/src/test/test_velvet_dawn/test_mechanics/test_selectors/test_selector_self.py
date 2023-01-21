import velvet_dawn.map.creation
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.db.instances import WorldInstance
from velvet_dawn.mechanics import selectors


class TestSelfSelectors(BaseTest):

    def test_selector_self(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(5, 0)[0]
            tile = velvet_dawn.map.get_tile(5, 0)

            selector = selectors.get_selector(unit.entity_id, "self")

            self.assertEqual(unit.id, selector.get_selection(unit)[0].id)
            self.assertEqual(tile.id, selector.get_selection(tile)[0].id)
            self.assertTrue(WorldInstance() is selector.get_selection(WorldInstance())[0])
