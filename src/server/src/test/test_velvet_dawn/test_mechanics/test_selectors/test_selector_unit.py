import velvet_dawn.map.creation
from velvet_dawn.dao import app
from velvet_dawn.models import Tile
from test.base_test import BaseTest
from velvet_dawn.mechanics import selectors


class TestUnitSelectors(BaseTest):

    def test_selector_unit(self):
        with app.app_context():
            self.setup_game()

            tile = velvet_dawn.map.get_tile(15, 0)
            selector = selectors.get_selector(tile.tile_id, Tile, "unit")

            # Test one unit is loaded, placed in the setup
            self.assertEqual(1, len(selector.get_selection(tile, self.get_test_config())))
            self.assertTrue(selector.function_equals(tile, "testing:commander", self.get_test_config()))

            # check attr options
            selector = selectors.get_selector(tile.tile_id, Tile, "unit.movement.range")
            unit = velvet_dawn.units.list()[0]
            self.assertEqual(2, unit.get_attribute("movement.range", _type=int))
            selector.function_add(tile, 2, self.get_test_config())
            self.assertEqual(4, unit.get_attribute("movement.range", _type=int))
            selector.function_subtract(tile, 10, self.get_test_config())
            self.assertEqual(-6, unit.get_attribute("movement.range", _type=int))
            selector.function_multiply(tile, 5, self.get_test_config())
            self.assertEqual(-30, unit.get_attribute("movement.range", _type=int))
            selector.function_set(tile, "example", self.get_test_config())
            self.assertTrue(selector.function_equals(tile, "example", self.get_test_config()))
