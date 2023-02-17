package velvetdawn.models.instances.attributes;

import velvetdawn.VelvetDawn;
import velvetdawn.models.instances.Instance;
import velvetdawn.utils.Json;

import java.util.ArrayList;
import java.util.List;

public class AttributesDefinition {

    private final ArrayList<Attribute> attributes = new ArrayList<>();

    /** Parse the data to create the attributes */
    public void load(VelvetDawn velvetDawn, String parentId, Json json) throws Exception {
        List<Json> data = json.getStrictJsonList("attributes", List.of(), String.format(
                "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId));

        for (Json item: data) {
            var attr = Attribute.load(velvetDawn, parentId, item);
            attributes.add(attr);
        }
    }

    public void instantiateInstanceAttributes(Instance instance) {
        this.attributes.forEach(attribute -> instance.attributes.set(attribute.id, attribute.name, attribute.icon, attribute.value));
    }

    public void add(Attribute attr) {
        this.attributes.add(attr);
    }
}
