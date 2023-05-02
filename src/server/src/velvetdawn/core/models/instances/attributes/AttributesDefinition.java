package velvetdawn.core.models.instances.attributes;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.models.instances.Instance;

import java.util.ArrayList;

public class AttributesDefinition {

    public final ArrayList<AttributeDefinition> attributes = new ArrayList<>();

    /** Parse the data to create the attributes */
    public void load(VelvetDawn velvetDawn, String parentId, AnyJson json) throws Exception {
        AnyList data = json.get("attributes", Any.list())
                .validateInstanceIsList(String.format(
                    "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId));

        for (Any item: data.items) {
            var attr = AttributeDefinition.load(velvetDawn, parentId, item.validateInstanceIsJson(String.format(
                    "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId)));
            attributes.add(attr);
        }
    }

    public void instantiateInstanceAttributes(Instance instance) {
        this.attributes.forEach(attribute -> instance.attributes.set(attribute.id, attribute.value));
    }

    public void set(String id, Any value) {
        this.set(id, null, null, value);
    }

    public void set(String id, String name, String icon, Any value) {
        attributes.removeIf(x -> x.id.equals(id));
        attributes.add(new AttributeDefinition(id, name, icon, value));
    }

    public AttributeDefinition get(String key) {
        return this.attributes.stream().filter(x -> x.id.equals(key)).findFirst().orElse(null);
    }
}
