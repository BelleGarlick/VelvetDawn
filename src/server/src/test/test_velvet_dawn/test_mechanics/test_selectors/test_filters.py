import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn.dao import app
from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics import selectors


class TestFilteredSelectors(BaseTest):

    def test_filter_parsing(self):
        # Test selectors work
        selector = selectors.get_selector(
            "0", "unit[id=10,tag=dsa,range=100]>commanders[id=4,tag=10]")

        self.assertIsInstance(selector, selectors.SelectorUnit)
        self.assertIsInstance(selector.chained_selector, selectors.SelectorCommanders)

        self.assertIn('10', selector.filters.allowed_ids)
        self.assertIn('tag:dsa', selector.filters.allowed_tags)
        self.assertEqual(100, selector.filters.max_range)
        self.assertIsNone(selector.filters.min_range)

        self.assertIn('4', selector.chained_selector.filters.allowed_ids)
        self.assertIn('tag:10', selector.chained_selector.filters.allowed_tags)
        self.assertNotIn('10', selector.chained_selector.filters.allowed_tags)
        self.assertIsNone(selector.chained_selector.filters.max_range)
        self.assertIsNone(selector.chained_selector.filters.min_range)

    def test_filters_id(self):
        with app.app_context():
            self.prepare_game()

            selector_1 = selectors.get_selector('world', "units[tag=tag:test-tag1]")
            selector_2 = selectors.get_selector('world', "units[tag=x]")

            self.assertEqual(2, len(selector_1.get_selection(WorldInstance())))
            self.assertEqual(0, len(selector_2.get_selection(WorldInstance())))

    def test_filters_tags(self):
        with app.app_context():
            self.prepare_game()

            selector_1 = selectors.get_selector('world', "units[id=testing:commander]")
            selector_2 = selectors.get_selector('world', "units[id=testing:upgradable]")
            selector_3 = selectors.get_selector('world', "units[id=testing:commander, id=testing:upgradable]")

            self.assertEqual(2, len(selector_1.get_selection(WorldInstance())))
            self.assertEqual(1, len(selector_2.get_selection(WorldInstance())))
            self.assertEqual(3, len(selector_3.get_selection(WorldInstance())))

    def test_filters_max_range(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.units.get_unit_at_position(5, 0)

            selector_range_0 = selectors.get_selector(unit.entity_id, "tiles[range=0]")
            selector_range_1 = selectors.get_selector(unit.entity_id, "tiles[range=1]")
            selector_range_2 = selectors.get_selector(unit.entity_id, "tiles[range=2]")

            self.assertEqual(1, len(selector_range_0.get_selection(unit)))
            self.assertEqual(6, len(selector_range_1.get_selection(unit)))
            self.assertEqual(11, len(selector_range_2.get_selection(unit)))

    def test_filters_min_range(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.units.get_unit_at_position(5, 0)

            selector_range_0 = selectors.get_selector(unit.entity_id, "tiles[min-range=0]")
            selector_range_1 = selectors.get_selector(unit.entity_id, "tiles[min-range=1]")
            selector_range_2 = selectors.get_selector(unit.entity_id, "tiles[min-range=2]")

            self.assertEqual(77, len(selector_range_0.get_selection(unit)))
            self.assertEqual(76, len(selector_range_1.get_selection(unit)))
            self.assertEqual(71, len(selector_range_2.get_selection(unit)))

    def test_exclude_test_filter(self):
        with app.app_context():
            self.prepare_game()

            unit = velvet_dawn.units.get_unit_at_position(5, 0)

            selector_self = selectors.get_selector(unit.entity_id, "self[exclude-self]")
            selector_units = selectors.get_selector(unit.entity_id, "units[exclude-self]")

            self.assertEqual(0, len(selector_self.get_selection(unit)))
            self.assertEqual(3, len(selector_units.get_selection(unit)))  # only 3 of 4 units returned
