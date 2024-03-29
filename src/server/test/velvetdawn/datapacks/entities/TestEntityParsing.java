package velvetdawn.datapacks.entities;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.datapacks.entities.EntityDefinition;

import java.util.List;

import static junit.framework.TestCase.assertEquals;
import static org.junit.Assert.assertThrows;


public class TestEntityParsing extends BaseTest {

    @Test
    public void test_unit_health() throws Exception {
        var entityDef = new EntityDefinition("", "", false, "");

        // Type is wrong
        assertThrows(Exception.class, () ->
            entityDef.parseHealth(new AnyJson().set("health", new AnyJson().set("max", "dsaa"))));

        // Must be at least 0
        assertThrows(Exception.class, () ->
            entityDef.parseHealth(new AnyJson().set("health", new AnyJson().set("max", -1))));

        // Wrong key
        assertThrows(Exception.class, () ->
            entityDef.parseHealth(new AnyJson().set("health", new AnyJson().set("random-key", false))));

        // Valid
        entityDef.parseHealth(new AnyJson()
                .set("health", new AnyJson()
                        .set("max", 100)
                        .set("notes", "example")));
        assertEquals(100.0, entityDef.attributes.get("health.max").value.toNumber(), 0);
    }

    @Test
    public void test_unit_combat() throws Exception {
        var entityDef = new EntityDefinition("", "", false, "");

        // Type is wrong
        List.of("range", "attack", "defence", "reload").forEach(key ->
                assertThrows(Exception.class, () ->
                        entityDef.parseCombat(new AnyJson().set("combat", new AnyJson().set(key, "dsa")))));

        // Must be at least 0
        List.of("range", "attack", "defence", "reload").forEach(key ->
                assertThrows(Exception.class, () ->
                        entityDef.parseCombat(new AnyJson().set("combat", new AnyJson().set(key, -1)))));

        // Wrong key
        assertThrows(Exception.class, () ->
                entityDef.parseCombat(new AnyJson().set("combat", new AnyJson().set("random-key", 10))));

        // Valid
        entityDef.parseCombat(new AnyJson()
                .set("combat", new AnyJson()
                        .set("range", 5)
                        .set("attack", 10)
                        .set("defense", 20)
                        .set("cooldown", 9)
                        .set("blast-radius", 11)
                        .set("notes", "Example")));

        assertEquals(5.0, entityDef.attributes.get("combat.range").value.toNumber(), 0.001);
        assertEquals(10.0, entityDef.attributes.get("combat.attack").value.toNumber(), 0.001);
        assertEquals(20.0, entityDef.attributes.get("combat.defense").value.toNumber(), 0.001);
        assertEquals(9, entityDef.attributes.get("combat.cooldown").value.toNumber(), 0.001);
        assertEquals(11, entityDef.attributes.get("combat.blast-radius").value.toNumber(), 0.001);
    }

    @Test
    public void test_unit_movement() throws Exception {
        var entityDef = new EntityDefinition("", "", false, "");

        // Type is wrong
        assertThrows(Exception.class, () ->
                entityDef.parseMovement(new AnyJson().set("movement", new AnyJson().set("range", "dsa"))));

        // Wrong key
        assertThrows(Exception.class, () ->
                entityDef.parseMovement(new AnyJson().set("movement", new AnyJson().set("range", 2).set("random-key", false))));

        // Valid
        entityDef.parseMovement(new AnyJson()
                .set("movement", new AnyJson()
                        .set("range", 5)
                        .set("notes", "Example")));

        assertEquals(5f, entityDef.attributes.get("movement.range").value.toNumber());
    }
}
