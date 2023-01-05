import velvet_dawn.map.creation
from velvet_dawn.dao import app
from velvet_dawn.models import Unit
from test.base_test import BaseTest
from velvet_dawn.mechanics import selectors


class TestTileSelectors(BaseTest):

    def test_selector_tile(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "tile")

            # Test one unit is loaded, placed in the setup
            self.assertEqual(1, len(selector.get_selection(unit, self.get_test_config())))
            self.assertTrue(selector.function_equals(unit, "civil-war:shallow-water", self.get_test_config()))

            # check attr options
            selector = selectors.get_selector(unit.entity_id, Unit, "tile.movement.weight")
            tile = velvet_dawn.map.get_tile(15, 0)
            self.assertEqual(2, tile.get_attribute("movement.weight"))
            selector.function_add(unit, 3, self.get_test_config())
            self.assertEqual(5, tile.get_attribute("movement.weight"))
            selector.function_subtract(unit, 10, self.get_test_config())
            self.assertEqual(-5, tile.get_attribute("movement.weight"))
            selector.function_multiply(unit, 5, self.get_test_config())
            self.assertEqual(-25, tile.get_attribute("movement.weight"))
            selector.function_set(unit, "example", self.get_test_config())
            self.assertTrue(selector.function_equals(unit, "example", self.get_test_config()))
