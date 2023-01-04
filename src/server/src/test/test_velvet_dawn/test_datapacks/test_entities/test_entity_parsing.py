import velvet_dawn.datapacks
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models import Attributes


class TestUnitParsing(BaseTest):

    def test_unit_health(self):
        # Type is wrong
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_health("", Attributes(), {"max": "dsa"})

        # Must be at least 0
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_health("", Attributes(), {"max": -1})

        # Wrong key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_health("", Attributes(), {"random-key": False})

        # Valid
        attributes = Attributes()
        velvet_dawn.models.unit._parse_health("", attributes, {
            "max": 1000,
            "notes": "Example"
        })
        self.assertEqual(1000, attributes.attributes['health.max'].default)

    def test_unit_combat(self):
        # Type is wrong
        for key in ["range", "attack", "defense", "reload"]:
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.models.unit._parse_combat("", Attributes(), {key: "dsa"})

        # Must be at least 0
        for key in ["range", "attack", "defense", "reload"]:
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.models.unit._parse_combat("", Attributes(), {key: -1})

        # Wrong key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_combat("", Attributes(), {"random-key": False})

        # Valid
        attributes = Attributes()
        velvet_dawn.models.unit._parse_combat("", attributes, {
            "range": 5,
            "attack": 10,
            "defense": 20,
            "reload": 0,
            "notes": "Example"
        })
        self.assertEqual(5, attributes.attributes['combat.range'].default)
        self.assertEqual(10, attributes.attributes['combat.attack'].default)
        self.assertEqual(20, attributes.attributes['combat.defense'].default)
        self.assertEqual(0, attributes.attributes['combat.reload'].default)

    def test_unit_movement(self):
        # Type is wrong
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_movement("", Attributes(), {"range": "dsa"})

        # Must be at least 0
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_movement("", Attributes(), {"range": 0})

        # Wrong key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.models.unit._parse_movement("", Attributes(), {"range": 2, "random-key": False})

        # Valid
        attributes = Attributes()
        velvet_dawn.models.unit._parse_movement("", attributes, {
            "range": 5,
            "notes": "Example"
        })
        self.assertEqual(5, attributes.attributes['movement.range'].default)
