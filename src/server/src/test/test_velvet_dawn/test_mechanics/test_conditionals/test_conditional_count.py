import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.dao import app
from velvet_dawn.mechanics.conditionals import ConditionalStandard
from velvet_dawn.mechanics.conditionals.conditional import Comparison


class TestConditionalCount(BaseTest):

    def test_conditional_count(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.get_unit_at_position(15, 0)

            conditional_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "equals": 3})
            conditional_not_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "ne": 3})
            conditional_less_than = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "lt": 3})
            conditional_less_than_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "lte": 3})
            conditional_greater_than = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "gt": 3})
            conditional_greater_than_equals = velvet_dawn.mechanics.conditionals.get_conditional(
                "0", {"count": "units", "gte": 3})

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
