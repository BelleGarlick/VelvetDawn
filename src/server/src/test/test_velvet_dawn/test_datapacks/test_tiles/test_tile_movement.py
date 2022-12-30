from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models.datapacks.tiles.tile_movement import TileMovement


class TestTileMovement(BaseTest):

    def test_tile_movement(self):
        # Type is wrong
        with self.assertRaises(errors.ValidationError):
            TileMovement.load("", {"weight": "dsa"})

        # Must be at least 1
        with self.assertRaises(errors.ValidationError):
            TileMovement.load("", {"weight": 0})

        # Wrong type
        with self.assertRaises(errors.ValidationError):
            TileMovement.load("", {"traversable": "kjl"})

        # Wrong key
        with self.assertRaises(errors.ValidationError):
            TileMovement.load("", {"traversable": True, "random-key": False})

        # Valid
        movement = TileMovement.load("", {
            "traversable": False,
            "weight": 5,
            "notes": "Example"
        })
        self.assertEqual(False, movement.traversable)
        self.assertEqual(5, movement.weight)
