package velvetdawn.server.models;

import com.google.gson.JsonObject;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.attributes.AttributeUpdate;

import java.util.List;
import java.util.stream.Collectors;

public class APIAttributeUpdate {

    public static List<JsonObject> fromUpdates(List<AttributeUpdate> updates) {
        return updates.stream().map(update -> new AnyJson()
                    .set("instanceId", update.parent.instanceId)
                    .set("attribute", update.attribute)
                    .set("value", update.value)
                    .set("type", update.getParentType())
                    .toGson())
                .collect(Collectors.toList());
    }
}
