package velvetdawn.models.instances;

import velvetdawn.models.Coordinate;
import velvetdawn.models.anytype.Any;

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
