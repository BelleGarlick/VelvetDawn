package velvetdawn.models.datapacks.entities;

import velvetdawn.models.anytype.AnyNull;
import velvetdawn.utils.Json;

public class EntityTextures {

    // TODO Standard
    // TODO Moving
    // TODO Fighting
    // TODO Movement particles
    // TODO Add proper validation

    private String sprite = null;

    public void fromJson(String parentId, Json parentJson) throws Exception {
        var json = parentJson.getJson("textures", new Json(), "Entity textures must be a json object.");

        var sprite = json.get("background");
        if (!(sprite instanceof AnyNull) )
                this.sprite = sprite
                        .validateInstanceIsString(String.format("Entity sprite %s textures.background must be a string.", parentId))
                        .value;
    }

    public Json toJson() {
        var json = new Json();
        json.set("background", this.sprite);

        return json;
    }
}
