import velvet_dawn.datapacks
from velvet_dawn import errors
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.mechanics.actions import ActionModify
from velvet_dawn.mechanics.actions.action_modify import ActionModifierFunction
from velvet_dawn.models import Unit


class TestActionModify(BaseTest):

    def test_parsing_dict(self):
        with app.app_context():
            # Wrong major key
            with self.assertRaises(errors.ValidationError):
                ActionModify.from_dict("id", Unit, {
                    "modifies": "self.health",
                    "set": 0
                })

            # No function type
            with self.assertRaises(errors.ValidationError):
                ActionModify.from_dict("id", Unit, {
                    "modify": "self.health"
                })

            # too many function type
            with self.assertRaises(errors.ValidationError):
                ActionModify.from_dict("id", Unit, {
                    "modify": "self.health",
                    "set": 0,
                    "add": 1
                })

            # Can't modify non-attribute
            with self.assertRaises(errors.ValidationError):
                action = ActionModify.from_dict("id", Unit, {
                    "modify": "self",
                    "sub": 0
                })

            # Just right
            action = ActionModify.from_dict("id", Unit, {
                "modify": "self.health",
                "sub": 0
            })
            self.assertEqual(action.function, ActionModifierFunction.SUB)

    def test_modifier_working(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.list()[0]

            action_set = ActionModify.from_dict("id", Unit, {"modify": "self.health", "set": 50})
            action_add = ActionModify.from_dict("id", Unit, {"modify": "self.health", "add": 10})
            action_sub = ActionModify.from_dict("id", Unit, {"modify": "self.health", "subtract": 5})
            action_mul = ActionModify.from_dict("id", Unit, {"modify": "self.health", "multiply": 2})

            self.assertEqual(100, unit.get_attribute("health", _type=int))

            action_set.run(unit, self.get_test_config())
            action_add.run(unit, self.get_test_config())
            action_sub.run(unit, self.get_test_config())
            action_mul.run(unit, self.get_test_config())

            self.assertEqual(110, unit.get_attribute("health", _type=int))

