package velvetdawn.models.instances.attributes;

import velvetdawn.VelvetDawn;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;
import velvetdawn.models.instances.Instance;

import java.util.ArrayList;

public class AttributesDefinition {

    private final ArrayList<Attribute> attributes = new ArrayList<>();

    /** Parse the data to create the attributes */
    public void load(VelvetDawn velvetDawn, String parentId, AnyJson json) throws Exception {
        AnyList data = json.get("attributes", Any.list())
                .validateInstanceIsList(String.format(
                    "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId));

        for (Any item: data.items) {
            var attr = Attribute.load(velvetDawn, parentId, item.validateInstanceIsJson(String.format(
                    "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId)));
            attributes.add(attr);
        }
    }

    public void instantiateInstanceAttributes(Instance instance) {
        this.attributes.forEach(attribute -> instance.attributes.set(attribute.id, attribute.name, attribute.icon, attribute.value));
    }

    public void add(Attribute attr) {
        this.attributes.add(attr);
    }

    public Attribute get(String key) {
        return this.attributes.stream().filter(x -> x.id.equals(key)).findFirst().orElse(null);
    }
}
