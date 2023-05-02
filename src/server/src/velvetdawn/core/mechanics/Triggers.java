package velvetdawn.core.mechanics;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.actions.Action;
import velvetdawn.core.mechanics.actions.Actions;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.Instance;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Triggers {

    /* Triggers class attached to entities and tiles. This
       class also parses the given dict of triggers and
       actions given to the class
     */

    // TODO implement attack and attacked, spawn, death and kill
    // TODO Add validation for this
    Set<String> WORLD_TRIGGERS = Set.of("game", "turn", "turn-end", "round");
    Set<String> TILE_TRIGGERS = Stream.concat(
            Stream.of("enter", "leave", "target", "targeted", "death", "kill", "attack", "attacked"),
            WORLD_TRIGGERS.stream()).collect(Collectors.toSet());
    Set<String> UNIT_TRIGGERS = Stream.concat(
            Stream.of("friendly-turn", "friendly-turn-end", "enemy-turn", "enemy-turn-end", "spawn"),
            TILE_TRIGGERS.stream()).collect(Collectors.toSet());

    public final Map<String, List<Action>> triggers = new HashMap<>();

    /** Parse and load a dict defining triggers and it's
     * actions into this class
     *
     * @param parentId The definition id of the entity or tile
     * @param data The data defining the entity/tile's triggers
     */
    public void load(VelvetDawn velvetDawn, String parentId, AnyJson data) throws Exception {
        // Iterate through each key in the dict to check it 's valid
        for (String key: data.keys()) {
            if (key.equals("notes"))
                continue;

            if (!UNIT_TRIGGERS.contains(key))
                throw new Exception(String.format("Invalid trigger key '%s'", key));

            var errorMessage = String.format("Trigger '%s' must be a list of actions", key);
            var jsonActions = data.get(key, Any.list()).validateInstanceIsList(errorMessage);
            List<Action> actions = new ArrayList<>();
            for (Any action: jsonActions.items) {
                actions.add(Actions.fromJson(velvetDawn, parentId, action.validateInstanceIsJson(errorMessage)));
            }

            this.triggers.put(key, actions);
        }
    }

    /** Execute each action in a given list of triggers */
    private void runTrigger(String triggerName, Instance instance) throws Exception {
        if (this.triggers.containsKey(triggerName)) {
            for (Action action: this.triggers.get(triggerName)) {
                if (action.canRun(instance))
                    action.run(instance);
            }
        }
    }

    public void onTurn(Instance instance) throws Exception {
        this.runTrigger("turn", instance);
    }

    public void onTurnEnd(Instance instance) throws Exception {
        this.runTrigger("turn-end", instance);
    }

    public void onFriendlyTurn(Instance instance) throws Exception {
        this.runTrigger("friendly-turn", instance);
    }

    public void onFriendlyTurnEnd(Instance instance) throws Exception {
        this.runTrigger("friendly-turn-end", instance);
    }

    public void onEnemyTurn(Instance instance) throws Exception {
        this.runTrigger("enemy-turn", instance);
    }

    public void onEnemyTurnEnd(Instance instance) throws Exception {
        this.runTrigger("enemy-turn-end", instance);
    }

    public void onEnter(Instance instance) throws Exception {
        this.runTrigger("enter", instance);
    }

    public void onLeave(Instance instance) throws Exception {
        this.runTrigger("leave", instance);
    }

    public void onTarget(Instance instance) throws Exception {
        this.runTrigger("target", instance);
    }

    public void onTargeted(Instance instance) throws Exception {
        this.runTrigger("targeted", instance);
    }

    public void onSpawn(Instance instance) throws Exception {
        this.runTrigger("spawn", instance);
    }

    public void onGameStart(Instance instance) throws Exception {
        this.runTrigger("game", instance);
    }

    public void onDeath(Instance instance) throws Exception {
        this.runTrigger("death", instance);
    }

    public void onKill(Instance instance) throws Exception {
        this.runTrigger("kill", instance);
    }

    public void onAttack(Instance instance) throws Exception {
        this.runTrigger("attack", instance);
    }

    public void onAttacked(Instance instance) throws Exception {
        this.runTrigger("attacked", instance);
    }

    public void onRound(Instance instance) throws Exception {
        this.runTrigger("round", instance);
    }
}
