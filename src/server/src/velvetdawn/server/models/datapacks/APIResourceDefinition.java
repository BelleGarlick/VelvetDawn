package velvetdawn.server.models.datapacks;

import lombok.Builder;
import velvetdawn.core.models.datapacks.ResourceDefinition;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APIResourceDefinition {

    public final String resourceId;
    public final String type;
    public final Integer imWidth;
    public final Integer imHeight;

    public static APIResourceDefinition from(ResourceDefinition value) {
        return APIResourceDefinition.builder()
                .resourceId(value.resourceId)
                .type(value.type.toString())
                .imWidth(value.imWidth)
                .imHeight(value.imHeight)
                .build();
    }

    public static List<APIResourceDefinition> from(Collection<ResourceDefinition> values) {
        return values
                .stream()
                .map(APIResourceDefinition::from)
                .collect(Collectors.toList());
    }
}
