import velvet_dawn.datapacks
from velvet_dawn import errors
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.mechanics.actions import ActionModify
from velvet_dawn.models import Unit


class TestGetAction(BaseTest):

    def test_get_actions(self):
        with app.app_context():
            action = velvet_dawn.mechanics.actions.get_action("0", Unit, {
                "modify": "self.health",
                "set": "x"
            })
            self.assertTrue(isinstance(action, ActionModify))

            # Invalid action
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.mechanics.actions.get_action("0", Unit, {
                    "random key": "self.health",
                })

