import velvet_dawn.datapacks
from velvet_dawn.dao import app
from test.base_test import BaseTest
from velvet_dawn.dao.models.world_instance import WorldInstance

""" Test all triggers are executed correctly

Units and tiles will be assigned a trigger then
a test is performed to check that trigger was
executed.
"""


def set_commander_trigger(trigger_name: str):
    """ Assign a trigger on the given trigger name """
    velvet_dawn.datapacks.entities['testing:commander'].triggers._triggers[trigger_name] = [
        velvet_dawn.mechanics.actions.get_action("0", {
            "modify": "self.health",
            "set": 0.1
        })
    ]


def set_commander_tile_trigger(trigger_name: str):
    """ Assign a trigger to a tile on the given trigger name """
    velvet_dawn.datapacks.entities['testing:commander'].triggers._triggers[trigger_name] = [
        velvet_dawn.mechanics.actions.get_action("0", {
            "modify": "tile.test",
            "set": 0.1
        })
    ]


# TODO Finish tests here when targeting and combat is complete


class TestTriggers(BaseTest):

    def test_trigger_turn(self):
        with app.app_context():
            self.prepare_game()
            set_commander_trigger('turn')
            WorldInstance().remove_tag("tag:turn-trigger-ran")

            unit = velvet_dawn.units.list()[0]
            self.assertNotEqual(0.1, unit.get_attribute("health"))

            # Begin turn should trigger the health update
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, unit.get_attribute("health"))
            self.assertTrue(WorldInstance().has_tag("tag:turn-trigger-ran"))

    def test_trigger_turn_end(self):
        with app.app_context():
            self.prepare_game()
            set_commander_trigger('turn-end')
            WorldInstance().remove_tag("tag:turn-end-trigger-ran")

            unit = velvet_dawn.units.list()[0]
            self.assertNotEqual(0.1, unit.get_attribute("health"))

            # On turn end will update the health
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, unit.get_attribute("health"))
            self.assertTrue(WorldInstance().has_tag("tag:turn-end-trigger-ran"))

    def test_trigger_friendly_turn(self):
        with app.app_context():
            self.setup_game()
            set_commander_trigger('friendly-turn')

            player_a_commander = velvet_dawn.units.list()[0]
            player_b_commander = velvet_dawn.units.list()[2]

            self.assertNotEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertNotEqual(0.1, player_b_commander.get_attribute("health"))

            # On turn end will start player_b's turn so player_a will not update
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertNotEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertEqual(0.1, player_b_commander.get_attribute("health"))

            # Back to player a
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertEqual(0.1, player_b_commander.get_attribute("health"))

    def test_trigger_friendly_turn_end(self):
        with app.app_context():
            self.setup_game()
            set_commander_trigger('friendly-turn-end')

            player_a_commander = velvet_dawn.units.list()[0]
            player_b_commander = velvet_dawn.units.list()[2]

            self.assertNotEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertNotEqual(0.1, player_b_commander.get_attribute("health"))

            # On turn end will end player_a's turn so player_b will not update
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertNotEqual(0.1, player_b_commander.get_attribute("health"))

            # End player_b
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertEqual(0.1, player_b_commander.get_attribute("health"))

    def test_trigger_enemy_turn(self):
        with app.app_context():
            self.setup_game()
            set_commander_trigger('enemy-turn')

            player_a_commander = velvet_dawn.units.list()[0]
            player_b_commander = velvet_dawn.units.list()[2]

            self.assertNotEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertNotEqual(0.1, player_b_commander.get_attribute("health"))

            # On turn end will start player_b's so player_a's (enemy turn) will begin
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertNotEqual(0.1, player_b_commander.get_attribute("health"))

            # Back to player a
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertEqual(0.1, player_b_commander.get_attribute("health"))

    def test_trigger_enemy_turn_end(self):
        with app.app_context():
            self.setup_game()
            set_commander_trigger('enemy-turn-end')

            player_a_commander = velvet_dawn.units.list()[0]
            player_b_commander = velvet_dawn.units.list()[2]

            self.assertNotEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertNotEqual(0.1, player_b_commander.get_attribute("health"))

            # On turn end will end player_a's so player_b's (enemy turn) will end
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertNotEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertEqual(0.1, player_b_commander.get_attribute("health"))

            # End player_b
            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())

            self.assertEqual(0.1, player_a_commander.get_attribute("health"))
            self.assertEqual(0.1, player_b_commander.get_attribute("health"))

    def test_trigger_enter(self):
        with app.app_context():
            self.setup_game()
            set_commander_tile_trigger('enter')

            commander = velvet_dawn.units.list()[0]
            player = velvet_dawn.players.get_player(commander.player)

            velvet_dawn.units.movement.move(
                player, commander.id, [
                    {"x": commander.x, "y": commander.y},
                    {"x": commander.x + 1, "y": commander.y}
                ], self.get_test_config()
            )

            new_tile = velvet_dawn.map.get_tile(commander.x, commander.y)
            self.assertEqual(0.1, new_tile.get_attribute("test"))

    def test_trigger_leave(self):
        with app.app_context():
            self.setup_game()
            set_commander_tile_trigger('leave')

            commander = velvet_dawn.units.list()[0]
            player = velvet_dawn.players.get_player(commander.player)

            velvet_dawn.units.movement.move(
                player, commander.id, [
                    {"x": commander.x, "y": commander.y},
                    {"x": commander.x + 1, "y": commander.y}
                ], self.get_test_config()
            )

            new_tile = velvet_dawn.map.get_tile(commander.x - 1, commander.y)
            self.assertEqual(0.1, new_tile.get_attribute("test"))

    def test_trigger_spawn(self):
        with app.app_context():
            config = self.get_test_config()
            config.seed = 0
            velvet_dawn.datapacks.init(config)

            set_commander_trigger('spawn')

            velvet_dawn.map.creation.new(config)
            velvet_dawn.players.join("player1", "")
            velvet_dawn.players.join("player2", "")
            velvet_dawn.game.setup.update_setup("testing:commander", 1)
            velvet_dawn.game.phase.start_setup_phase(config)
            velvet_dawn.game.setup.place_entity("player1", "testing:commander", 15, 0, config)

            commander = velvet_dawn.units.list()[0]
            self.assertEqual(0.1, commander.get_attribute("health"))

    def test_trigger_game_begin(self):
        with app.app_context():
            config = self.get_config()
            config.seed = 0
            velvet_dawn.datapacks.init(config)

            set_commander_trigger('game')

            velvet_dawn.map.creation.new(config)
            velvet_dawn.players.join("player1", "")
            velvet_dawn.players.join("player2", "")
            velvet_dawn.game.setup.update_setup("testing:commander", 1)
            velvet_dawn.game.phase.start_setup_phase(config)
            velvet_dawn.game.setup.place_entity("player1", "testing:commander", 6, 0, config)
            velvet_dawn.game.phase.start_game_phase(config)

            commander = velvet_dawn.units.list()[0]
            self.assertEqual(0.1, commander.get_attribute("health"))
            self.assertTrue(WorldInstance().has_tag("tag:game-trigger-ran"))

    def test_trigger_round_begin(self):
        with app.app_context():
            self.prepare_game()
            WorldInstance().remove_tag("tag:round-trigger-ran")

            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())
            self.assertFalse(WorldInstance().has_tag("tag:round-trigger-ran"))

            velvet_dawn.game.turns.begin_next_turn(self.get_test_config())
            self.assertTrue(WorldInstance().has_tag("tag:round-trigger-ran"))

    # def test_trigger_death(self):
    #     with app.app_context():
    #         self.assertTrue(False)
    #
    # def test_trigger_kill(self):
    #     with app.app_context():
    #         self.assertTrue(False)
    #
    # def test_trigger_attack(self):
    #     with app.app_context():
    #         self.assertTrue(False)
    #
    # def test_trigger_attacked(self):
    #     with app.app_context():
    #         self.assertTrue(False)

    # def test_trigger_target(self):
    #     with app.app_context():
    #         self.assertTrue(False)
    #
    # def test_trigger_targeted(self):
    #     with app.app_context():
    #         self.assertTrue(False)
