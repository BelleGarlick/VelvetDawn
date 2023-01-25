import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.dao import app
from velvet_dawn.models.coordinate import Coordinate


class TestUnitAbilities(BaseTest):

    def test_abilities(self):
        """ The testing:abilitied unit has predefined abilities specifically
        for this test to make sure that hidden/enabled all work correctly.
        """
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(6, 0))[0]
            abilities = velvet_dawn.datapacks.entities[unit.entity_id].abilities.abilities

            # Unit not found raised
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.abilities.run_unit_ability(unit.player, "-1", abilities[0].id)

            # Invalid ability
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, "random key")

            # Invalid player
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.abilities.run_unit_ability("invlid", unit.id, abilities[0].id)

            velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities[0].id)
            self.assertTrue(unit.has_tag("tag:ability1-ran"))

            # Test hidden elements can't run as missing tag
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities[1].id)
            unit.add_tag("tag:visible")
            velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities[1].id)
            self.assertTrue(unit.has_tag("tag:ability2-ran"))

            # Test disable elements can't run as missing tag
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities[2].id)
            unit.add_tag("tag:enabled")
            velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities[2].id)
            self.assertTrue(unit.has_tag("tag:ability3-ran"))

    def test_fetching_abilities(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(6, 0))[0]
            abilities_list = velvet_dawn.datapacks.entities[unit.entity_id].abilities.abilities

            abilities = velvet_dawn.units.abilities.get_unit_ability_updates(unit.id)
            self.assertEqual(1, len(abilities.abilities))
            self.assertEqual(1, len(abilities.hidden))
            self.assertEqual(1, len(abilities.disabled))

            unit.add_tag("tag:visible")
            velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities_list[1].id)
            abilities = velvet_dawn.units.abilities.get_unit_ability_updates(unit.id)
            self.assertEqual(2, len(abilities.abilities))
            self.assertEqual(0, len(abilities.hidden))
            self.assertEqual(1, len(abilities.disabled))

            unit.add_tag("tag:enabled")
            velvet_dawn.units.abilities.run_unit_ability(unit.player, unit.id, abilities_list[2].id)
            abilities = velvet_dawn.units.abilities.get_unit_ability_updates(unit.id)
            self.assertEqual(3, len(abilities.abilities))
            self.assertEqual(0, len(abilities.hidden))
            self.assertEqual(0, len(abilities.disabled))

