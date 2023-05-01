package velvetdawn.core.models.instances.entities;

import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;

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
    }
}
