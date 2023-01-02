from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models import Tile, Entity
from velvet_dawn.mechanics import selectors


class TestSelectorsParsing(BaseTest):

    def test_selector_parsing(self):
        # Parsing self selector for both types
        self.assertTrue(isinstance(selectors.get_selector("0", Tile, "self.health.max"), selectors.SelectorSelf))

        self.assertTrue(isinstance(selectors.get_selector("0", Tile, "local-units.combat.range"), selectors.SelectorLocalUnits))
        self.assertTrue(isinstance(selectors.get_selector("0", Tile, "local-tiles"), selectors.SelectorLocalTiles))
        self.assertTrue(isinstance(selectors.get_selector("0", Entity, "local-units.combat.range"), selectors.SelectorLocalUnits))
        self.assertTrue(isinstance(selectors.get_selector("0", Entity, "local-friendlies.combat.range"), selectors.SelectorLocalFriendlies))
        self.assertTrue(isinstance(selectors.get_selector("0", Entity, "local-enemies.combat.range"), selectors.SelectorLocalEnemies))
        self.assertTrue(isinstance(selectors.get_selector("0", Entity, "local-tiles"), selectors.SelectorLocalTiles))

        self.assertTrue(isinstance(selectors.get_selector("0", Entity, "tile"), selectors.SelectorTile))
        self.assertTrue(isinstance(selectors.get_selector("0", Tile, "unit"), selectors.SelectorUnit))

    def test_selector_invalid_filters(self):
        # Test valid filters
        selectors.get_selector("0", Tile, "local[id=10,tag=dsa,range=100]")
        selectors.get_selector("0", Entity, "local[id=10,tag=dsa,range=100]")
        selectors.get_selector("0", Entity, "local-enemies[id=10]")
        selectors.get_selector("0", Entity, "local-friendlies[id=10]")

        # Invalid filters
        with self.assertRaises(errors.InvalidSelectorFilter):
            selectors.get_selector("0", Entity, "local[id=10,tag=dsa,range=100, invalid_tag=dsa]")
        with self.assertRaises(errors.InvalidSelectorFilter):
            selectors.get_selector("0", Tile, "local[id=10,tag=dsa,range=100, invalid_tag=dsa]")

        with self.assertRaises(errors.InvalidSelectorFilter):
            selectors.get_selector("0", Tile, "self[range=10]")

    def test_attributes(self):
        self.assertEqual(selectors.get_selector("0", Tile, "self.health.max").attribute, "health.max")
        self.assertEqual(selectors.get_selector("0", Tile, "local-units[id=1].combat.range").attribute, "combat.range")
        self.assertIsNone(selectors.get_selector("0", Entity, "tile").attribute)
