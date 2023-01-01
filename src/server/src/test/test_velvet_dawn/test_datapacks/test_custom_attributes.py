from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models.datapacks import Attributes


class TestCustomAttributesParsing(BaseTest):

    def test_attributes_parsing(self):
        # Missing id
        with self.assertRaises(errors.ValidationError):
            Attributes().load("", [{}])

        # Malformed id
        with self.assertRaises(errors.ValidationError):
            Attributes().load("", [{"id": "%id"}])

        # Malformed name
        with self.assertRaises(errors.ValidationError):
            Attributes().load("", [{"id": "example-id", "name": "$£@"}])

        # Invalid default value
        with self.assertRaises(errors.ValidationError):
            Attributes().load("", [{"id": "example-id", "name": "Fine Name", "default": "False"}])

        # Invalid icon
        with self.assertRaises(errors.ValidationError):
            Attributes().load("", [{"id": "example-id", "name": "Fine Name", "icon": False}])

        # Invalid key
        with self.assertRaises(errors.ValidationError):
            Attributes().load("", [{"id": "example-id", "name": "Fine Name", "invalid-key": "False"}])

        # Valid attributes
        Attributes().load("", [
            {"id": "example-id", "name": "Fine Name", "icon": "an icon", "default": 100},
            {"id": "example-id2", "name": "Fine Name", "icon": "an icon", "default": 100},
        ])
