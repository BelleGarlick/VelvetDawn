import velvet_dawn.map.creation
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.db.instances import WorldInstance
from velvet_dawn.mechanics import selectors
from velvet_dawn.mechanics.selectors import SelectorUnit, SelectorUnits, SelectorFriendlies, SelectorEnemies


""" Test the unit selectors get the correct selection 
for the different instance types.
"""


class TestUnitSelectors(BaseTest):

    def test_selector_units(self):
        selector = selectors.get_selector("0", "unit")
        units_selector = selectors.get_selector("0", "units")
        friendlies_selector = selectors.get_selector("0", "friendlies")
        selector_enemies = selectors.get_selector("0", "enemies")

        self.assertTrue(isinstance(selector, SelectorUnit))
        self.assertTrue(isinstance(units_selector, SelectorUnits))
        self.assertTrue(isinstance(friendlies_selector, SelectorFriendlies))
        self.assertTrue(isinstance(selector_enemies, SelectorEnemies))

    def test_selectors_from_unit(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.db.units.get_units_at_positions(5, 0)[0]

            selector = selectors.get_selector(unit.id, "unit")
            units_selector = selectors.get_selector(unit.id, "units")
            friendlies_selector = selectors.get_selector(unit.id, "friendlies")
            selector_enemies = selectors.get_selector(unit.id, "enemies")

            single_unit = selector.get_selection(unit)
            all_units = units_selector.get_selection(unit)
            friendlies = friendlies_selector.get_selection(unit)
            enemies = selector_enemies.get_selection(unit)
            self.assertEqual(unit.id, single_unit[0].id)
            self.assertEqual(4, len(all_units))
            self.assertEqual(3, len(friendlies))
            self.assertEqual(1, len(enemies))

    def test_selectors_from_tile_and_world(self):
        with app.app_context():
            self.prepare_game()

            tile = velvet_dawn.db.tiles.get_tile(5, 0)

            # Get selectors
            selector = selectors.get_selector(tile.tile_id, "unit")
            units_selector = selectors.get_selector(tile.tile_id, "units")
            friendlies_selector = selectors.get_selector(tile.tile_id, "friendlies")
            selector_enemies = selectors.get_selector(tile.tile_id, "enemies")

            # From tile perspective
            single_unit = selector.get_selection(tile)
            all_units = units_selector.get_selection(tile)
            friendlies = friendlies_selector.get_selection(tile)
            enemies = selector_enemies.get_selection(tile)
            self.assertEqual(1, len(single_unit))
            self.assertEqual(4, len(all_units))
            self.assertEqual(3, len(friendlies))
            self.assertEqual(1, len(enemies))

            # From world perspective
            single_unit = selector.get_selection(WorldInstance())
            all_units = units_selector.get_selection(WorldInstance())
            friendlies = friendlies_selector.get_selection(WorldInstance())
            enemies = selector_enemies.get_selection(WorldInstance())
            self.assertEqual(0, len(single_unit))
            self.assertEqual(4, len(all_units))
            self.assertEqual(3, len(friendlies))
            self.assertEqual(1, len(enemies))

            # Switch turns
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            # From tile perspective
            friendlies = friendlies_selector.get_selection(tile)
            enemies = selector_enemies.get_selection(tile)
            self.assertEqual(1, len(friendlies))
            self.assertEqual(3, len(enemies))

            # From world perspective
            friendlies = friendlies_selector.get_selection(WorldInstance())
            enemies = selector_enemies.get_selection(WorldInstance())
            self.assertEqual(1, len(friendlies))
            self.assertEqual(3, len(enemies))
