import velvet_dawn
from test.base_test import BaseTest


class TestDaoTags(BaseTest):

    def test_crud_operations(self):
        """ Test all crud operations for tags """
        velvet_dawn.db.tags.add_unit_tag("1", "tag:example")
        velvet_dawn.db.tags.add_unit_tag("1", "tag:example2")
        velvet_dawn.db.tags.add_unit_tag("2", "tag:example")
        velvet_dawn.db.tags.add_unit_tag("2", "tag:example3")
        velvet_dawn.db.tags.add_tile_tag("1", "tag:example-tile1")
        velvet_dawn.db.tags.add_tile_tag("1", "tag:example-tile2")
        velvet_dawn.db.tags.add_world_tag("tag:example")

        # Check Units
        tags = velvet_dawn.db.tags.get_unit_tags("1")
        self.assertIn("tag:example", tags)
        self.assertIn("tag:example2", tags)

        unit_ids = velvet_dawn.db.tags.get_units_with_tag("tag:example")
        self.assertIn("1", unit_ids)
        self.assertIn("2", unit_ids)

        # Check tiles
        tags = velvet_dawn.db.tags.get_tile_tags("1")
        self.assertIn("tag:example-tile1", tags)
        self.assertIn("tag:example-tile2", tags)

        self.assertFalse(velvet_dawn.db.tags.get_tiles_with_tag("tag:example"))  # empty set
        tile_ids = velvet_dawn.db.tags.get_tiles_with_tag("tag:example-tile1")
        self.assertIn("1", tile_ids)
        self.assertNotIn("2", tile_ids)

        # Check world
        tags = velvet_dawn.db.tags.get_world_tags()
        self.assertIn("tag:example", tags)
        self.assertNotIn("tag:example2", tags)

        # Test removing
        velvet_dawn.db.tags.remove_unit_tag("1", "tag:example")
        unit_ids = velvet_dawn.db.tags.get_units_with_tag("tag:example")
        self.assertNotIn("1", unit_ids)
        self.assertIn("2", unit_ids)

        # Test removing unit
        velvet_dawn.db.tags.remove_unit("2")
        self.assertFalse(velvet_dawn.db.tags.get_tiles_with_tag("tag:example"))
        self.assertFalse(velvet_dawn.db.tags.get_unit_tags("2"))
