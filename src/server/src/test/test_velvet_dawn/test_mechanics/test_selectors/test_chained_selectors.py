import velvet_dawn.units
from test.base_test import BaseTest
from velvet_dawn.dao import app
from velvet_dawn.mechanics import selectors
from velvet_dawn.models.coordinate import Coordinate


class TestChainedSelectors(BaseTest):

    def test_selector_parsing(self):
        selector = selectors.get_selector("0", "world>units>commanders>closest.max.health.example")

        self.assertIsInstance(selector, selectors.SelectorWorld)
        self.assertIsInstance(selector.chained_selector, selectors.SelectorUnits)
        self.assertIsInstance(selector.chained_selector.chained_selector, selectors.SelectorCommanders)
        self.assertIsInstance(selector.chained_selector.chained_selector.chained_selector, selectors.SelectorClosest)

        self.assertEqual(selector.attribute, "max.health.example")

    def test_chained_selectors(self):
        with app.app_context():
            self.prepare_game()

            selector = selectors.get_selector("0", "world>units>commander>tile.max.health.example")

            tiles = selector.get_chained_selection(velvet_dawn.db.units.get_units_at_positions(Coordinate(5, 0))[0])

            # 3 units with two commanders each on 1 tile results in 2 tiles
            self.assertEqual(2, len(tiles))
