from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models.datapacks.tiles.tile_textures import TileTextures


class TestTileTextures(BaseTest):

    def test_tile_textures_parsing_color(self):
        # Type is wrong
        with self.assertRaises(errors.ValidationError):
            TileTextures.load("", {"color": 0})

        # String color
        textures = TileTextures.load("", {"color": "example"})
        self.assertEqual(["example"], textures.colors)

        # List color
        textures = TileTextures.load("", {"color": ["example", "example2"]})
        self.assertIn("example", textures.colors)
        self.assertIn("example2", textures.colors)

        # Json color
        textures = TileTextures.load("", {"color": {"example": 2, "example2": 1}})
        self.assertIn("example", textures.colors)
        self.assertIn("example2", textures.colors)
        self.assertEqual(3, len(textures.colors))

        self.assertIn(textures.choose_color(), ["example", "example2"])
        self.assertIsNone(textures.choose_image())

    def test_tile_textures_parsing_image(self):
        # Image is wrong
        with self.assertRaises(errors.ValidationError):
            TileTextures.load("", {"color": "example", "image": 0})

        # String image
        textures = TileTextures.load("", {"color": "example", "image": "example"})
        self.assertEqual(["example"], textures.images)

        # List image
        textures = TileTextures.load("", {"color": "example", "image": ["example", "example2"]})
        self.assertIn("example", textures.images)
        self.assertIn("example2", textures.images)

        # Json image
        textures = TileTextures.load("", {"color": "example", "image": {"example": 2, "example2": 1}})
        self.assertIn("example", textures.images)
        self.assertIn("example2", textures.images)
        self.assertEqual(3, len(textures.images))

        self.assertIn(textures.choose_color(), ["example", "example2"])
        self.assertIn(textures.choose_image(), ["example", "example2"])
