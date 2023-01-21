from test.base_test import BaseTest
from velvet_dawn.db.instances import WorldInstance
from velvet_dawn.mechanics import selectors


class TestSelectorsWorld(BaseTest):

    def test_selector_parsing(self):
        """ Test world selector return the world instance """
        selector = selectors.get_selector("0", "world.health.max")
        self.assertTrue(isinstance(selector, selectors.SelectorWorld))

        selection = selector.get_selection(None)
        self.assertTrue(selection[0], WorldInstance())
