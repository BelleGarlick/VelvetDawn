package velvetdawn.core.models.instances.attributes;

import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.instances.Instance;
import velvetdawn.core.models.instances.TileInstance;
import velvetdawn.core.models.instances.WorldInstance;
import velvetdawn.core.models.instances.entities.EntityInstance;

public class AttributeUpdate {

    public Instance parent;
    public String attribute;
    public Any value;
    public long updateTime;

    public AttributeUpdate(Instance parent, String attribute, Any value) {
        this.parent = parent;
        this.attribute = attribute;
        this.value = value;

        this.updateTime = System.currentTimeMillis();
    }

    public String getParentType() {
        if (this.parent instanceof EntityInstance)
            return "entity";
        if (this.parent instanceof TileInstance)
            return "tile";
        if (this.parent instanceof WorldInstance)
            return "world";
        return "unknown";
    }
}
