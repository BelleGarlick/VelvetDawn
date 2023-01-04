from typing import Dict, List, Union, Type

import velvet_dawn
from velvet_dawn import errors
from velvet_dawn.config import Config
from velvet_dawn.dao.models import UnitInstance, TileInstance
from velvet_dawn.mechanics.actions.action import Action
from velvet_dawn.models import Unit, Tile


""" Triggers class attached to units and tiles. This
class also parses the given dict of triggers and 
actions given to the class
"""


# TODO implement attack and attacked, spawn, death and kill
TILE_TRIGGERS = [
    "turn", "turn-end",
    "enter", "leave",
    "target", "targeted",
    "game-start"
    "death", "kill",
    "attack", "attacked"
]

UNIT_TRIGGERS = ["friendly-turn", "friendly-turn-end", "enemy-turn", "enemy-turn-end", "spawn"] + TILE_TRIGGERS


class Triggers:

    def __init__(self):
        self._triggers: Dict[str, List[Action]] = {}

    def load(self, parent_id: str, parent_type: Union[Type[Unit], Type[Tile]], data: dict):
        """ Parse and load a dict defining triggers and it's
        actions into this class

        Args:
            parent_id: The definition id of the unit or tile
            parent_type: The type of the object attached
            data: The data defining the unit/tile's triggers
        """
        if parent_type == Unit: valid_triggers = UNIT_TRIGGERS
        elif parent_type == Tile: valid_triggers = TILE_TRIGGERS
        else: raise errors.ValidationError(f"Invalid parent type for triggers: {parent_type}.")

        # Iterate through each key in the dict to check it's valid
        for key in data:
            if key == "notes":
                continue

            if key not in valid_triggers:
                raise errors.ValidationError(f"'{key}' is invalid trigger on '{parent_id}'")

            if not isinstance(data[key], list):
                raise errors.ValidationError(f"Trigger '{key}' must be a list of actions in '{parent_id}'")

            self._triggers[key] = [
                velvet_dawn.mechanics.actions.get_action(parent_id, parent_type, item)
                for item in data[key]
            ]

    def _run_trigger(self, trigger_name: str, instance: Union[UnitInstance, TileInstance], config: Config):
        """ Execute each action in a given list of triggers """
        if trigger_name in self._triggers:
            for action in self._triggers[trigger_name]:
                action.run(instance, config)

    def on_turn(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("turn", instance, config)

    def on_turn_end(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("turn-end", instance, config)

    def on_friendly_turn(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("friendly-turn", instance, config)

    def on_friendly_turn_end(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("friendly-turn-end", instance, config)

    def on_enemy_turn(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("enemy-turn", instance, config)

    def on_enemy_turn_end(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("enemy-turn-end", instance, config)

    def on_enter(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("enter", instance, config)

    def on_leave(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("leave", instance, config)

    def on_target(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("target", instance, config)

    def on_targeted(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("targeted", instance, config)

    def on_spawn(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("spawn", instance, config)

    def on_game_start(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("game-start", instance, config)

    def on_death(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("death", instance, config)

    def on_kill(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("kill", instance, config)

    def on_attack(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("attack", instance, config)

    def on_attacked(self, instance: Union[UnitInstance, TileInstance], config: Config):
        self._run_trigger("attacked", instance, config)
