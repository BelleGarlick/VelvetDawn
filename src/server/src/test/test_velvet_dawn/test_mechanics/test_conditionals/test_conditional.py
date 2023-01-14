import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.mechanics.conditionals import ConditionalStandard, ConditionalCounting
from velvet_dawn.mechanics.conditionals.conditional import Comparison


class TestConditional(BaseTest):

    def test_conditional_parsing(self):
        """ Test the various aspect of parsing to make sure the correct errors are raised """
        # Random key
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.conditionals.get_conditional("0", {
                "if": "self",
                "fdsa": "Random key",
            })

        # Two operations
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.conditionals.get_conditional("0", {
                "if": "self",
                "gt": 5,
                "lt": 5,
            })

        # Cannot compare greater than to a string
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.conditionals.get_conditional("0", {
                "if": "self",
                "gt": "ans",
            })

        # Cannot compare tags on an attribute
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.conditionals.get_conditional("0", {
                "if": "self.attribute",
                "tagged": "atag",
            })

        # Cannot compare tagged on a count condition
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.conditionals.get_conditional("0", {
                "count": "self",
                "tagged": "atag",
            })

        # Test standard comparison
        conditional = velvet_dawn.mechanics.conditionals.get_conditional("0", {
            "if": "self",
            "equals": "testing:commander",
            "reason": "Instance is not a commander",
            "notes": "Test if is a commander"
        })

        self.assertEqual(conditional.not_true_reason, "Instance is not a commander")
        self.assertEqual(conditional.function, Comparison.EQUALS)
        self.assertEqual(conditional.function_value.raw, "testing:commander")
        self.assertIsInstance(conditional, ConditionalStandard)

        # Test count
        conditional = velvet_dawn.mechanics.conditionals.get_conditional("0", {
            "count": "units",
            "equals": 4,
            "reason": "There must be four units",
            "notes": "Test if there are four units"
        })

        self.assertEqual(conditional.not_true_reason, "There must be four units")
        self.assertEqual(conditional.function, Comparison.EQUALS)
        self.assertEqual(conditional.function_value.raw, 4)
        self.assertIsInstance(conditional, ConditionalCounting)

        # Test invalid key (not if/count)
        with self.assertRaises(errors.ValidationError):
            velvet_dawn.mechanics.conditionals.get_conditional("0", {
                "basic": "units",
                "equals": 4,
                "reason": "There must be four units",
                "notes": "Test if there are four units"
            })
