from test.base_test import BaseTest
from velvet_dawn.mechanics import selectors


class TestSelectorsParsing(BaseTest):

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
