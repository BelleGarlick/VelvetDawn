package velvetdawn.server.models.datapacks;

import lombok.Builder;
import velvetdawn.core.models.datapacks.tiles.TileDefinition;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APITileDefinition {

    public String datapackId;
    public String name;

    public static APITileDefinition from(TileDefinition value) {
        return APITileDefinition.builder()
                .datapackId(value.id)
                .name(value.name)
                .build();
    }

    public static List<APITileDefinition> from(Collection<TileDefinition> values) {
        return values
                .stream()
                .map(APITileDefinition::from)
                .collect(Collectors.toList());
    }
}
