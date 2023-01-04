import velvet_dawn.map.creation
from velvet_dawn.dao import app
from velvet_dawn.dao.models import UnitInstance
from velvet_dawn.models import Unit
from test.base_test import BaseTest
from velvet_dawn.mechanics import selectors


class TestSelfSelectors(BaseTest):

    def test_selector_self(self):
        with app.app_context():
            self.setup_game()

            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "self")

            # Test one unit is loaded, placed in the setup
            self.assertEqual(1, len(selector.get_selection(unit, self.get_test_config())))
            self.assertTrue(selector.function_equals(unit, "testing:commander", self.get_test_config()))

            # check attr options
            selector = selectors.get_selector(unit.entity_id, Unit, "self.health.max")
            self.assertEqual(100, unit.get_attribute("health.max", _type=int))
            selector.function_add(unit, 3, self.get_test_config())
            self.assertEqual(103, unit.get_attribute("health.max", _type=int))
            selector.function_subtract(unit, 10, self.get_test_config())
            self.assertEqual(93, unit.get_attribute("health.max", _type=int))
            selector.function_multiply(unit, 5, self.get_test_config())
            self.assertEqual(93 * 5, unit.get_attribute("health.max", _type=int))
            selector.function_set(unit, "example", self.get_test_config())
            self.assertTrue(selector.function_equals(unit, "example", self.get_test_config()))
