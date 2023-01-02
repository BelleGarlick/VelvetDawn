import velvet_dawn.map.creation
from velvet_dawn.dao import app
from velvet_dawn.dao.models import UnitInstance
from velvet_dawn.models import Unit
from test.base_test import BaseTest
from velvet_dawn.mechanics import selectors


class TestLocalSelectors(BaseTest):

    def test_selector_local(self):
        with app.app_context():
            self.setup_game()

            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "local")

            # twelve tiles, 3 units
            self.assertEqual(16, len(selector.get_selection(unit, config=self.get_test_config())))

    def test_selector_local_enemies(self):
        with app.app_context():
            self.setup_game()

            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "local-enemies")

            # One enemy
            self.assertEqual(1, len(selector.get_selection(unit, self.get_test_config())))
            self.assertTrue(selector.function_equals(unit, "civil-war:commander", self.get_test_config()))

    def test_selector_local_friendlies(self):
        with app.app_context():
            self.setup_game()

            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "local-friendlies")

            self.assertEqual(2, len(selector.get_selection(unit, self.get_test_config())))

            # They're not all this
            self.assertFalse(selector.function_equals(unit, "civil-war:commander", self.get_test_config()))

            selector = selectors.get_selector(unit.entity_id, Unit, "local-friendlies.health.max")
            selector.function_set(unit, 5, self.get_test_config())
            self.assertTrue(selector.function_equals(unit, 5, self.get_test_config()))

    def test_selector_local_units(self):
        with app.app_context():
            self.setup_game()

            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "local-units")

            self.assertEqual(3, len(selector.get_selection(unit, self.get_test_config())))

    def test_selector_local_tiles(self):
        with app.app_context():
            self.setup_game()

            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(15, 0)
            selector = selectors.get_selector(unit.entity_id, Unit, "local-tiles")

            self.assertEqual(13, len(selector.get_selection(unit, self.get_test_config())))

