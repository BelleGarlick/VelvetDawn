import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.dao import app
from velvet_dawn.models.coordinate import Coordinate


class TestConditionalIf(BaseTest):

    def test_conditional_if(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(5, 0))[0]

            conditional_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.testing", "equals": 5})
            conditional_not_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.testing", "ne": 5})
            conditional_less_than = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.testing", "lt": 5})
            conditional_less_than_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.testing", "lte": 5})
            conditional_greater_than = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.testing", "gt": 5})
            conditional_greater_than_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.testing", "gte": 5})
            conditional_has_tag = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self", "tagged": "x"})

            # cant compare tag on attribute
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.mechanics.conditionals.get_conditional(
                    "0", {"if": "self.testing", "tagged": "x"})

            self.assertFalse(conditional_equals.is_true(unit))

            unit.set_attribute("testing", 5)

            self.assertTrue(conditional_equals.is_true(unit))
            self.assertFalse(conditional_not_equals.is_true(unit))
            self.assertFalse(conditional_less_than.is_true(unit))
            self.assertTrue(conditional_less_than_equals.is_true(unit))
            self.assertFalse(conditional_greater_than.is_true(unit))
            self.assertTrue(conditional_greater_than_equals.is_true(unit))
            self.assertFalse(conditional_has_tag.is_true(unit))

            unit.add_tag("x")

            self.assertTrue(conditional_has_tag.is_true(unit))

    def test_conditional_if_function_value(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.units.list()[0]
            unit.set_attribute("example1", 5)
            unit.set_attribute("example2", 5)
            unit.set_attribute("example3", 3)

            conditional_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.example1", "equals": "@self.example2"})
            conditional_not_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"if": "self.example1", "equals": "@self.example3"})

            self.assertTrue(conditional_equals.is_true(unit))
            self.assertFalse(conditional_not_equals.is_true(unit))
