package velvetdawn.models.instances.attributes;

import velvetdawn.VelvetDawn;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;
import velvetdawn.models.anytype.AnyNull;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Attributes {

    public final Map<String, Attribute> attributes = new HashMap<>();
    public final Map<String, Attribute> defaultAttributes = new HashMap<>();

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
            this.set(attribute, attr.value);
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
    public void load(VelvetDawn velvetDawn, String parentId, AnyJson json) throws Exception {
        AnyList data = json.get("attributes", Any.list()).validateInstanceIsList(String.format(
                "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId));

        for (Any item: data.items) {
            var attr = Attribute.load(velvetDawn, parentId, item.validateInstanceIsJson(String.format(
                    "Attributes in '%s' are invalid. Attributes must be a list of json objects.", parentId)));
            this.attributes.put(attr.id, attr);
        }
    }
}
