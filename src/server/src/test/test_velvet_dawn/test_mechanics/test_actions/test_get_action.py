import velvet_dawn.datapacks
from velvet_dawn import errors
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.mechanics.actions import ActionModify
from velvet_dawn.models.coordinate import Coordinate


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
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(5, 0))[0]
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

