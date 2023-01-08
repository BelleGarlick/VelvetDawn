import velvet_dawn.datapacks
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models import Attributes
import velvet_dawn


class TestUnitUpgradesParsing(BaseTest):

    def test_upgrade_parsing(self):
        # Test no name
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {})
        velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {"name": "hi"})

        # Type id is wrong type
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "id": False,
                "name": "hi"
            })

        # Enabled is not a list
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "enabled": False,
                "name": "hi"
            })

        # Hidden is not a list
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "hidden": False,
                "name": "hi"
            })

        # actions is not a list
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "actions": False,
                "name": "hi"
            })

        # Require is not a list of strings
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "requires": False,
                "name": "hi"
            })
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "requires": [False],
                "name": "hi"
            })

        # Random key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
                "random-key": [False],
                "name": "hi"
            })

        # Valid
        velvet_dawn.models.datapacks.units.upgrades.Upgrade.load("0", -1, {
            "id": "example",
            "enabled": [{"if": "self", "eq": "example"}],
            "hidden": [{"if": "self", "ne": "example"}],
            "actions": [{"modify": "self.health", "add": 1}],
            "requires": ["eg"],
            "name": "hi"
        })

