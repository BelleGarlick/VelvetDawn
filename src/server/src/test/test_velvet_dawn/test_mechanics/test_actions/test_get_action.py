import velvet_dawn.datapacks
from velvet_dawn import errors
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.mechanics.actions import ActionModify


class TestGetAction(BaseTest):

    def test_get_actions(self):
        action = velvet_dawn.mechanics.actions.get_action("0", {
            "modify": "self.health",
            "set": "x"
        })
        self.assertTrue(isinstance(action, ActionModify))

        # Invalid action
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.actions.get_action("0", {
                "random key": "self.health",
            })

    def test_action_can_run(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.get_unit_at_position(15, 0)
            action = velvet_dawn.mechanics.actions.get_action("0", {
                "modify": "self.health",
                "set": 100,
                "conditions": [{
                    "if": "self.health",
                    "lte": 10
                }]
            })

            unit.set_attribute("health", 50)
            self.assertFalse(action.can_run(unit))

            unit.set_attribute("health", 2)
            self.assertTrue(action.can_run(unit))

