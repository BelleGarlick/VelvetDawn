package velvetdawn.models.instances.entities;

import velvetdawn.VelvetDawn;
import velvetdawn.constants.AttributeKeys;
import velvetdawn.constants.AttributeValues;
import velvetdawn.models.Coordinate;
import velvetdawn.models.anytype.Any;

public class Combat {

    private final VelvetDawn velvetDawn;
    private final EntityInstance entity;

    public Combat(VelvetDawn velvetDawn, EntityInstance entity) {
        this.velvetDawn = velvetDawn;
        this.entity = entity;
    }

    /** This function handles combat between one unit and all units in the target
     * positions.
     *
     * This function will handle:
     *  - one unit against multiple units
     *
     * @param target The position the unit is attacking
     */
    public void attack(Coordinate target) throws Exception {
        var attackees = velvetDawn.entities.getAtPosition(target);
        if (attackees.isEmpty())
            throw new Exception("No units found in this position");

        // Perform attack on all units in the position
        var combatDamage = this.entity.attributes.get(AttributeKeys.EntityAttack, Any.from(AttributeValues.DefaultEntityHealthMax)).toNumber() / attackees.size();
        for (EntityInstance instance: attackees) {
            // Both units attack each other but the attacks damange is shared across units
            damageEntity(instance, combatDamage);
            damageEntity(this.entity, instance.attributes.get(AttributeKeys.EntityAttack).toNumber());
        }
    }

    // TODO Triggers
    public void damageEntity(EntityInstance entity, float damage) {
        var newHealth = entity.attributes.get("health", Any.from(AttributeValues.DefaultEntityHealthMax)).toNumber() - damage;

        if (newHealth <= 0)
            // TODO Chat message saying '{player_name}'s {unit name} killed {player_names}'s {unit name}'
            velvetDawn.entities.kill(entity);

        else
            entity.attributes.set("health", Any.from(newHealth));
    }
}
