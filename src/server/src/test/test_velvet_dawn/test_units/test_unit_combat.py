import velvet_dawn.units
from test.base_test import BaseTest
from velvet_dawn.dao import app
from velvet_dawn.models.coordinate import Coordinate


class TestUnitCombat(BaseTest):

    def test_unit_combat(self):
        """ This function tests one unit attacking multiple units in the same position """
        with app.app_context():
            self.prepare_game()

            attacker = velvet_dawn.units.list()[0]
            attackees = velvet_dawn.units.list()[1:]
            target_position = Coordinate(attacker.x + 1, attacker.y)
            player = velvet_dawn.players.get_player(attacker.player)

            attacker.set_attribute("health", 100)
            attacker.set_attribute("combat.attack", 30)

            for attackee in attackees:
                velvet_dawn.db.units.move(attackee, target_position)
                attackee.set_attribute("health", 100)
                attackee.set_attribute("combat.attack", 20)

            velvet_dawn.units.combat.attack_entity(player, attacker.id, target_position)

            # Each of the three attackes should lose the (combat of the attacker)/(n attackees)
            for attackee in attackees:
                self.assertEqual(90, attackee.get_attribute("health"))

            # Each attackee damages the attacker
            self.assertEqual(40, attacker.get_attribute("health"))

    # TODO Test selectors ran
    # TODO, test: kill, blast radius and defense, validate range of target from attacker
