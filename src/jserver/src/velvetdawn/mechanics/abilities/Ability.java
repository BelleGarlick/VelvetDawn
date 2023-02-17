package velvetdawn.mechanics.abilities;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.actions.Action;
import velvetdawn.mechanics.actions.Actions;
import velvetdawn.mechanics.conditionals.Conditional;
import velvetdawn.mechanics.conditionals.Conditionals;
import velvetdawn.models.ActionRunnableReason;
import velvetdawn.models.instances.EntityInstance;
import velvetdawn.models.instances.Instance;
import velvetdawn.utils.Json;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Ability {

    private static Set<String> ValidKeys = Set.of(
            "name", "enabled", "actions",
            "icon", "hidden", "notes", "description"
    );

    public final String id;
    public final String name;
    public final String icon;
    public final String description;

    public final List<Conditional> enabled = new ArrayList<>();
    public final List<Conditional> hidden = new ArrayList<>();
    public final List<Action> actions = new ArrayList<>();

    public Ability(String id, String name, String icon, String description) {
        this.id = id;
        this.name = name;
        this.icon = icon;
        this.description = description;
    }

    public Json toJson() {
        return new Json()
                .set("id", this.id)
                .set("name", this.name)
                .set("icon", this.icon)
                .set("description", this.description);
    }

    /** Load the ability json
     *
     * @param velvetDawn vd instance
     * @param parentId The id of the unit this is applied to
     * @param abilityNumber The index of the ability within abilities, used to generate an id
     * @param data The json data
     * @return The new Ability
     */
    public static Ability fromJson(VelvetDawn velvetDawn, String parentId, int abilityNumber, Json data) throws Exception {
        String id = String.format("%s-ability-%s", parentId, abilityNumber);
        String name = data.get("name")
                .validateInstanceIsString(String.format("Ability name in %s is invalid", parentId))
                .value;
        String description = data.get("description")
                .validateInstanceIsStringOrNull(String.format("Entity description in %s must be a string or null", parentId))
                .toString();
        String icon = data.get("icon")
                .validateInstanceIsStringOrNull(String.format("%s has ability with missing/invalid icon.", parentId))
                .toString();

        var ability = new Ability(id, name, icon, description);

        if (!velvetDawn.datapacks.resources.containsKey(ability.icon))
            System.out.println(String.format("[WARN] %s ability has missing icon '%s'", parentId, ability.icon));

        // Parse hidden conditions
        var hiddenConditions = data.getStrictJsonList("hidden", List.of(), String.format(
                "Ability hidden in %s is invalid. Hidden attributes must be a list of conditions.", parentId));
        for (Json json: hiddenConditions)
            ability.hidden.add(Conditionals.get(velvetDawn, parentId, json));

        // Parse actions
        var abilityActions = data.getStrictJsonList("actions", List.of(), String.format(
                "Ability actions in %s is invalid. Actions must be a list of action objects.", parentId));
        for (Json json: abilityActions)
            ability.actions.add(Actions.fromJson(velvetDawn, parentId, json));

        // check invalid key
        for (String key: data.keys()) {
            if (!ValidKeys.contains(key))
                throw new Exception(String.format("Invalid ability key '%s' (in %s)", key, parentId));
        }

        return ability;
    }

    /** Execute the Ability */
    public void run(Instance instance) throws Exception {
        for (Action action: this.actions)
            action.run(instance);
    }

    /** Check if the ability should be hidden and therefore not ran */
    public ActionRunnableReason isHidden(Instance instance) {
        for (Conditional condition: this.hidden) {
            if (!condition.isTrue(instance))
                return new ActionRunnableReason(true, condition.notTrueReason);
        }

        return new ActionRunnableReason(false);
    }

    /** Check if the ability should be disabled and therefore not ran */
    public ActionRunnableReason isEnabled(EntityInstance instance) {
        for (Conditional condition: this.enabled) {
            if (!condition.isTrue(instance)) {
                return new ActionRunnableReason(true, condition.notTrueReason);
            }
        }

        return new ActionRunnableReason(false);
    }
}
