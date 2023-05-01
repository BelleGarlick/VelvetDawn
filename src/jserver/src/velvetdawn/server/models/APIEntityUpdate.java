package velvetdawn.server.models;

import com.google.gson.JsonObject;
import lombok.Builder;
import velvetdawn.core.models.instances.entities.EntityInstanceUpdate;

import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APIEntityUpdate {

    public String instanceId;
    public APICoordinate position;
    public JsonObject attrUpdate;
    public long time;

    public static APIEntityUpdate fromUpdate(EntityInstanceUpdate update) {
        return APIEntityUpdate.builder()
                .instanceId(update.instanceId)
                .position(APICoordinate.fromCoordinate(update.position))
                .attrUpdate(update.attrUpdate.toGson())
                .time(update.time)
                .build();
    }

    public static List<APIEntityUpdate> fromUpdates(List<EntityInstanceUpdate> updates) {
        return updates.stream().map(APIEntityUpdate::fromUpdate).collect(Collectors.toList());
    }
}
