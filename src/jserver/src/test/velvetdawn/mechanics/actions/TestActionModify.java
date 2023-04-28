package test.velvetdawn.mechanics.actions;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.actions.ActionModify;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyJson;

import java.util.ArrayList;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;


public class TestActionModify extends BaseTest {

    @Test
    public void test_parsing_dict() throws Exception {
        var velvetDawn = new VelvetDawn(this.getConfig());

        // Wrong major key
        assertThrows(Exception.class, () -> ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modifies", "self.health").set("set", 0)));

        // No function type
        assertThrows(Exception.class, () -> ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modifies", "self.health")));

        // too many function type
        assertThrows(Exception.class, () -> ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health")
                .set("set", 0)
                .set("add", 1)));

        // Can't modify non-attribute
        assertThrows(Exception.class, () -> ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self")
                .set("set", 0)));

        // Just right
        var action = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health")
                .set("sub", 0));
        assertEquals(action.function, ActionModify.ActionModifierFunction.SUB);
    }

    @Test
    public void test_modifier_working() throws Exception {
        var velvetDawn = this.prepareGame();

        var entity = velvetDawn.entities.list().get(0);

        var actionSet = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health").set("set", 50));

        var actionAdd = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health").set("add", 10));

        var actionSub = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health").set("sub", 5));

        var actionMul = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health").set("mul", 2));

        // Test resetting and reset to a default if the attribute doens't exists
        var actionReset = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.health").set("reset", 0));
        var actionResetOther = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.healthy").set("reset", 9));

        assertEquals(100, entity.attributes.get("health").toNumber(), 0);

        actionSet.run(entity);
        actionAdd.run(entity);
        actionSub.run(entity);
        actionMul.run(entity);

        assertEquals(110, entity.attributes.get("health").toNumber(), 0);

        actionReset.run(entity);
        actionResetOther.run(entity);

        assertEquals(100, entity.attributes.get("health").toNumber(), 0);
        assertEquals(9, entity.attributes.get("healthy").toNumber(), 0);
    }

    @Test
    public void test_modifier_function_value() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.list().get(0);
        unit.attributes.set("actual", Any.from(12));

        var actionRaw = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.example").set("set", "raw-value"));
        var actionRandom = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.example").set("set", "__rand__"));
        var actionSelector = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self.example").set("set", "@self.actual"));

        // Tet raw
        actionRaw.run(unit);
        assertEquals("raw-value", unit.attributes.get("example").toString());

        // Test random
        actionRandom.run(unit);
        assertTrue(1 >= unit.attributes.get("example").toNumber()
                && unit.attributes.get("example").toNumber() >= 0);

        // Test selector
        assertNotEquals(12, unit.attributes.get("example").toNumber());
        actionSelector.run(unit);
        assertEquals(12, unit.attributes.get("example").toNumber(), 0);
    }

    @Test
    public void test_modifier_tags() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.list().get(0);

        var actionAddTag = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self").set("add-tag", "tagg"));

        var actionRemoveTag = ActionModify.fromJson(velvetDawn, "id", new AnyJson()
                .set("modify", "self").set("remove-tag", "tagg"));

        assertFalse(unit.tags.contains("tagg"));
        actionAddTag.run(unit);
        assertTrue(unit.tags.contains("tagg"));
        actionRemoveTag.run(unit);
        assertFalse(unit.tags.contains("tagg"));
    }
}

