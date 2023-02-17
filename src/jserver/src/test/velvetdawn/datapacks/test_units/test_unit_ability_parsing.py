import velvet_dawn.datapacks
from test.base_test import BaseTest
from velvet_dawn import errors
import velvet_dawn


class TestUnitAbilitiesParsing(BaseTest):

    def test_abilities_parsing(self):
        # Test no name
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {})
        velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {"name": "hi"})

        # Enabled is not a list
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
                "enabled": False,
                "name": "hi"
            })

        # Hidden is not a list
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
                "hidden": False,
                "name": "hi"
            })

        # actions is not a list
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
                "actions": False,
                "name": "hi"
            })

        # Require is not a list of strings
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
                "requires": False,
                "name": "hi"
            })
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
                "requires": [False],
                "name": "hi"
            })

        # Random key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
                "random-key": [False],
                "name": "hi"
            })

        # Valid
        velvet_dawn.models.datapacks.units.abilities.Ability.load("0", -1, {
            "enabled": [{"if": "self", "eq": "example"}],
            "hidden": [{"if": "self", "ne": "example"}],
            "actions": [{"modify": "self.health", "add": 1}],
            "name": "hi"
        })
