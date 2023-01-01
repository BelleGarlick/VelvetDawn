import velvet_dawn.datapacks
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models import Attributes


class TestTileParsing(BaseTest):

    def test_tile_movement(self):
        # Type is wrong
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.tile._parse_movement("", Attributes(), {"weight": "dsa"})

        # Must be at least 1
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.tile._parse_movement("", Attributes(), {"weight": 0})

        # Wrong type
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.tile._parse_movement("", Attributes(), {"traversable": "kjl"})

        # Wrong key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.tile._parse_movement("", Attributes(), {"traversable": True, "random-key": False})

        # Valid
        attributes = Attributes()
        velvet_dawn.models.tile._parse_movement("", attributes, {
            "traversable": False,
            "weight": 5,
            "notes": "Example"
        })
        self.assertEqual(False, attributes.attributes['movement.traversable'].default)
        self.assertEqual(5, attributes.attributes['movement.weight'].default)
