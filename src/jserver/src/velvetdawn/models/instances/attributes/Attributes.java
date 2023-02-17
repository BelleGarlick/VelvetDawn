package velvetdawn.models.instances.attributes;

import velvetdawn.VelvetDawn;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyNull;
import velvetdawn.utils.Json;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Attributes {

    private final Map<String, Attribute> attributes = new HashMap<>();
    private final Map<String, Attribute> defaultAttributes = new HashMap<>();

    public void set(String attribute, String name, String icon, Any value) {
        if (!this.defaultAttributes.containsKey(attribute))
            this.defaultAttributes.put(attribute, new Attribute(attribute, name, icon, value));
        this.attributes.put(attribute, new Attribute(attribute, name, icon, value));
    }

    public void set(String attribute, Any value) {
        this.set(attribute, null, null, value);
    }

    public void reset(String attribute, Any value) {
        var attr = this.defaultAttributes.get(attribute);
        if (attr == null)
            this.set(attribute, value);
        else {
            attr.value = value;
        }
    }

    public Any get(String attribute) {
        var attr = this.attributes.get(attribute);
        if (attr != null)
            return attr.value;

        return Any.Null();
    }

    public Any get(String attribute, Any defaultValue) {
        var attr = this.attributes.get(attribute);
        if (attr != null)
            return attr.value;

        return defaultValue;
    }

    /** Parse the data to create the attributes */
    public void load(VelvetDawn velvetDawn, String parentId, Json json) throws Exception {
        List<Json> data = json.getStrictJsonList("attributes", List.of(), String.format(
                "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId));

        for (Json item: data) {
            var attr = Attribute.load(velvetDawn, parentId, item);
            this.attributes.put(attr.id, attr);
        }
    }
}
