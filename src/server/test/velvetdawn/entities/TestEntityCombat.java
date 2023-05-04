package velvetdawn.entities;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.constants.AttributeKeys;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;

import java.util.stream.Collectors;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;


public class TestEntityCombat extends BaseTest {

    /** This function tests one unit attacking multiple units in the same position */
    @Test
    public void testUnitCombat() throws Exception {
        var velvetDawn = this.prepareGame();

        var attacker = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);
        var attackees = velvetDawn.entities.list().stream().filter(x -> x != attacker).collect(Collectors.toSet());
        var targetPosition = new Coordinate(attacker.position.x + 1, attacker.position.y);

        attacker.attributes.set("health", Any.from(100));
        attacker.attributes.set("combat.attack", Any.from(30));

        attackees.forEach(attackee -> {
            velvetDawn.entities.setPosition(attackee, targetPosition);
            attackee.attributes.set("health", Any.from(100));
            attackee.attributes.set("combat.attack", Any.from(20));
        });

        attacker.combat.attack(targetPosition);

        // Each of the three attackes should lose the (combat of the attacker)/(n attackees)
        attackees.forEach(attackee ->
            assertEquals(90, attackee.attributes.get("health").toNumber(), 0));

        // Each attackee damages the attacker
        assertEquals(40, attacker.attributes.get("health").toNumber(), 0);

        // TODO Test selectors ran
        // TODO, test: kill and defense, validate range of target from attacker
    }

    /** This function tests blast radius for combat */
    @Test
    public void testUnitCombatBlastRadius() throws Exception {
        var velvetDawn = this.prepareGame();

        // Get entities
        var p1Entity1 = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);
        var p1Entity2 = velvetDawn.entities.getAtPosition(new Coordinate(4, 0)).get(0);
        var p1Entity3 = velvetDawn.entities.getAtPosition(new Coordinate(6, 0)).get(0);
        var p2Instance = velvetDawn.entities.getAtPosition(new Coordinate(5, 2)).get(0);

        // Test correct values to begin with
        assertEquals(100, p1Entity1.attributes.get("health").toNumber(), 0.01);
        assertEquals(100, p1Entity2.attributes.get("health").toNumber(), 0.01);
        assertEquals(100, p1Entity3.attributes.get("health").toNumber(), 0.01);

        // Test 0 blast radius works as expected
        p2Instance.attributes.set("combat.blast-radius", Any.from(0));
        p2Instance.combat.attack(new Coordinate(5, 0));
        assertTrue(p1Entity1.attributes.get("health").toNumber() < 99);
        assertEquals(100, p1Entity2.attributes.get("health").toNumber(), 0.01);
        assertEquals(100, p1Entity3.attributes.get("health").toNumber(), 0.01);

        // Test larger blast radius affects surrounding entities
        p2Instance.attributes.set("combat.blast-radius", Any.from(1));
        p2Instance.attributes.set("combat.cooldown.remaining", Any.from(0));  // Set to 0 so can attack again
        p2Instance.combat.attack(new Coordinate(5, 0));
        assertTrue(p1Entity1.attributes.get("health").toNumber() < 96);
        assertTrue(p1Entity2.attributes.get("health").toNumber() < 99);
        assertTrue(p1Entity3.attributes.get("health").toNumber() < 99);
    }

    @Test
    public void testCombatCooldownCycle() throws Exception {
        var velvetDawn = this.prepareGame();

        var attacker = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);
        velvetDawn.entities.setPosition(attacker, new Coordinate(5, 1));  // Set position as to put it next to enemy item

        // Test cooldown starts at 0
        assertEquals(0f, attacker.attributes.get(AttributeKeys.EntityCombatCooldownRemaining).toNumber(), 0);

        // Attack enemy item in this tile increases the cooldown
        attacker.combat.attack(new Coordinate(5, 2));
        assertEquals(5f, attacker.attributes.get(AttributeKeys.EntityCombatCooldownRemaining).toNumber(), 0);
        // Attacking again will throw the error since cooldown is not 0
        assertThrows(Exception.class, () ->
                attacker.combat.attack(new Coordinate(5, 2)));

        // Through five rounds checking the cooldown each time
        for (int round = 4; round >= 0; round--) {
            for (int i = 0; i < 2; i++)
                velvetDawn.game.turns.beginNextTurn();

            // Assert cooldown decreases each round
            assertEquals(round, attacker.attributes.get(AttributeKeys.EntityCombatCooldownRemaining).toNumber(), 0);
        }

        // Test can attack with no error raised and cooldown increases again
        attacker.combat.attack(new Coordinate(5, 2));
        assertEquals(5f, attacker.attributes.get(AttributeKeys.EntityCombatCooldownRemaining).toNumber(), 0);
    }
}
