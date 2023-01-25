from velvet_dawn import errors, datapacks
import velvet_dawn.game.setup
import velvet_dawn.game.setup
from velvet_dawn.config import Config

from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.db.models import Phase

test_config = Config()
test_config.datapacks = ['civil-war']


class TestSetup(BaseTest):
    @classmethod
    def setUpClass(cls) -> None:
        velvet_dawn.datapacks.init(test_config)

    def test_updating_setup_definition(self):
        with app.app_context():
            velvet_dawn.players.join("player1", "password")

            setup = velvet_dawn.game.setup.get_setup("player1")
            self.assertEqual(len(setup.commanders), 0)
            self.assertEqual(len(setup.units), 0)

            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.setup.update_setup("invalid_name", 10)

            # Add item to setup
            velvet_dawn.game.setup.update_setup("civil-war:workers", 10)
            setup = velvet_dawn.game.setup.get_setup("player1")
            self.assertEqual(setup.units["civil-war:workers"], 10)

            # Remove item from setup
            velvet_dawn.game.setup.update_setup("civil-war:workers", 0)
            setup = velvet_dawn.game.setup.get_setup("player1")
            self.assertEqual(len(setup.units), 0)

            # Add commanders
            velvet_dawn.game.setup.update_setup("civil-war:commander", 10)
            setup = velvet_dawn.game.setup.get_setup("player1")
            self.assertEqual(len(setup.commanders), 1)

            # Test setup is valid with commanders
            velvet_dawn.game.setup.update_setup("civil-war:workers", 1)
            self.assertTrue(velvet_dawn.game.setup.is_setup_valid("player1"))

            # Test invalid setup with no commanders but has entities
            velvet_dawn.game.setup.update_setup("civil-war:commander", 0)
            self.assertFalse(velvet_dawn.game.setup.is_setup_valid("player1"))

    def test_place_setup_entity(self):
        with app.app_context():
            for tile in datapacks.tiles:
                datapacks.tiles[tile].attributes.set("movement.traversable", value=True)

            config = Config().set_map_size(50, 50)
            velvet_dawn.db.key_values.set_phase(Phase.Lobby)
            velvet_dawn.map.new(config)
            velvet_dawn.players.join("playerA", "")
            velvet_dawn.players.join("playerB", "")
            velvet_dawn.game.phase.start_setup_phase(config)

            # Test random entity throws error
            with self.assertRaises(errors.UnknownEntityError):
                velvet_dawn.game.setup.place_entity("playerA", "dsjakdksla", 0, 0)

            # Test trying to place a commander and entity not in the setup definition
            with self.assertRaises(errors.EntityMissingFromSetupDefinition) as e:
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 25, 0)
            with self.assertRaises(errors.EntityMissingFromSetupDefinition) as e:
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 25, 0)

            # Update the setup definition to allow a commander and two muskets
            velvet_dawn.db.key_values.set_phase(Phase.Lobby)
            velvet_dawn.game.setup.update_setup("civil-war:commander", 1)
            velvet_dawn.game.setup.update_setup("civil-war:musketeers", 2)
            velvet_dawn.db.key_values.set_phase(Phase.Setup)

            # Test creating twos commander is an issue and that a commander can be removed and re-added
            # also testing that removing an entity with no entity to remove will raise an error
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 24, 0)
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 26, 0)
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.setup.remove_entity("playerA", 26, 0)
            velvet_dawn.game.setup.remove_entity("playerA", 24, 0)
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 26, 0)

            # Test placing and placing in same pos and placing too many
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 24, 1)
            with self.assertRaises(errors.ValidationError):  # Placing two items in same cell
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 24, 1)
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 23, 1)
            with self.assertRaises(errors.ValidationError):  # too many places
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 24, 2)

            # Test is not validated until player b has been setup
            self.assertFalse(velvet_dawn.game.setup.validate_player_setups())

            velvet_dawn.game.setup.place_entity("playerB", "civil-war:musketeers", 25, 49)
            velvet_dawn.game.setup.place_entity("playerB", "civil-war:musketeers", 24, 49)
            velvet_dawn.game.setup.place_entity("playerB", "civil-war:commander", 26, 49)

            self.assertTrue(velvet_dawn.game.setup.validate_player_setups())
