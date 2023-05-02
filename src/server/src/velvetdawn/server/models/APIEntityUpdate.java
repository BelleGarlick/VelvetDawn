package velvetdawn.server.models;

import lombok.Builder;
import velvetdawn.core.entities.EntityInstanceUpdate;

import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APIEntityUpdate {

    public String instanceId;
    public APICoordinate position;
    public String datapackId;
    public String player;

    public static APIEntityUpdate fromUpdate(EntityInstanceUpdate update) {
        return APIEntityUpdate.builder()
                .instanceId(update.instanceId)
                .datapackId(update.datapackId)
                .player(update.player)
                .position(APICoordinate.fromCoordinate(update.position))
                .build();
    }

    public static List<APIEntityUpdate> fromUpdates(List<EntityInstanceUpdate> updates) {
        return updates.stream().map(APIEntityUpdate::fromUpdate).collect(Collectors.toList());
    }
}
