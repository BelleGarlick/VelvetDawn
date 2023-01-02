import time

from velvet_dawn import errors
import velvet_dawn.players
from test.base_test import BaseTest
from velvet_dawn.config import Config
from velvet_dawn.server.app import config
from velvet_dawn.dao import app, db
from velvet_dawn.dao.models import Keys, Player
from velvet_dawn.models.phase import Phase


class TestGameTurns(BaseTest):

    def test_check_end_turn_case_in_setup_from_time(self):
        """ Test if the turn should end """
        with app.app_context():
            test_config = Config()
            test_config.setup_time = 1

            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")
            velvet_dawn.game.phase.start_setup_phase(test_config)

            time.sleep(2)
            velvet_dawn.game.turns.check_end_turn_case(test_config)
            self.assertEqual(velvet_dawn.game.phase.get_phase(), Phase.GAME)

    def test_check_end_turn_case_in_setup_when_ready(self):
        """ Test if the turn should end """
        with app.app_context():
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")
            velvet_dawn.game.phase.start_setup_phase(config)

            db.session.query(Player).update({Player.ready: True})
            db.session.commit()
            velvet_dawn.game.turns.check_end_turn_case(config)
            self.assertEqual(velvet_dawn.game.phase.get_phase(), Phase.GAME)

    def test_check_end_turn_case_in_game_from_time(self):
        """ Test if the turn should end """
        with app.app_context():
            test_config = Config()
            test_config.turn_time = 1

            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")
            velvet_dawn.game.phase.start_game_phase()
            velvet_dawn.game.turns._update_turn_start_time()
            self.assertEqual(
                velvet_dawn.players.get_player("player1").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

            time.sleep(2)
            velvet_dawn.game.turns.check_end_turn_case(test_config)
            self.assertEqual(
                velvet_dawn.players.get_player("player2").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

    def test_check_end_turn_case_in_game_when_ready(self):
        """ Test if the turn should end """
        with app.app_context():
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")
            velvet_dawn.game.phase.start_game_phase()

            self.assertEqual(
                velvet_dawn.players.get_player("player1").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

            db.session.query(Player).where(Player.name == "player1").update({Player.ready: True})
            db.session.commit()
            velvet_dawn.game.turns.check_end_turn_case(config)
            self.assertEqual(
                velvet_dawn.players.get_player("player2").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

    def test_begin_next_turn_resets_entity_movement(self):
        """ Test that when a turn begins the entity movement is set to it's range """
        with app.app_context():
            test_config = Config().load()
            test_config.seed = 0

            # Setup the game state
            velvet_dawn.datapacks.init(test_config)
            velvet_dawn.map.new(test_config)
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.game.phase._set_phase(Phase.Lobby)
            velvet_dawn.game.setup.update_setup("civil-war:commander", 1)
            velvet_dawn.game.phase.start_setup_phase(test_config)
            velvet_dawn.game.setup.place_entity("player1", "civil-war:commander", test_config.map_width // 2, 0)

            unit = velvet_dawn.units.list("player1")[0]
            self.assertEqual(0, unit.get_attribute("movement.remaining", _type=int))

            velvet_dawn.game.phase.start_game_phase()

            self.assertEqual(
                unit.get_attribute("movement.remaining", _type=int),
                unit.get_attribute("movement.range", _type=int)
            )

    def test_begin_next_turn_and_get_active_turn(self):
        """ This will test getting the active turn and beginning a new turn """
        with app.app_context():
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")
            self.assertIsNone(velvet_dawn.game.turns.get_active_turn(Phase.Setup))

            velvet_dawn.game.phase.start_game_phase()

            self.assertEqual(
                velvet_dawn.players.get_player("player1").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

            velvet_dawn.game.turns.ready("player1")

            velvet_dawn.game.turns.begin_next_turn()

            players = velvet_dawn.players.list()
            for player in players:
                self.assertFalse(player.ready)

            self.assertEqual(
                velvet_dawn.players.get_player("player2").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

            velvet_dawn.game.turns.begin_next_turn()

            self.assertEqual(
                velvet_dawn.players.get_player("player1").team,
                velvet_dawn.game.turns.get_active_turn(Phase.GAME)
            )

    def test_check_all_players_ready_during_setup(self):
        with app.app_context():
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")
            velvet_dawn.players.join("player3", "password")

            velvet_dawn.game.turns.ready("player1")
            self.assertFalse(velvet_dawn.game.turns._check_all_players_ready(Phase.Setup))
            velvet_dawn.game.turns.ready("player2")
            self.assertFalse(velvet_dawn.game.turns._check_all_players_ready(Phase.Setup))
            velvet_dawn.game.turns.ready("player3")
            self.assertTrue(velvet_dawn.game.turns._check_all_players_ready(Phase.Setup))

            velvet_dawn.game.phase.start_game_phase()

            velvet_dawn.game.turns.ready("player2")
            self.assertFalse(velvet_dawn.game.turns._check_all_players_ready(Phase.GAME))
            velvet_dawn.game.turns.ready("player3")
            self.assertFalse(velvet_dawn.game.turns._check_all_players_ready(Phase.GAME))
            velvet_dawn.game.turns.ready("player1")
            self.assertTrue(velvet_dawn.game.turns._check_all_players_ready(Phase.GAME))

    def test_ready_setup_placed_commander(self):
        with app.app_context():
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.game.phase._set_phase(Phase.Setup)

            # No commanders played so can't ready up
            with self.assertRaises(errors.ValidationError):
                velvet_dawn.game.turns.ready("player1")

    def test_ready_unready(self):
        with app.app_context():
            velvet_dawn.players.join("player1", "password")
            velvet_dawn.players.join("player2", "password")

            velvet_dawn.game.turns.ready("player1")
            self.assertTrue(velvet_dawn.players.get_player("player1").ready)
            self.assertFalse(velvet_dawn.players.get_player("player2").ready)

            velvet_dawn.game.turns.ready("player2")
            self.assertTrue(velvet_dawn.players.get_player("player1").ready)
            self.assertTrue(velvet_dawn.players.get_player("player2").ready)

            velvet_dawn.game.turns.unready("player1")
            self.assertFalse(velvet_dawn.players.get_player("player1").ready)
            self.assertTrue(velvet_dawn.players.get_player("player2").ready)

            velvet_dawn.game.turns.unready("player2")
            self.assertFalse(velvet_dawn.players.get_player("player1").ready)
            self.assertFalse(velvet_dawn.players.get_player("player2").ready)

    def test_update_turn_start_time(self):
        with app.app_context():
            self.assertIsNone(velvet_dawn.dao.get_value(Keys.TURN_START))

            updated_time = velvet_dawn.game.turns._update_turn_start_time()
            self.assertEqual(round(updated_time), round(velvet_dawn.dao.get_value(Keys.TURN_START, _type=float)))

    def test_current_turn_time(self):
        with app.app_context():
            config = Config()

            config.turn_time = 10
            self.assertEqual(10, velvet_dawn.game.turns._current_turn_time(config, Phase.GAME))

            config.turn_time = 500
            self.assertEqual(500, velvet_dawn.game.turns._current_turn_time(config, Phase.GAME))

            # Test setup is always 5 mins
            config.setup_time = 5
            self.assertEqual(5, velvet_dawn.game.turns._current_turn_time(config, Phase.Setup))