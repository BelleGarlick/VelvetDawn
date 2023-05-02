package velvetdawn.core.entities;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Abilities {

    private final EntityInstance entity;
    private final VelvetDawn velvetDawn;

    public Abilities(VelvetDawn velvetDawn, EntityInstance entity) {
        this.velvetDawn = velvetDawn;
        this.entity = entity;
    }

    /** Verify and run an ability on a unit
     *
     * @param abilityId The ability ID to run
     */
    public void perform(String abilityId) throws Exception {
        var entityDefinition = velvetDawn.datapacks.entities.get(this.entity.datapackId);
        if (entityDefinition == null)
            throw new Exception(String.format("Entity definition not found for %s.", this.entity.datapackId));

        var ability = entityDefinition.abilities.getById(abilityId);
        if (ability == null)
            throw new Exception(String.format("Ability '%s' not found", abilityId));

        // Check is not hidden
        var hidden = ability.isHidden(entity);
        if (hidden.isTrue)
            throw new Exception(String.format("Cannot run ability. %s", hidden.reason));
    
        // Check is not disabled
        var enabled = ability.isEnabled(entity);
        if (!enabled.isTrue)
            throw new Exception(String.format("Cannot run ability. %s", enabled.reason));
    
        ability.run(entity);
    }

    /** Get the breakdown of abilities that are hidden / disabled
     or already used */
    public EntityAbilityData getAbilityUpdates() {
        var abilities = new EntityAbilityData(entity.instanceId);

        var entityDefinition = velvetDawn.datapacks.entities.get(this.entity.datapackId);
        if (entityDefinition == null)
            return abilities;

        // Iterate through all abilities to find which can/can't be run
        for (var ability: entityDefinition.abilities.abilities.values()) {
            // Check if not hidden
            var hidden = ability.isHidden(this.entity);
            if (hidden.isTrue) {
                abilities.hidden.add(new NotActionable(ability.id, hidden.reason));
                continue;
            }

            // Check if enabled
            var isEnabled = ability.isEnabled(this.entity);
            if (!isEnabled.isTrue) {
                abilities.disabled.add(new NotActionable(ability.id, isEnabled.reason));
                continue;
            }

            abilities.abilities.add(ability.id);
        };

        return abilities;
    }

    private static class NotActionable {

        public final String abilityId;
        public final String reason;

        public NotActionable(String abilityId, String reason) {
            this.abilityId = abilityId;
            this.reason = reason;
        }

        public AnyJson json() {
            return new AnyJson()
                    .set("abilityId", this.abilityId)
                    .set("reason", this.reason);
        }
    }

    public static class EntityAbilityData {
        
        private final String instanceId;

        public final List<NotActionable> hidden = new ArrayList<>();
        public final List<NotActionable> disabled = new ArrayList<>();
        public final List<String> abilities = new ArrayList<>();
        
        public EntityAbilityData(String instanceId) {
            this.instanceId = instanceId;
        }

        public AnyJson json() {
            return new AnyJson()
                    .set("instance", this.instanceId)
                    .set("hidden", new AnyList(this.hidden.stream().map(NotActionable::json).collect(Collectors.toList())))
                    .set("disabled", new AnyList(this.disabled.stream().map(NotActionable::json).collect(Collectors.toList())))
                    .set("abilities", AnyList.of(this.abilities));
        }
    }
}
