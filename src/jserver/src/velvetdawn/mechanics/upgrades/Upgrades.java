package velvetdawn.mechanics.upgrades;

import velvetdawn.VelvetDawn;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Upgrades {

    public Map<String, Upgrade> upgrades = new HashMap<>();

    /** Get upgrade by it's id */
    public Upgrade getById(String upgradeId) {
        return upgrades.get(upgradeId);
    }

    public AnyList toJson() {
        return (AnyList) this.upgrades.values().stream()
                .map(Upgrade::toJson)
                .collect(Collectors.toList());
    }

    /** Parse the upgrades list */
    public void load(VelvetDawn velvetDawn, String parentId, AnyList data) throws Exception {
        for (int i = 0; i < data.size(); i++) {
            var upgrade = Upgrade.fromJson(velvetDawn, parentId, i, data
                    .get(i)
                    .validateInstanceIsJson(String.format("Error in %s. Upgrades must be a list of json objects.", parentId)));
            this.upgrades.put(upgrade.id, upgrade);
        }
    }
}
