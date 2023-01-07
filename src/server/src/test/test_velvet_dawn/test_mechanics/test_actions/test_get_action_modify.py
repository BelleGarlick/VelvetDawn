import velvet_dawn.datapacks
from velvet_dawn import errors
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.mechanics.actions import ActionModify
from velvet_dawn.mechanics.actions.action_modify import ActionModifierFunction


class TestActionModify(BaseTest):

    def test_parsing_dict(self):
        with app.app_context():
            # Wrong major key
            with self.assertRaises(errors.ValidationError):
                ActionModify.from_dict("id", {
                    "modifies": "self.health",
                    "set": 0
                })

            # No function type
            with self.assertRaises(errors.ValidationError):
                ActionModify.from_dict("id", {
                    "modify": "self.health"
                })

            # too many function type
            with self.assertRaises(errors.ValidationError):
                ActionModify.from_dict("id", {
                    "modify": "self.health",
                    "set": 0,
                    "add": 1
                })

            # Can't modify non-attribute
            with self.assertRaises(errors.ValidationError):
                action = ActionModify.from_dict("id", {
                    "modify": "self",
                    "sub": 0
                })

            # Just right
            action = ActionModify.from_dict("id", {
                "modify": "self.health",
                "sub": 0
            })
            self.assertEqual(action.function, ActionModifierFunction.SUB)

    def test_modifier_working(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.list()[0]

            action_set = ActionModify.from_dict("id", {"modify": "self.health", "set": 50})
            action_add = ActionModify.from_dict("id", {"modify": "self.health", "add": 10})
            action_sub = ActionModify.from_dict("id", {"modify": "self.health", "subtract": 5})
            action_mul = ActionModify.from_dict("id", {"modify": "self.health", "multiply": 2})

            # Test resetting and reset to a default if the attribute doens't exists
            action_reset = ActionModify.from_dict("id", {"modify": "self.health", "reset": 0})
            action_reset_other = ActionModify.from_dict("id", {"modify": "self.healthy", "reset": 9})

            self.assertEqual(100, unit.get_attribute("health"))

            action_set.run(unit)
            action_add.run(unit)
            action_sub.run(unit)
            action_mul.run(unit)

            self.assertEqual(110, unit.get_attribute("health"))

            action_reset.run(unit)
            action_reset_other.run(unit)

            self.assertEqual(100, unit.get_attribute("health"))
            self.assertEqual(9, unit.get_attribute("healthy"))

    def test_modifier_tags(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.list()[0]

            action_add_tag = ActionModify.from_dict("id", {"modify": "self", "add-tag": "tagg"})
            action_remove_tag = ActionModify.from_dict("id", {"modify": "self", "remove-tag": "tagg"})

            self.assertFalse(unit.has_tag("tag:tagg"))
            action_add_tag.run(unit)
            self.assertTrue(unit.has_tag("tag:tagg"))
            action_remove_tag.run(unit)
            self.assertFalse(unit.has_tag("tag:tagg"))

