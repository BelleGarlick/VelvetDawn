import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.dao import app
from velvet_dawn.models.coordinate import Coordinate


class TestUnitUpgrades(BaseTest):

    def test_upgrading(self):
        """ The testing:upgrades unit has predefined upgrades specifically
        for this test to make sure that hidden/enabled and requirements all
        work correctly.
        """
        with app.app_context():
            self.prepare_game()

            upgradable_unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(4, 0))[0]
            upgrades = velvet_dawn.datapacks.entities[upgradable_unit.entity_id].upgrades.upgrades

            # Unit not found raised
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, "-1", upgrades[0].id)

            # Invalid upgrade
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, "random key")

            # Invalid player
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit("invlid", upgradable_unit.id, upgrades[0].id)

            # Upgrade already owned
            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[0].id)
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[0].id)

            # Missing upgrade requirement
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[-1].id)

            # Test hidden elements can't run as missing tag
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[1].id)
            upgradable_unit.add_tag("tag:visible")
            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[1].id)

            # Test disable elements can't run as missing tag
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[2].id)
            upgradable_unit.add_tag("tag:enabled")
            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[2].id)

            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, upgrades[3].id)

            self.assertTrue(upgradable_unit.has_tag("tag:upgrade-added"))

    def test_fetching_upgrades(self):
        with app.app_context():
            self.prepare_game()

            upgradable_unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(4, 0))[0]

            upgrades = velvet_dawn.units.upgrades.get_unit_upgrade_updates(upgradable_unit.id)
            self.assertEqual(0, len(upgrades.upgraded))
            self.assertEqual(1, len(upgrades.upgrades))
            self.assertEqual(1, len(upgrades.missing_requirements))
            self.assertEqual(1, len(upgrades.hidden))
            self.assertEqual(1, len(upgrades.disabled))

            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, "health_1")
            upgradable_unit.add_tag("tag:visible")
            upgrades = velvet_dawn.units.upgrades.get_unit_upgrade_updates(upgradable_unit.id)
            self.assertEqual(1, len(upgrades.upgraded))
            self.assertEqual(1, len(upgrades.upgrades))
            self.assertEqual(1, len(upgrades.missing_requirements))
            self.assertEqual(0, len(upgrades.hidden))
            self.assertEqual(1, len(upgrades.disabled))

            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, "health_2")
            upgradable_unit.add_tag("tag:enabled")
            upgrades = velvet_dawn.units.upgrades.get_unit_upgrade_updates(upgradable_unit.id)
            self.assertEqual(2, len(upgrades.upgraded))
            self.assertEqual(1, len(upgrades.upgrades))
            self.assertEqual(1, len(upgrades.missing_requirements))
            self.assertEqual(0, len(upgrades.hidden))
            self.assertEqual(0, len(upgrades.disabled))

            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, "movement")
            upgrades = velvet_dawn.units.upgrades.get_unit_upgrade_updates(upgradable_unit.id)
            self.assertEqual(3, len(upgrades.upgraded))
            self.assertEqual(1, len(upgrades.upgrades))
            self.assertEqual(0, len(upgrades.missing_requirements))
            self.assertEqual(0, len(upgrades.hidden))
            self.assertEqual(0, len(upgrades.disabled))

            velvet_dawn.units.upgrades.upgrade_unit(upgradable_unit.player, upgradable_unit.id, "testing:upgradable-upgrade-3")
            upgrades = velvet_dawn.units.upgrades.get_unit_upgrade_updates(upgradable_unit.id)
            self.assertEqual(4, len(upgrades.upgraded))
            self.assertEqual(0, len(upgrades.upgrades))
            self.assertEqual(0, len(upgrades.missing_requirements))
            self.assertEqual(0, len(upgrades.hidden))
            self.assertEqual(0, len(upgrades.disabled))
