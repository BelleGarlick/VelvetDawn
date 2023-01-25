import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn.db.instances import WorldInstance
from velvet_dawn.db.models import Phase
from velvet_dawn.logger import logger
from velvet_dawn.dao.models import Player


def start_setup_phase(config: Config):
    logger.info("Starting setup phase.")
    velvet_dawn.map.allocate_spawn_points(config)
    velvet_dawn.game.turns._update_turn_start_time()
    velvet_dawn.db.key_values.set_phase(Phase.Setup)

    db.session.query(Player).update({Player.ready: False})
    db.session.commit()

    # TODO Check game setup is valid before people start placing


def start_game_phase(config: Config):
    logger.info("Starting game")
    velvet_dawn.db.key_values.set_phase(Phase.GAME)

    # Trigger game start
    for unit in velvet_dawn.units.list():
        velvet_dawn.datapacks.entities[unit.entity_id].triggers.on_game_start(unit)
    for tile in velvet_dawn.db.tiles.all():
        velvet_dawn.datapacks.tiles[tile.tile_id].triggers.on_game_start(tile)
    velvet_dawn.datapacks.world.triggers.on_game_start(WorldInstance())

    velvet_dawn.game.turns.begin_next_turn(config)


    # TODO if players haven't got a commander, move them to spectators

    # TODO Trigger entities on game start
    # TODO If game mode is CTF then trigger stuff here
