package velvetdawn.core.models.instances.attributes;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.models.instances.Instance;
import velvetdawn.core.models.instances.WorldInstance;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Attributes {

    // Static list of updates which are collected here and broadcast to users
    private static ArrayList<AttributeUpdate> attributeUpdates = new ArrayList<>();
    private static long AttributeStaleAge = 10 * 1000;  // 10 seconds

    private Instance parent;

    public final Map<String, Any> attributes = new HashMap<>();
    public final Map<String, Any> defaultAttributes = new HashMap<>();

    public static List<AttributeUpdate> getUpdates(VelvetDawn velvetDawn, boolean fullState) {
        if (fullState) {
            ArrayList<AttributeUpdate> updates = new ArrayList<>();
            updates.addAll(WorldInstance.getInstance().attributes.getAsAttributeUpdates());
            updates.addAll(velvetDawn.entities.list()
                    .stream()
                    .map(entitiy -> entitiy.attributes.getAsAttributeUpdates())
                    .flatMap(Collection::stream)
                    .collect(Collectors.toList()));
            updates.addAll(velvetDawn.map.listTiles()
                    .stream()
                    .map(tile -> tile.attributes.getAsAttributeUpdates())
                    .flatMap(Collection::stream)
                    .collect(Collectors.toList()));
            return updates;

        } else {
            while (!attributeUpdates.isEmpty()) {
                if (Attributes.attributeUpdates.get(0).updateTime < System.currentTimeMillis() - AttributeStaleAge)
                    attributeUpdates.remove(0);
                else
                    break;
            }
            return attributeUpdates;
        }
    }

    public Attributes(Instance parent) {
        this.parent = parent;
    }

    public void set(String attribute, Any value) {
        if (!this.defaultAttributes.containsKey(attribute))
            this.defaultAttributes.put(attribute, value);
        this.attributes.put(attribute, value);

        Attributes.attributeUpdates.add(new AttributeUpdate(this.parent, attribute, value));
    }

    public void reset(String attribute, Any value) {
        var attr = this.defaultAttributes.get(attribute);
        if (attr == null)
            this.set(attribute, value);
        else
            this.set(attribute, attr);
    }

    public Any get(String attribute) {
        return this.get(attribute, Any.Null());
    }

    public Any get(String attribute, Any defaultValue) {
        return this.attributes.getOrDefault(attribute, defaultValue);
    }

    public List<AttributeUpdate> getAsAttributeUpdates() {
        return this.attributes
                .entrySet()
                .stream()
                .map(entry -> new AttributeUpdate(this.parent, entry.getKey(), entry.getValue()))
                .collect(Collectors.toList());
    }
}
