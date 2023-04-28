import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.dao import app
from velvet_dawn.models.coordinate import Coordinate


class TestConditionalCount(BaseTest):

    def test_conditional_count(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(5, 0))[0]

            conditional_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "entities", "equals": 4})
            conditional_not_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "entities", "ne": 4})
            conditional_less_than = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "lt": 4})
            conditional_less_than_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "lte": 4})
            conditional_greater_than = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "gt": 4})
            conditional_greater_than_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "gte": 4})

            # cant compare tag on attribute
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.mechanics.conditionals.get_conditional(
                    "0", {"count": "self", "tagged": "tag:x"})

            self.assertTrue(conditional_equals.is_true(unit))
            self.assertFalse(conditional_not_equals.is_true(unit))
            self.assertFalse(conditional_less_than.is_true(unit))
            self.assertTrue(conditional_less_than_equals.is_true(unit))
            self.assertFalse(conditional_greater_than.is_true(unit))
            self.assertTrue(conditional_greater_than_equals.is_true(unit))

    def test_conditional_if_function_value(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.units.list()[0]
            unit.set_attribute("units-count-true", 4)
            unit.set_attribute("units-count-false", 5)

            conditional_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "equals": "@self.units-count-true"})
            conditional_not_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "equals": "@self.units-count-false"})

            self.assertTrue(conditional_equals.is_true(unit))
            self.assertFalse(conditional_not_equals.is_true(unit))
