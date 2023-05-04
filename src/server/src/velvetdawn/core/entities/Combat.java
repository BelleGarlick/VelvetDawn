package velvetdawn.core.entities;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.constants.AttributeKeys;
import velvetdawn.core.constants.AttributeValues;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyFloat;

import java.util.Collection;
import java.util.stream.Collectors;

import static velvetdawn.core.constants.AttributeKeys.EntityCombatBlastRadius;

public class Combat {

    private final VelvetDawn velvetDawn;
    private final EntityInstance entity;

    public Combat(VelvetDawn velvetDawn, EntityInstance entity) {
        this.velvetDawn = velvetDawn;
        this.entity = entity;
    }

    // TODO update documentation
    /** This function handles combat between one unit and all units in the target
     * positions.
     *
     * This function will handle:
     *  - one unit against multiple units
     *
     * @param target The position the unit is attacking
     */
    public void attack(Coordinate target) throws Exception {
        // Check if can attack based on remaining cooldown
        var remainingCooldown = this.entity.attributes.get(AttributeKeys.EntityCombatCooldownRemaining).toNumber();
        if (remainingCooldown > 0)
            throw new Exception("Unable to attack whilst cooldown is greater than 0");

        // Get all cells targeted by the attack
        int blastRadius = (int) this.entity.attributes.get(EntityCombatBlastRadius, Any.from(0)).toNumber();
        var targetCells = velvetDawn.map.getNeighboursInRange(target, blastRadius);

        // Get all entities in those position
        var attackees = targetCells.stream()
                .map(velvetDawn.entities::getAtPosition)
                .flatMap(Collection::stream)
                .filter(x -> x != this.entity)
                .collect(Collectors.toSet());

        if (attackees.isEmpty())
            throw new Exception("Nothing to attack.");

        // Perform attack on all units in the position
        var combatDamage = this.entity.attributes.get(AttributeKeys.EntityCombatDamage, Any.from(AttributeValues.DefaultEntityHealthMax)).toNumber() / attackees.size();
        for (EntityInstance instance: attackees) {
            // Both units attack each other but the attacks damage is shared across units
            damageEntity(instance, combatDamage);
            // TODO Take into account combat range so entities can't damange another entity at range
            damageEntity(this.entity, instance.attributes.get(AttributeKeys.EntityCombatDamage).toNumber());
        }

        // Update the attackers cooldown to prevent them attacking again
        this.entity.attributes.set(AttributeKeys.EntityCombatCooldownRemaining, new AnyFloat(
                Math.max(0, this.entity.attributes.get(AttributeKeys.EntityCombatCooldownRemaining).toNumber())
                + this.entity.attributes.get(AttributeKeys.EntityCombatCooldown).toNumber()));
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
