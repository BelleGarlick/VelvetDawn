import velvet_dawn
from test.base_test import BaseTest


class TestDbSetup(BaseTest):

    def test_setup(self):
        velvet_dawn.db.setup_untits.set_count("a", 10)
        velvet_dawn.db.setup_untits.set_count("a", 0)
        velvet_dawn.db.setup_untits.set_count("b", 10)
        velvet_dawn.db.setup_untits.set_count("c", -10)

        setup = velvet_dawn.db.setup_untits.get()
        self.assertEqual(0, setup['a'])
        self.assertEqual(10, setup['b'])
        self.assertEqual(-10, setup['c'])
