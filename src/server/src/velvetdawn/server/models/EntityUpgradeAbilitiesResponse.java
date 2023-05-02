package velvetdawn.server.models;

import com.google.gson.JsonObject;
import velvetdawn.core.entities.EntityInstance;

public class EntityUpgradeAbilitiesResponse {

    public JsonObject abilities;
    public JsonObject upgrades;

    private EntityUpgradeAbilitiesResponse(JsonObject abilities, JsonObject upgrades) {
        this.abilities = abilities;
        this.upgrades = upgrades;
    }

    public static Object from(EntityInstance entity) throws Exception {
        return new EntityUpgradeAbilitiesResponse(
                entity.abilities.getAbilityUpdates().json().toGson(),
                entity.upgrades.getUpgradeUpdates().json().toGson());
    }
}
