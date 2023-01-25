import velvet_dawn.db.units
from test.base_test import BaseTest
from velvet_dawn.db.models import Phase


class TestDbKeyValues(BaseTest):

    def test_key_values(self):
        velvet_dawn.db.key_values.set_phase(Phase.GAME)
        self.assertEqual(Phase.GAME, velvet_dawn.db.key_values.get_phase())

        velvet_dawn.db.key_values.set_map_size(49, 50)
        width, height = velvet_dawn.db.key_values.get_map_size()
        self.assertEqual(width, 49)
        self.assertEqual(height, 50)

        velvet_dawn.db.key_values.set_turn_start(-1)
        self.assertEqual(-1, velvet_dawn.db.key_values.get_turn_start())

        velvet_dawn.db.key_values.set_active_turn("value")
        self.assertEqual("value", velvet_dawn.db.key_values.get_active_turn())
