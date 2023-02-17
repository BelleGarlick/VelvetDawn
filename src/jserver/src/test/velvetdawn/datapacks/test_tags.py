from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.models import Tags


class TestTagsParsing(BaseTest):

    def test_attributes_parsing(self):
        # Not list
        with self.assertRaises(errors.ValidationError):
            Tags().load("", {})

        # List but not string item
        with self.assertRaises(errors.ValidationError):
            Tags().load("", [{}])

        # Valid attributes
        tags = Tags().load("", [
            "test1",
            "tag:test2"
        ])

        self.assertEqual(2, len(tags.tags))
        self.assertTrue(tags.has("tag:test1"))
        self.assertTrue(tags.has("tag:test2"))
