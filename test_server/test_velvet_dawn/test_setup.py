import errors
import velvet_dawn.game.setup
from velvet_dawn.dao import app
from test_server.base_test import BaseTest
from velvet_dawn.models.phase import Phase


class TestSetup(BaseTest):
    def test_updating_setup_definition(self):
        with app.app_context():
            setup = velvet_dawn.game.setup.get_setup()
            self.assertEqual(len(setup.commanders), 0)
            self.assertEqual(len(setup.units), 0)

            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.setup.update_setup("invalid_name", 10)

            # Add item to setup
            velvet_dawn.game.setup.update_setup("civil-war:workers", 10)
            setup = velvet_dawn.game.setup.get_setup()
            self.assertEqual(setup.units[0].entity_id, "civil-war:workers")
            self.assertEqual(setup.units[0].amount, 10)

            # Remove item from setup
            velvet_dawn.game.setup.update_setup("civil-war:workers", 0)
            setup = velvet_dawn.game.setup.get_setup()
            self.assertEqual(len(setup.units), 0)

            # Add commanders
            velvet_dawn.game.setup.update_setup("gods:valnorak", 10)
            velvet_dawn.game.setup.update_setup("gods:baledung", 10)
            setup = velvet_dawn.game.setup.get_setup()
            self.assertEqual(len(setup.commanders), 2)

            # Test setip is valid with commanders
            velvet_dawn.game.setup.update_setup("civil-war:workers", 1)
            self.assertTrue(velvet_dawn.game.setup.is_setup_valid())

            # Test invalid setup with no commanders but has entities
            velvet_dawn.game.setup.update_setup("gods:valnorak", 0)
            velvet_dawn.game.setup.update_setup("gods:baledung", 0)
            self.assertFalse(velvet_dawn.game.setup.is_setup_valid())

    def test_place_setup_entity(self):
        with app.app_context():
            # TODO Check within starting territory
            velvet_dawn.game.phase(set=Phase.Lobby)
            velvet_dawn.map.creation.new(5, 5)
            velvet_dawn.players.join("playerA", "")
            velvet_dawn.players.join("playerB", "")
            velvet_dawn.game.phase(set=Phase.Setup)

            # Test random entity throws error
            with self.assertRaises(errors.UnknownEntityError):
                velvet_dawn.game.setup.place_entity("playerA", "dsjakdksla", 0, 0)

            # Test trying to place a commander and entity not in the setup definition
            with self.assertRaises(errors.EntityMissingFromSetupDefinition) as e:
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 0, 0)
            with self.assertRaises(errors.EntityMissingFromSetupDefinition) as e:
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 0, 0)

            # Update the setup definition to allow a commander and two muskets
            velvet_dawn.game.phase(set=Phase.Lobby)
            velvet_dawn.game.setup.update_setup("civil-war:commander", 1)
            velvet_dawn.game.setup.update_setup("civil-war:musketeers", 2)
            velvet_dawn.game.phase(set=Phase.Setup)

            # Test creating twos commander is an issue and that a commander can be removed and readded
            # also testing that removing an entity with no entity to remove will rause an error
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 1, 0)
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 2, 0)
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.setup.remove_entity("playerA", 2, 0)
            velvet_dawn.game.setup.remove_entity("playerA", 1, 0)
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:commander", 2, 0)

            # Test placing and placing in same pos and placing too many
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 1, 1)
            with self.assertRaises(errors.ValidationError):  # Placing two items in same cell
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 1, 1)
            velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 1, 3)
            with self.assertRaises(errors.ValidationError):  # too many places
                velvet_dawn.game.setup.place_entity("playerA", "civil-war:musketeers", 1, 2)

            # Test is not validated until player b has been setup
            self.assertFalse(velvet_dawn.game.setup.validate_player_setups())

            velvet_dawn.game.setup.place_entity("playerB", "civil-war:musketeers", 3, 1)
            velvet_dawn.game.setup.place_entity("playerB", "civil-war:musketeers", 3, 3)
            velvet_dawn.game.setup.place_entity("playerB", "civil-war:commander", 4, 2)

            self.assertTrue(velvet_dawn.game.setup.validate_player_setups())
