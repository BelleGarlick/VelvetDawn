import time

import velvet_dawn
from test.base_test import BaseTest


class TestDbAttributes(BaseTest):

    def test_attribute_operations(self):
        """ Test getting, setting, setting again, resetting operations """
        # Units
        self.assertEqual(10, velvet_dawn.db.attributes.get_unit_attribute("1", "example.health", 10))  # get default

        velvet_dawn.db.attributes.set_unit_attribute("1", "example.health", 100)
        self.assertEqual(100, velvet_dawn.db.attributes.get_unit_attribute("1", "example.health"))
        velvet_dawn.db.attributes.set_unit_attribute("1", "example.health", 120)
        self.assertEqual(120, velvet_dawn.db.attributes.get_unit_attribute("1", "example.health"))
        velvet_dawn.db.attributes.reset_unit_attribute("1", "example.health", None)
        self.assertEqual(100, velvet_dawn.db.attributes.get_unit_attribute("1", "example.health"))

        velvet_dawn.db.attributes.reset_unit_attribute("1", "another-example", 200)
        self.assertEqual(200, velvet_dawn.db.attributes.get_unit_attribute("1", "another-example"))

        # Tiles
        self.assertEqual(10, velvet_dawn.db.attributes.get_tile_attribute("1", "example.health", 10))
        velvet_dawn.db.attributes.set_tile_attribute("1", "example.health", 100)
        self.assertEqual(100, velvet_dawn.db.attributes.get_tile_attribute("1", "example.health"))
        velvet_dawn.db.attributes.set_tile_attribute("1", "example.health", 120)
        self.assertEqual(120, velvet_dawn.db.attributes.get_tile_attribute("1", "example.health"))
        velvet_dawn.db.attributes.reset_tile_attribute("1", "example.health", None)
        self.assertEqual(100, velvet_dawn.db.attributes.get_tile_attribute("1", "example.health"))

        velvet_dawn.db.attributes.reset_tile_attribute("1", "another-example", 200)
        self.assertEqual(200, velvet_dawn.db.attributes.get_tile_attribute("1", "another-example"))

        # Worlds
        self.assertEqual(10, velvet_dawn.db.attributes.get_world_attribute("example.health", 10))
        velvet_dawn.db.attributes.set_world_attribute("example.health", 100)
        self.assertEqual(100, velvet_dawn.db.attributes.get_world_attribute("example.health"))
        velvet_dawn.db.attributes.set_world_attribute("example.health", 120)
        self.assertEqual(120, velvet_dawn.db.attributes.get_world_attribute("example.health"))
        velvet_dawn.db.attributes.reset_world_attribute("example.health", None)
        self.assertEqual(100, velvet_dawn.db.attributes.get_world_attribute("example.health"))

        velvet_dawn.db.attributes.reset_world_attribute("another-example", 200)
        self.assertEqual(200, velvet_dawn.db.attributes.get_world_attribute("another-example"))

    def test_stale_attributes(self):
        stale_time = time.time() - 100
        velvet_dawn.db.attributes._register_changed_attribute("unit", "1", "example", 1, stale_time)
        velvet_dawn.db.attributes._register_changed_attribute("unit", "1", "example2", 12, stale_time)
        velvet_dawn.db.attributes._register_changed_attribute("unit", "1", "example3", 13)
        velvet_dawn.db.attributes._register_changed_attribute("unit", "1", "example3", 15)

        # Two stale so should be removed
        updates = velvet_dawn.db.attributes.get_attribute_updates()
        self.assertEqual(2, len(updates))
        self.assertTrue(updates[0]['value'] < updates[1]['value'])  # 13 < 15, 15 was added last so should be newest

    def test_removing_units(self):
        velvet_dawn.db.attributes.set_unit_attribute("1", "example.health", 100)
        self.assertEqual(100, velvet_dawn.db.attributes.get_unit_attribute("1", "example.health"))

        velvet_dawn.db.attributes.remove_unit("1")
        self.assertIsNone(velvet_dawn.db.attributes.get_unit_attribute("1", "example.health"))
