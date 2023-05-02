package velvetdawn.core.entities;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.upgrades.Upgrade;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class Upgrades {

    private final EntityInstance entity;
    private final VelvetDawn velvetDawn;

    public Set<String> upgradedIds = new HashSet<>();

    public Upgrades(VelvetDawn velvetDawn, EntityInstance entity) {
        this.velvetDawn = velvetDawn;
        this.entity = entity;
    }

    /** Verify an upgrade and, if possible, run the upgrade
     * 
     * @param upgradeId The upgrade id to upgrade the entity with
     * @throws Exception Throws exceptions if the upgrade can't be performed
     */
    public void upgrade(String upgradeId) throws Exception {
        var entityUpgrades = velvetDawn.datapacks.entities.get(this.entity.datapackId).upgrades;
        var upgrade = entityUpgrades.getById(upgradeId);
        if (upgrade == null)
            throw new Exception(String.format("No upgrade found for entity %s: %s", this.entity.datapackId, upgradeId));

        if (this.upgradedIds.contains(upgrade.id))
            throw new Exception("This entity already has this upgrade.");
        
        // Test for missing requirments
        var missingRequirements = upgrade.requires
                .stream()
                .filter(x -> !this.upgradedIds.contains(x))
                .collect(Collectors.toList());
        if (!missingRequirements.isEmpty()) {
            var requirement = entityUpgrades.getById(missingRequirements.get(0));
            var requirementName = requirement != null ? requirement.name : missingRequirements.get(0);
            throw new Exception(String.format("Requires: '%s'", requirementName));
        }

        // Check is not hidden
        var hidden = upgrade.isHidden(this.entity);
        if (hidden.isTrue) 
            throw new Exception(String.format("Cannot run upgrade. %s", hidden.reason));

        // Check is not disabled
        var enabled = upgrade.isEnabled(this.entity);
        if (!enabled.isTrue)
            throw new Exception(String.format("Cannot run upgrade. %s", enabled.reason));

        // Run the upgrade
        upgrade.run(this.entity);
        this.upgradedIds.add(upgrade.id);
    }
    
    /** Get the breakdown of upgrades that are hidden / disabled
     or already used */
    public EntityUpgradeData getUpgradeUpdates() {
        var upgrades = new EntityUpgradeData(this.entity.instanceId);

        var unitDefinition = velvetDawn.datapacks.entities.get(this.entity.datapackId);
        if (unitDefinition == null)
            return upgrades;

        // Iterate through all upgrades to find which can/can't be run
        for (Upgrade upgrade: unitDefinition.upgrades.upgrades.values()) {
            if (this.upgradedIds.contains(upgrade.id)) {
                upgrades.upgraded.add(upgrade.id);
                continue;
            }

            // Check if all requirements are upgraded
            var missingRequirements = upgrade.requires.stream().filter(x -> !this.upgradedIds.contains(x)).collect(Collectors.toList());
            if (!missingRequirements.isEmpty()) {
                var requirement = unitDefinition.upgrades.getById(missingRequirements.get(0));
                var requirementName = requirement != null ? requirement.name : missingRequirements.get(0);

                upgrades.missingRequirements.add(new NotUpgradable(
                        upgrade.id, String.format("Requires: '%s'", requirementName)));
                continue;
            }

            // Check if not hidden
            var hidden = upgrade.isHidden(this.entity);
            if (hidden.isTrue) {
                upgrades.hidden.add(new NotUpgradable(upgrade.id, hidden.reason));
                continue;
            }

            // Check if enabled
            var isEnabled = upgrade.isEnabled(this.entity);
            if (!isEnabled.isTrue) {
                upgrades.disabled.add(new NotUpgradable(upgrade.id, isEnabled.reason));
                continue;
            }

            upgrades.upgrades.add(upgrade.id);
        }

        return upgrades;
    }

    private static class NotUpgradable {

        public final String upgradeId;
        public final String reason;

        public NotUpgradable(String upgradeId, String reason) {
            this.upgradeId = upgradeId;
            this.reason = reason;
        }

        public AnyJson json() {
            return new AnyJson()
                    .set("upgradeId", this.upgradeId)
                    .set("reason", this.reason);
        }
    }

    public static class EntityUpgradeData {
        
        private final String instanceId;

        public final List<String> upgraded = new ArrayList<>();
        public final List<NotUpgradable> hidden = new ArrayList<>();
        public final List<NotUpgradable> disabled = new ArrayList<>();
        public final List<String> upgrades = new ArrayList<>();
        public final List<NotUpgradable> missingRequirements = new ArrayList<>();
        
        public EntityUpgradeData(String instanceId) {
            this.instanceId = instanceId;
        }

        public AnyJson json() {
            return new AnyJson()
                    .set("instance", this.instanceId)
                    .set("upgraded", AnyList.of(this.upgraded))
                    .set("hidden", new AnyList(this.hidden.stream().map(NotUpgradable::json).collect(Collectors.toList())))
                    .set("disabled", new AnyList(this.disabled.stream().map(NotUpgradable::json).collect(Collectors.toList())))
                    .set("missingRequirements", new AnyList(this.missingRequirements.stream().map(NotUpgradable::json).collect(Collectors.toList())))
                    .set("upgrades", AnyList.of(this.upgrades));
        }
    }
}
