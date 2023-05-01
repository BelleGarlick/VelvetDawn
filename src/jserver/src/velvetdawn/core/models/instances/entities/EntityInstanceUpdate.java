package velvetdawn.core.models.instances.entities;

import com.google.gson.JsonObject;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;

public class EntityInstanceUpdate {

    public String instanceId;
    public Coordinate position;
    public AttributeUpdate attrUpdate;
    public long time;

    public static class AttributeUpdate {

        String key;
        Any value;

        public AttributeUpdate(String key, Any value) {
            this.key = key;
            this.value = value;
        }

        public JsonObject toGson() {
            return new AnyJson()
                    .set("key", this.key)
                    .set("value", this.value)
                    .toGson();
        }
    }
}
