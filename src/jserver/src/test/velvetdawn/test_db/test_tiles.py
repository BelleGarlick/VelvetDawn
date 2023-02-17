import velvet_dawn.db.units
from test.base_test import BaseTest


class TestDbTile(BaseTest):

    def test_hashing_position(self):
        self.assertEqual("0:0", velvet_dawn.db.tiles.get_tile_instance_id(0, 0))
        self.assertEqual("-100:11", velvet_dawn.db.tiles.get_tile_instance_id(-100, 11))

    def test_set_and_get(self):
        tile = velvet_dawn.db.tiles.set_tile(0, 0, "example")
        self.assertEqual("0:0", tile.instance_id)
        self.assertEqual(0, tile.x)
        self.assertEqual(0, tile.y)
        self.assertEqual("example", tile.tile_id)

        get_tile = velvet_dawn.db.tiles.get_tile(0, 0)
        self.assertEqual(tile.tile_id, get_tile.tile_id)
        self.assertEqual(tile.x, get_tile.x)
        self.assertEqual(tile.y, get_tile.y)
        self.assertEqual(tile.instance_id, get_tile.instance_id)

    def test_all(self):
        velvet_dawn.db.tiles.set_tile(0, 0, "example")
        self.assertEqual(1, len(velvet_dawn.db.tiles.all()))

        velvet_dawn.db.tiles.set_tile(0, 1, "example")
        velvet_dawn.db.tiles.set_tile(0, 2, "example")
        velvet_dawn.db.tiles.set_tile(0, 3, "example")
        velvet_dawn.db.tiles.set_tile(0, 4, "example")
        self.assertEqual(5, len(velvet_dawn.db.tiles.all()))

        velvet_dawn.db.tiles.clear()
        self.assertEqual(0, len(velvet_dawn.db.tiles.all()))
