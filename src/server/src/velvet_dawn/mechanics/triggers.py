from typing import Dict, List

import velvet_dawn
from velvet_dawn import errors
from velvet_dawn.db.instances import Instance
from velvet_dawn.mechanics.actions.action import Action


""" Triggers class attached to units and tiles. This
class also parses the given dict of triggers and 
actions given to the class
"""


# TODO implement attack and attacked, spawn, death and kill
# TODO Add validation for this
WORLD_TRIGGERS = ["game", "turn", "turn-end"]
TILE_TRIGGERS = ["enter", "leave", "target", "targeted", "death", "kill", "attack", "attacked"] + WORLD_TRIGGERS
UNIT_TRIGGERS = ["friendly-turn", "friendly-turn-end", "enemy-turn", "enemy-turn-end", "spawn"] + TILE_TRIGGERS


class Triggers:

    def __init__(self):
        self._triggers: Dict[str, List[Action]] = {}

    def load(self, parent_id: str, data: dict):
        """ Parse and load a dict defining triggers and it's
        actions into this class

        Args:
            parent_id: The definition id of the unit or tile
            data: The data defining the unit/tile's triggers
        """
        # Iterate through each key in the dict to check it's valid
        for key in data:
            if key == "notes":
                continue

            if not isinstance(data[key], list):
                raise errors.ValidationError(f"Trigger '{key}' must be a list of actions in '{parent_id}'")

            self._triggers[key] = [
                velvet_dawn.mechanics.actions.get_action(parent_id, item)
                for item in data[key]
            ]

    def _run_trigger(self, trigger_name: str, instance: Instance):
        """ Execute each action in a given list of triggers """
        if trigger_name in self._triggers:
            for action in self._triggers[trigger_name]:
                if action.can_run(instance):
                    action.run(instance)

    def on_turn(self, instance: Instance):
        self._run_trigger("turn", instance)

    def on_turn_end(self, instance: Instance):
        self._run_trigger("turn-end", instance)

    def on_friendly_turn(self, instance: Instance):
        self._run_trigger("friendly-turn", instance)

    def on_friendly_turn_end(self, instance: Instance):
        self._run_trigger("friendly-turn-end", instance)

    def on_enemy_turn(self, instance: Instance):
        self._run_trigger("enemy-turn", instance)

    def on_enemy_turn_end(self, instance: Instance):
        self._run_trigger("enemy-turn-end", instance)

    def on_enter(self, instance: Instance):
        self._run_trigger("enter", instance)

    def on_leave(self, instance: Instance):
        self._run_trigger("leave", instance)

    def on_target(self, instance: Instance):
        self._run_trigger("target", instance)

    def on_targeted(self, instance: Instance):
        self._run_trigger("targeted", instance)

    def on_spawn(self, instance: Instance):
        self._run_trigger("spawn", instance)

    def on_game_start(self, instance: Instance):
        self._run_trigger("game", instance)

    def on_death(self, instance: Instance):
        self._run_trigger("death", instance)

    def on_kill(self, instance: Instance):
        self._run_trigger("kill", instance)

    def on_attack(self, instance: Instance):
        self._run_trigger("attack", instance)

    def on_attacked(self, instance: Instance):
        self._run_trigger("attacked", instance)

    def on_round(self, instance: Instance):
        self._run_trigger("round", instance)
