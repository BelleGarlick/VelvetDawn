package velvetdawn.mechanics.upgrades;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.actions.Action;
import velvetdawn.mechanics.actions.Actions;
import velvetdawn.mechanics.conditionals.Conditional;
import velvetdawn.mechanics.conditionals.Conditionals;
import velvetdawn.models.ActionRunnableReason;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.instances.Instance;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Upgrade {

    private static final Set<String> ValidKeys = Set.of(
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

    public List<String> requires = new ArrayList<>();

    public Upgrade(String upgradeId, String name, String icon, String description) {
        this.id = upgradeId;
        this.name = name;
        this.icon = icon;
        this.description = description;
    }

    public AnyJson toJson() {
        return new AnyJson()
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
    public static Upgrade fromJson(VelvetDawn velvetDawn, String parentId, int upgradeNumber, AnyJson data) throws Exception {
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

        String description = null;
        if (data.containsKey("description"))
            description = data.get("description")
                    .validateInstanceIsString("Upgrade description must be a string or null")
                    .toString();

        String icon = null;
        if (data.containsKey("icon"))
            icon = data.get("icon")
                    .validateInstanceIsString(String.format("%s has upgrade with missing/invalid icon.", parentId))
                    .toString();

        var upgrade = new Upgrade(upgradeId, upgradeName, icon, description);

        if (!velvetDawn.datapacks.resources.containsKey(upgrade.icon))
            System.out.printf("[WARN] %s upgrade has missing icon '%s'%n", parentId, upgrade.icon);

        // Parse enabled conditions
        var errorMessage = String.format("Upgrade enabled in %s is invalid. Enabled attributes must be a list of conditions.", parentId);
        var enabledConditions = data.get("enabled", Any.list()).validateInstanceIsList(errorMessage);
        for (Any json: enabledConditions.items)
            upgrade.enabled.add(Conditionals.get(velvetDawn, parentId, json.validateInstanceIsJson(errorMessage)));

        // Parse hidden conditions
        errorMessage = String.format("Upgrade hidden in %s is invalid. Hidden attributes must be a list of conditions.", parentId);
        var hiddenConditions = data.get("hidden", Any.list()).validateInstanceIsList(errorMessage);
        for (Any json: hiddenConditions.items)
            upgrade.hidden.add(Conditionals.get(velvetDawn, parentId, json.validateInstanceIsJson(errorMessage)));

        // Parse actions
        errorMessage = String.format("Upgrade actions in %s is invalid. Actions must be a list of action objects.", parentId);
        var upgradeActions = data.get("actions", Any.list()).validateInstanceIsList(errorMessage);
        for (Any json: upgradeActions.items)
            upgrade.actions.add(Actions.fromJson(velvetDawn, parentId, json.validateInstanceIsJson(errorMessage)));

        // Upgrade requirements
        errorMessage = String.format("Upgrade requirements (in %s) must be a list of strings.", parentId);
        var requirements = data.get("requires", Any.list()).validateInstanceIsList(errorMessage);
        for (Any item: requirements.items)
            upgrade.requires.add(item.validateInstanceIsString(errorMessage).toString());

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
            if (condition.isTrue(instance))
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
