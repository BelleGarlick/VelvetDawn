package velvetdawn.core.models.datapacks.entities;

import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyNull;

public class EntityTextures {

    // TODO Standard
    // TODO Moving
    // TODO Fighting
    // TODO Movement particles
    // TODO Add proper validation

    public String sprite = null;

    public void fromJson(String parentId, AnyJson parentJson) throws Exception {
        var json = parentJson.get("textures", new AnyJson())
                .validateInstanceIsJson("Entity textures must be a json object.");

        var sprite = json.get("background");
        if (!(sprite instanceof AnyNull) && sprite != null)
                this.sprite = sprite
                        .validateInstanceIsString(String.format("Entity sprite %s textures.background must be a string.", parentId))
                        .value;
    }
}
