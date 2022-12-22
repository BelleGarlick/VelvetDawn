import os
import json
from pathlib import Path

import velvet_dawn
from test_server.base_test import BaseTest


# TODO Test overriding entity from files

# TODO Test loading entities from json works as expected


class TestDatapackLoading(BaseTest):

    def test_construct_id(self):
        """ Test entity id is correct """
        datapack_path = Path("example") / "entities"

        def _id(x, ft=False, data=None):
            return velvet_dawn.datapacks._construct_id(x, include_file_type=ft, data=data)

        self.assertEqual("example:entity1", _id(datapack_path / "entity1.json"))
        self.assertEqual("example:entity1.json", _id(datapack_path / "entity1.json", ft=True))
        self.assertEqual("example:_entity1", _id(datapack_path / "_entity1.json"))
        self.assertEqual("other:entity1", _id(datapack_path / "other_entity1.json"))
        self.assertEqual("other:ahh", _id(datapack_path / "entity1.json", data={"id": "other:ahh"}))

    def test_load_items_in_dir(self):
        """ Test that files are loaded correctly into concrete and abstracts dirs """
        test_path = Path("test_directory")
        if test_path.exists():
            for file in os.listdir(test_path):
                os.remove(test_path / file)
            test_path.rmdir()
        test_path.mkdir()

        with open(test_path / "pack_example-a.json", "w+") as file:
            json.dump({"abstract": True, "name": "example_a"}, file)

        with open(test_path / "example-b.json", "w+") as file:
            json.dump({"name": "example_b"}, file)

        files = velvet_dawn.datapacks._load_items_in_dir(test_path)
        self.assertNotIn(test_path / "pack_example-a.json", files)
        self.assertIn(test_path / "example-b.json", files)
        self.assertIn("pack:example-a", velvet_dawn.datapacks._abstract_definitions)

        if test_path.exists():
            for file in os.listdir(test_path):
                os.remove(test_path / file)
            test_path.rmdir()

    def test_extend(self):
        velvet_dawn.datapacks._abstract_definitions = {
            "a": {"b": "c"},
            "d": {
                "e": ["f", "g"],
                "h": 1
            }
        }

        # Check no extension
        extended = velvet_dawn.datapacks._extend({})
        self.assertEqual(0, len(extended))

        # Check no extension even with the extension tag
        extended = velvet_dawn.datapacks._extend({"extends": []})
        self.assertEqual(1, len(extended))

        # Check extending from a but not d
        extended = velvet_dawn.datapacks._extend({"extends": ["a"]})
        self.assertEqual(2, len(extended))
        self.assertEqual("c", extended["b"])
        self.assertIsNone(extended.get("d"))

        # Check extending from d but not a
        extended = velvet_dawn.datapacks._extend({"extends": ["d"]})
        self.assertEqual(3, len(extended))
        self.assertEqual(1, extended["h"])
        self.assertIsNone(extended.get("b"))

        # Test extends from both
        extended = velvet_dawn.datapacks._extend({"extends": ["a", "d"]})
        self.assertEqual(4, len(extended))
        self.assertEqual(1, extended["h"])
        self.assertEqual("c", extended["b"])

    def test_copy_dict(self):
        """ Test copying dicts merged works """
        base = {
            "a": "string",
            "b": 0,
            "c": True,
            "e": {"f": "g"},
            "h": ["i"]
        }

        merged = {}
        velvet_dawn.datapacks._merge_dicts(merged, base)

        self.assertEqual(merged["a"], "string")

        # Test updating again works in meregd but doesn't affect base
        velvet_dawn.datapacks._merge_dicts(merged, {
            "a": "not string",
            "e": {
                "z": "y"
            },
            "h": ["j"]
        })

        # Updating doesn't update original
        self.assertEqual(merged["a"], "not string")
        self.assertEqual(base["a"], "string")

        self.assertEqual(merged["e"]["f"], "g")
        self.assertEqual(merged["e"]["z"], "y")
        self.assertIsNone(base["e"].get("z"))

        self.assertEqual(2, len(merged["h"]))
        self.assertEqual(1, len(base["h"]))
