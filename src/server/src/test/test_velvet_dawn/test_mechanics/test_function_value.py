import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn.dao import app
from velvet_dawn.mechanics.function_value import FunctionValue
from velvet_dawn.mechanics.selectors import Selector


"""
Test the FunctionValue works across raw values, selectors
and random values.
"""


class TestFunctionValue(BaseTest):

    def test_function_value(self):
        with app.app_context():
            self.prepare_game()

            self.assertEqual(4, FunctionValue().parse("0", 4).value(None))
            self.assertEqual("test", FunctionValue().parse("0", "test").value(None))
            self.assertEqual(None, FunctionValue().parse("0", None).value(None))
            self.assertTrue(1 >= FunctionValue().parse("0", "__rand__").value(None) >= 0)
            self.assertNotEqual(
                FunctionValue().parse("0", "__rand__").value(None),
                FunctionValue().parse("0", "__rand__").value(None)
            )

            unit = velvet_dawn.units.list()[0]
            function = FunctionValue().parse("0", "@self")
            self.assertIsInstance(function._selector_value, Selector)
            self.assertEqual(unit.id, function.value(unit))

            unit.set_attribute("example", 5)
            self.assertEqual(5, FunctionValue().parse("0", "@self.example").value(unit))
