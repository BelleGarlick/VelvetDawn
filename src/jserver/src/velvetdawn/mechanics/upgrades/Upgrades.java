package velvetdawn.mechanics.upgrades;

import velvetdawn.VelvetDawn;
import velvetdawn.utils.Json;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Upgrades {

    private Map<String, Upgrade> upgrades = new HashMap<>();

    /** Get upgrade by it's id */
    public Upgrade getById(String upgradeId) {
        return upgrades.get(upgradeId);
    }

    public List<Json> toJson() {
        return this.upgrades.values().stream()
                .map(Upgrade::toJson)
                .collect(Collectors.toList());
    }

    /** Parse the upgrades list */
    public void load(VelvetDawn velvetDawn, String parentId, List<Json> data) throws Exception {
        for (int i = 0; i < data.size(); i++) {
            var upgrade = Upgrade.fromJson(velvetDawn, parentId, i, data.get(i));
            this.upgrades.put(upgrade.id, upgrade);
        }
    }
}
