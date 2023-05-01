package velvetdawn.server.models;

import lombok.Builder;
import velvetdawn.core.models.Coordinate;

@Builder
public class APICoordinate {

    public float x;
    public float y;

    public static APICoordinate fromCoordinate(Coordinate position) {
        return APICoordinate.builder()
                .x(position.x)
                .y(position.y)
                .build();
    }
}
