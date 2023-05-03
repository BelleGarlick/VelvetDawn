package velvetdawn.core.models.instances.attributes;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyNull;
import velvetdawn.core.models.anytype.AnyString;
import velvetdawn.core.models.instances.Instance;

import java.util.Set;

public class AttributeDefinition {

    public static Set<String> AvailableKeys = Set.of("id", "name", "icon", "default", "notes");

    public final String id;
    public final String name;
    public final String icon;
    public Any value;
    public final long updateTime;

    public AttributeDefinition(String id, Any value) {
        this(id, null, null, value);
    }

    public AttributeDefinition(String id, String name, String icon, Any value) {
        this.id = id;
        this.name = name;
        this.icon = icon;
        this.value = value;
        updateTime = System.currentTimeMillis();
    }

    public static AttributeDefinition load(VelvetDawn velvetDawn, String parentId, AnyJson data) throws Exception {
        for (String key: data.keys()) {
            if (!AvailableKeys.contains(key))
                throw new Exception(String.format("%s's attributes have unknown key: '%s'", parentId, key));
        }

        Any rawAttrId = data.get("id");
        AnyString attrId = rawAttrId.validateInstanceIsString(String.format(
                "Attribute ids must be strings. Found incorrect type '%s' in %s", rawAttrId.toString(), parentId))
                .validateRegex("^[a-z][a-z0-9-.]{0,64}$", String.format("Object '%s' attribute id '%s' is not valid. Id must be at least 1 and smaller than 64 chars long and contain only letters, numbers or hyphens and begin in a letter. All letters must be lowercase.", parentId, rawAttrId.toString()));

        AnyString attrName = data.get("name")
                .validateInstanceIsString(String.format("Object '%s' attribute name in '%s' is not valid. Must be a string.", parentId, attrId))
                .validateRegex("^[a-zA-Z0-9. ]{1,32}$", String.format("Object '%s' has invalid attribute name. Names must be at least 1 and smaller than 33 chars long and contain only letters or numbers.", parentId));

        Any defaultValue = data.get("default", Any.Null());

        // Load the icon, if it's not null, extract the string value and validate
        Any attrIcon = data.get("icon", Any.Null());
        String icon = null;
        if (!(attrIcon instanceof AnyNull)) {
            icon = attrIcon.validateInstanceIsString(
                    String.format("Object '%s' attribute '%s' icon is not valid. Must be a string.", parentId, attrId.value))
                    .value;

            if (!velvetDawn.datapacks.resources.containsKey(icon))
                System.out.println(String.format("Object '%s' attribute '%s' icon is not valid. Resource '%s' not found.", parentId, attrId, icon));
        }

        return new AttributeDefinition(attrId.toString(), attrName.toString(), icon, defaultValue);
    }
}
