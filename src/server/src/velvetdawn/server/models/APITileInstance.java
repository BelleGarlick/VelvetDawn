package velvetdawn.server.models;

import lombok.Builder;
import velvetdawn.core.models.instances.TileInstance;

@Builder
public class APITileInstance {

    public String datapackId;
    public String instanceId;
    public APICoordinate position;

    public static APITileInstance from(TileInstance tile) {
        return APITileInstance.builder()
                .datapackId(tile.datapackId)
                .instanceId(tile.instanceId)
                .position(APICoordinate.fromCoordinate(tile.position))
                .build();
    }
}
