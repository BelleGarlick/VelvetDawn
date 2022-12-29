from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models.datapacks import CustomAttributes


class TestCustomAttributesParsing(BaseTest):

    def test_attributes_parsing(self):
        # Missing id
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"name": "Fine Name"}])

        # Malformed id
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "%id", "name": "Fine Name"}])

        # Duplicated id
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "id", "name": "Fine Name"}, {"id": "id", "name": "Fine Name"}])

        # Missing name
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "example-id"}])

        # Malformed name
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "example-id", "name": "$£@"}])

        # Invalid default value
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "example-id", "name": "Fine Name", "default": "False"}])

        # Invalid icon
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "example-id", "name": "Fine Name", "icon": False}])

        # Invalid hidden
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "example-id", "name": "Fine Name", "hidden": "False"}])

        # Invalid key
        with self.assertRaises(errors.ValidationError):
            CustomAttributes.load("", [{"id": "example-id", "name": "Fine Name", "invalid-key": "False"}])

        # Valid attributes
        CustomAttributes.load("", [
            {"id": "example-id", "name": "Fine Name", "hidden": True, "icon": "an icon", "default": 100},
            {"id": "example-id2", "name": "Fine Name", "hidden": True, "icon": "an icon", "default": 100},
        ])
