package test.velvetdawn.entities;

import org.junit.Test;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;

import static org.junit.Assert.assertEquals;


public class TestEntityCombat extends test.BaseTest {

    /** This function tests one unit attacking multiple units in the same position */
    @Test
    public void test_unit_combat() throws Exception {
        var velvetDawn = this.prepareGame();

        var entities = velvetDawn.entities.list();
        var attacker = entities.get(0);
        var attackees = entities.subList(1, entities.size());
        var target_position = new Coordinate(attacker.position.x + 1, attacker.position.y);

        attacker.attributes.set("health", Any.from(100));
        attacker.attributes.set("combat.attack", Any.from(30));

        attackees.forEach(attackee -> {
            velvetDawn.entities.setPosition(attackee, target_position);
            attackee.attributes.set("health", Any.from(100));
            attackee.attributes.set("combat.attack", Any.from(20));
        });

        attacker.combat.attack(target_position);

        // Each of the three attackes should lose the (combat of the attacker)/(n attackees)
        attackees.forEach(attackee -> {
            assertEquals(90, attackee.attributes.get("health").toNumber(), 0);
        });

        // Each attackee damages the attacker
        assertEquals(40, attacker.attributes.get("health").toNumber(), 0);

        // TODO Test selectors ran
        // TODO, test: kill, blast radius and defense, validate range of target from attacker
    }
}