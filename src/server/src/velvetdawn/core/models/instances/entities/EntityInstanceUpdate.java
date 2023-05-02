package velvetdawn.core.models.instances.entities;

import com.google.gson.JsonObject;
import lombok.Builder;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;

@Builder
public class EntityInstanceUpdate {

    public String instanceId;
    public String datapackId;
    public Coordinate position;
    public long time;
    public String player;

    public static EntityInstanceUpdate from(EntityInstance entity) {
        return EntityInstanceUpdate.builder()
                .instanceId(entity.instanceId)
                .datapackId(entity.datapackId)
                .position(entity.position)
                .time(System.currentTimeMillis())
                .player(entity.player.name)
                .build();
    }
}
