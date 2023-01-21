import velvet_dawn.units
from test.base_test import BaseTest
from velvet_dawn.dao import app
from velvet_dawn.db.instances import WorldInstance
from velvet_dawn.mechanics import selectors


class TestSelectors(BaseTest):

    def test_selector_parsing(self):
        # Parsing self selector for both types
        self.assertTrue(isinstance(selectors.get_selector("0", "self.health.max"), selectors.SelectorSelf))
        selector = selectors.get_selector("0", "unit>units[range=2]>commander.health")
        self.assertTrue(isinstance(selector, selectors.SelectorUnit))
        self.assertTrue(isinstance(selector.chained_selector, selectors.SelectorUnits))
        self.assertTrue(isinstance(selector.chained_selector.chained_selector, selectors.SelectorCommander))
        self.assertEqual(selector.attribute, "health")
        self.assertEqual(selector.chained_selector.filters.max_range, 2)

    def test_attributes(self):
        self.assertEqual(selectors.get_selector("0", "self.health.max").attribute, "health.max")
        self.assertEqual(selectors.get_selector("0", "units[id=1].combat.range").attribute, "combat.range")
        self.assertIsNone(selectors.get_selector("0", "tile").attribute)

    def test_selector_get_value(self):
        """ Test get values handles different data types properly """
        with app.app_context():
            self.prepare_game()

            # No attributes on units, so returns none
            self.assertIsNone(selectors.get_selector("0", "units.example").function_get_value(WorldInstance()))

            # Test with one number
            velvet_dawn.units.list()[0].set_attribute("example", 5)
            self.assertEqual(5, selectors.get_selector("0", "units.example").function_get_value(WorldInstance()))

            # Test the average of the two numbers
            velvet_dawn.units.list()[1].set_attribute("example", 3)
            self.assertEqual(4, selectors.get_selector("0", "units.example").function_get_value(WorldInstance()))

            # Test mixed values
            velvet_dawn.units.list()[1].set_attribute("example", "dsadsa")
            self.assertIsNone(selectors.get_selector("0", "units.example").function_get_value(WorldInstance()))

            # Test not equal strings
            velvet_dawn.units.list()[0].set_attribute("example", "dsadsa")
            velvet_dawn.units.list()[1].set_attribute("example", "aaaaa")
            self.assertIsNone(selectors.get_selector("0", "units.example").function_get_value(WorldInstance()))

            # Test equal strings
            velvet_dawn.units.list()[0].set_attribute("example", "aaaaa")
            velvet_dawn.units.list()[1].set_attribute("example", "aaaaa")
            self.assertEqual("aaaaa", selectors.get_selector("0", "units.example").function_get_value(WorldInstance()))
