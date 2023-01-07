from typing import Tuple

import velvet_dawn
from test.base_test import BaseTest
from velvet_dawn import errors
from velvet_dawn.config import Config
from velvet_dawn.dao import app, db
from velvet_dawn.dao.models import TileInstance
from velvet_dawn.models import Phase


""" Test the entities movement is validated correctly on the server """


def setup_game() -> Tuple[Config, Tuple[int, int]]:
    test_config = Config().load()
    test_config.seed = 3

    entity_position = test_config.map_width // 2, 0

    # Setup the game state
    velvet_dawn.datapacks.init(test_config)
    velvet_dawn.map.new(test_config)
    velvet_dawn.players.join("player1", "password")
    velvet_dawn.players.join("player2", "password")
    velvet_dawn.game.phase._set_phase(Phase.Lobby)
    velvet_dawn.game.setup.update_setup("civil-war:commander", 1)
    velvet_dawn.game.phase.start_setup_phase(test_config)
    velvet_dawn.game.setup.place_entity("player1", "civil-war:commander", entity_position[0], entity_position[1], test_config)
    velvet_dawn.game.setup.place_entity("player2", "civil-war:commander", entity_position[0], 18, test_config)
    velvet_dawn.game.phase.start_game_phase(test_config)

    return test_config, entity_position


class TestUnitMovement(BaseTest):

    def test_move(self):
        with app.app_context():
            test_config, entity_position = setup_game()

            player1 = velvet_dawn.players.list()[0]
            entity, player2entity = velvet_dawn.units.list()
            first_pos = {'x': entity_position[0], 'y': entity_position[1]}

            velvet_dawn.game.phase._set_phase(Phase.Lobby)
            with self.assertRaises(errors.GamePhaseError):
                velvet_dawn.units.movement.move(player1, entity.id, [
                    {'x': first_pos['x'], 'y': first_pos['y']},
                    {'x': first_pos['x'], 'y': first_pos['y'] + 1},
                ], test_config)
            velvet_dawn.game.phase._set_phase(Phase.GAME)

            velvet_dawn.game.turns.begin_next_turn(test_config)
            with self.assertRaises(errors.InvalidTurnError):
                velvet_dawn.units.movement.move(player1, entity.id, [
                    {'x': first_pos['x'], 'y': first_pos['y']},
                    {'x': first_pos['x'], 'y': first_pos['y'] + 1},
                ], test_config)
            velvet_dawn.game.turns.begin_next_turn(test_config)

            with self.assertRaises(errors.ItemNotFoundError):
                velvet_dawn.units.movement.move(player1, -1, [
                    {'x': first_pos['x'], 'y': test_config.map_height - 1},
                    {'x': first_pos['x'], 'y': test_config.map_height - 2},
                ], test_config)

            with self.assertRaises(errors.ValidationError):
                velvet_dawn.units.movement.move(player1, player2entity.id, [
                    {'x': first_pos['x'], 'y': test_config.map_height - 1},
                    {'x': first_pos['x'], 'y': test_config.map_height - 2},
                ], test_config)

            velvet_dawn.units.movement.move(player1, entity.id, [
                {'x': first_pos['x'], 'y': first_pos['y']},
                {'x': first_pos['x'], 'y': first_pos['y'] + 1},
            ], test_config)
            unit = velvet_dawn.units.get_unit_by_id(entity.id)
            self.assertEqual(2, unit.get_attribute("movement.remaining"))

            self.assertEqual(unit.x, first_pos['x'])
            self.assertEqual(unit.y, first_pos['y'] + 1)

    def test_validate_entity_traversing_path(self):
        with app.app_context():
            test_config, entity_position = setup_game()
            entity = velvet_dawn.units.list()[0]

            # Test invalid start tile
            with self.assertRaises(errors.EntityMovementErrorInvalidStartPos):
                velvet_dawn.units.movement._validate_entity_traversing_path(entity, [{'x': 0, 'y': 0}], test_config)

            # Test empty tile in sequence
            first_pos = {'x': entity_position[0], 'y': entity_position[1]}
            with self.assertRaises(errors.EntityMovementErrorInvalidItem):
                velvet_dawn.units.movement._validate_entity_traversing_path(entity, [first_pos, {'x': -1, 'y': 0}], test_config)

            # Test tiles not neighbours
            with self.assertRaises(errors.EntityMovementErrorNotNeighbours):
                velvet_dawn.units.movement._validate_entity_traversing_path(entity, [first_pos, {'x': 0, 'y': 0}], test_config)

            # Test unknown tile error
            tile = velvet_dawn.map.get_tile(first_pos['x'] - 1, first_pos['y'])
            db.session.query(TileInstance)\
                .where(TileInstance.x == tile.x, TileInstance.y == tile.y)\
                .update({TileInstance.tile_id: "unknown_tile"})
            db.session.commit()
            with self.assertRaises(errors.UnknownTile):
                velvet_dawn.units.movement._validate_entity_traversing_path(entity, [
                    first_pos,
                    {'x': first_pos['x'] - 1, 'y': first_pos['y']}
                ], test_config)

            # Test tile not traversable
            tile = velvet_dawn.map.get_tile(first_pos['x'] + 1, first_pos['y'])
            tile.set_attribute("movement.traversable", False)
            self.assertFalse(tile.get_attribute("movement.traversable"))
            with self.assertRaises(errors.EntityMovementErrorTileNotTraversable):
                velvet_dawn.units.movement._validate_entity_traversing_path(entity, [
                    first_pos,
                    {'x': first_pos['x'] + 1, 'y': first_pos['y']}
                ], test_config)

            # Too long
            with self.assertRaises(errors.EntityMovementErrorTileNoRemainingMoves):
                velvet_dawn.units.movement._validate_entity_traversing_path(entity, [
                    {'x': first_pos['x'], 'y': first_pos['y'] + i}
                    for i in range(10)
                ], test_config)

            # Just right
            remaining_moves = velvet_dawn.units.movement._validate_entity_traversing_path(entity, [
                {'x': first_pos['x'], 'y': first_pos['y']},
                {'x': first_pos['x'], 'y': first_pos['y'] + 1},
                {'x': first_pos['x'], 'y': first_pos['y'] + 2}
            ], test_config)
            self.assertEqual(1, remaining_moves)
