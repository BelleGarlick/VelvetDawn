package velvetdawn.server.models.datapacks;

import lombok.Builder;
import velvetdawn.core.models.datapacks.entities.EntityDefinition;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APIEntityDefinition {

    public String datapackId;
    public String name;
    public boolean commander;
    public String description;

    public APIEntityTexturesDefinition textures;

    public List<APIEntityPerformableDefinition> attributes;
    public List<APIEntityPerformableDefinition> upgrades;
    public List<APIEntityPerformableDefinition> abilities;

    public static APIEntityDefinition from(EntityDefinition value) {
        return APIEntityDefinition.builder()
                .datapackId(value.datapackId)
                .name(value.name)
                .commander(value.commander)
                .description(value.description)
                .textures(APIEntityTexturesDefinition.builder()
                        .background(value.textures.sprite)
                        .build())
                .attributes(APIEntityPerformableDefinition.fromAttributes(value.attributes.attributes))
                .upgrades(APIEntityPerformableDefinition.fromUpgrades(value.upgrades.list()))
                .abilities(APIEntityPerformableDefinition.fromAbilities(value.abilities.list()))
                .build();
    }

    public static List<APIEntityDefinition> from(Collection<EntityDefinition> values) {
        return values
                .stream()
                .map(APIEntityDefinition::from)
                .collect(Collectors.toList());
    }

    @Builder
    static class APIEntityTexturesDefinition {
        public String background;
    }
}
