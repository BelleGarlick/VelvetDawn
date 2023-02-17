package velvetdawn.mechanics.upgrades;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.actions.Action;
import velvetdawn.mechanics.actions.Actions;
import velvetdawn.mechanics.conditionals.Conditional;
import velvetdawn.mechanics.conditionals.Conditionals;
import velvetdawn.models.ActionRunnableReason;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.instances.Instance;
import velvetdawn.utils.Json;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Upgrade {

    private static Set<String> ValidKeys = Set.of(
            "id", "name", "enabled", "requires", "actions",
            "icon", "hidden", "notes", "description"
    );

    public final String id;
    public final String name;
    public final String icon;
    public final String description;

    private final List<Conditional> enabled = new ArrayList<>();
    private final List<Conditional> hidden = new ArrayList<>();
    private final List<Action> actions = new ArrayList<>();

    private List<String> requires = new ArrayList<>();

    public Upgrade(String upgradeId, String name, String icon, String description) {
        this.id = upgradeId;
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

    /** Parse a json object for an upgrade
     *
     * @param parentId The datapackId of the item the upgrade is attached to.
     * @param upgradeNumber The index of the upgrade on the parent, used to
     *                      automatically provide an id.
     * @param data The json object to load from.
     */
    public static Upgrade fromJson(VelvetDawn velvetDawn, String parentId, int upgradeNumber, Json data) throws Exception {
        // TODO TEst what happens if the value is not a string
        // Parse the id
        String upgradeId = data.get("id", Any.from(String.format("%s-upgrade-%s", parentId, upgradeNumber)))
                .validateInstanceIsString(String.format("Upgrade in %s ID must be a string", parentId))
                .value;

        // TODO Test what happens if not a string
        // Parse upgrade name
        String upgradeName = data.get("name")
                .validateInstanceIsString(String.format("%s has invalid upgrade name.", parentId))
                .value;

        String description = data.get("description")
                .validateInstanceIsStringOrNull("Upgrade description must be a string or null")
                .toString();

        String icon = data.get("icon")
                .validateInstanceIsStringOrNull(String.format("%s has upgrade with missing/invalid icon.", parentId))
                .toString();

        var upgrade = new Upgrade(upgradeId, upgradeName, icon, description);

        if (!velvetDawn.datapacks.resources.containsKey(upgrade.icon))
            System.out.println(String.format("[WARN] %s upgrade has missing icon '%s'", parentId, upgrade.icon));

        // Parse enabled conditions
        var enabledConditions = data.getStrictJsonList("enabled", List.of(), String.format(
                "Upgrade enabled in %s is invalid. Enabled attributes must be a list of conditions.", parentId));
        for (Json json: enabledConditions)
            upgrade.enabled.add(Conditionals.get(velvetDawn, parentId, json));

        // Parse hidden conditions
        var hiddenConditions = data.getStrictJsonList("hidden", List.of(), String.format(
                "Upgrade hidden in %s is invalid. Hidden attributes must be a list of conditions.", parentId));
        for (Json json: hiddenConditions)
            upgrade.hidden.add(Conditionals.get(velvetDawn, parentId, json));

        // Parse actions
        var upgradeActions = data.getStrictJsonList("actions", List.of(), String.format(
                "Upgrade actions in %s is invalid. Actions must be a list of action objects.", parentId));
        for (Json json: upgradeActions)
            upgrade.actions.add(Actions.fromJson(velvetDawn, parentId, json));

        // Upgrade requirements
        upgrade.requires = data.getStringList("requires", List.of(),
                String.format("Upgrade requirements (in %s) must be a list of strings. Found '%s'.",
                        parentId, upgrade.requires));

        // check invalid key
        for (String key: data.keys()) {
            if (!ValidKeys.contains(key))
                throw new Exception(String.format("Invalid upgrade key '%s' (in %s)", key, parentId));
        }

        return upgrade;
    }

    /** Execute the upgrade */
    public void run(Instance instance) throws Exception {
        for (Action action: this.actions)
            action.run(instance);
    }

    /** Check if the upgrade should be hidden and therefore not ran */
    public ActionRunnableReason isHidden(Instance instance) {
        for (Conditional condition: this.hidden) {
            if (!condition.isTrue(instance))
                return new ActionRunnableReason(true, condition.notTrueReason);
        }

        return new ActionRunnableReason(false);
    }

    /** Check if the upgrade should be disabled and therefore not ran */
    public ActionRunnableReason isEnabled(Instance instance) {
        for (Conditional condition: this.enabled) {
            if (!condition.isTrue(instance))
                return new ActionRunnableReason(false, condition.notTrueReason);
        }

        return new ActionRunnableReason(true);
    }
}
