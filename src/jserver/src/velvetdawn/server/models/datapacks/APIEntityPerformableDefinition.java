package velvetdawn.server.models.datapacks;

import lombok.Builder;
import velvetdawn.core.mechanics.abilities.Ability;
import velvetdawn.core.mechanics.upgrades.Upgrade;
import velvetdawn.core.models.instances.attributes.AttributeDefinition;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APIEntityPerformableDefinition {

    public String id;
    public String icon;
    public String name;
    public String description;

    public static List<APIEntityPerformableDefinition> fromUpgrades(Collection<Upgrade> list) {
        return list.stream().map(item ->
                        APIEntityPerformableDefinition.builder()
                                .id(item.id)
                                .icon(item.icon)
                                .name(item.name)
                                .description(item.description)
                                .build())
                .collect(Collectors.toList());
    }

    public static List<APIEntityPerformableDefinition> fromAbilities(Collection<Ability> list) {
        return list.stream().map(item ->
                        APIEntityPerformableDefinition.builder()
                                .id(item.id)
                                .icon(item.icon)
                                .name(item.name)
                                .description(item.description)
                                .build())
                .collect(Collectors.toList());
    }

    public static List<APIEntityPerformableDefinition> fromAttributes(ArrayList<AttributeDefinition> list) {
        return list.stream().map(item ->
                        APIEntityPerformableDefinition.builder()
                                .id(item.id)
                                .icon(item.icon)
                                .name(item.name)
                                .build())
                .collect(Collectors.toList());
    }
}
