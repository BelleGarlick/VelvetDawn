import velvet_dawn.map.creation
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics import selectors


class TestLocalSelectors(BaseTest):

    def test_selector_parsing(self):
        selector = selectors.get_selector("0", "commander")
        selector_commanders = selectors.get_selector("0", "commanders")
        selector_friendly_commanders = selectors.get_selector("0", "commanders-friendly")
        selector_enemy_commanders = selectors.get_selector("0", "commanders-enemy")

        self.assertTrue(isinstance(selector, selectors.SelectorCommander))
        self.assertTrue(isinstance(selector_commanders, selectors.SelectorCommanders))
        self.assertTrue(isinstance(selector_friendly_commanders, selectors.SelectorFriendlyCommanders))
        self.assertTrue(isinstance(selector_enemy_commanders, selectors.SelectorEnemyCommanders))

    def test_selector_from_unit(self):
        with app.app_context():
            self.setup_game()

            unit = velvet_dawn.units.get_unit_at_position(15, 0)

            selector = selectors.get_selector("0", "commander")
            selector_commanders = selectors.get_selector("0", "commanders")
            selector_friendly_commanders = selectors.get_selector("0", "commanders-friendly")
            selector_enemy_commanders = selectors.get_selector("0", "commanders-enemy")

            self.assertEqual(1, len(selector.get_selection(unit)))
            self.assertEqual(2, len(selector_commanders.get_selection(unit)))
            self.assertEqual(1, len(selector_friendly_commanders.get_selection(unit)))
            self.assertEqual(1, len(selector_enemy_commanders.get_selection(unit)))

            self.assertEqual(unit.id, selector.get_selection(unit)[0].id)
            self.assertEqual(unit.id, selector_friendly_commanders.get_selection(unit)[0].id)
            self.assertNotEqual(unit.id, selector_enemy_commanders.get_selection(unit)[0].id)

    def test_selector_from_tile(self):
        with app.app_context():
            self.setup_game()

            player_a_commander = velvet_dawn.units.get_unit_at_position(15, 0)
            tile = velvet_dawn.map.get_tile(15, 0)

            selector = selectors.get_selector("0", "commander")
            selector_commanders = selectors.get_selector("0", "commanders")
            selector_friendly_commanders = selectors.get_selector("0", "commanders-friendly")
            selector_enemy_commanders = selectors.get_selector("0", "commanders-enemy")

            self.assertEqual(0, len(selector.get_selection(tile)))
            self.assertEqual(2, len(selector_commanders.get_selection(tile)))
            self.assertEqual(1, len(selector_friendly_commanders.get_selection(tile)))
            self.assertEqual(1, len(selector_enemy_commanders.get_selection(tile)))

            # Check not friendly commanders is player a
            self.assertEqual(
                player_a_commander.id,
                selector_friendly_commanders.get_selection(tile)[0].id
            )
            self.assertEqual(
                player_a_commander.id,
                selector_friendly_commanders.get_selection(WorldInstance())[0].id
            )

            # Go to next turn
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            # Check not friendly commanders is player b
            self.assertEqual(
                player_a_commander.id,
                selector_enemy_commanders.get_selection(tile)[0].id
            )
            self.assertEqual(
                player_a_commander.id,
                selector_enemy_commanders.get_selection(WorldInstance())[0].id
            )
